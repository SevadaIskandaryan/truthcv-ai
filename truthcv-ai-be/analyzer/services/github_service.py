import os
import math
import requests
import concurrent.futures
from datetime import datetime, timezone
from analyzer.services.metrics_engine import (
    compute_shannon_entropy,
    calculate_repo_quality,
    calculate_activity_score,
    rank_top_projects,
    get_recent_activity_level
)

# Simple module-level cache
_github_cache = {}

def get_github_session():
    session = requests.Session()
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        session.headers.update({"Authorization": f"token {token}"})
    return session

def fetch_repo_languages(session, owner, repo_name):
    cache_key = f"lang_{owner}_{repo_name}"
    if cache_key in _github_cache:
        return _github_cache[cache_key]

    url = f"https://api.github.com/repos/{owner}/{repo_name}/languages"
    try:
        resp = session.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            _github_cache[cache_key] = data
            return data
    except Exception:
        pass
    return {}

def get_github_data(username):
    session = get_github_session()
    
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    response = session.get(url)

    if response.status_code != 200:
        return {"error": "User not found or API rate limit exceeded"}

    repos = response.json()
    if not isinstance(repos, list):
        return {"error": "Unexpected format from GitHub API"}

    now = datetime.now(timezone.utc)
    
    total_repos = 0
    original_repos = 0
    forked_repos = 0
    total_stars = 0
    
    active_repos = 0
    inactive_repos = 0
    
    parsed_repos = []
    
    for repo in repos:
        if repo.get("private"):
            continue
            
        total_repos += 1
        is_fork = repo.get("fork", False)
        if is_fork:
            forked_repos += 1
        else:
            original_repos += 1
            
        stars = repo.get("stargazers_count", 0)
        total_stars += stars
        
        pushed_at_str = repo.get("pushed_at")
        repo_pushed_dt = None
        days_since_push = 9999
        
        if pushed_at_str:
            try:
                repo_pushed_dt = datetime.fromisoformat(pushed_at_str.replace('Z', '+00:00'))
                days_since_push = (now - repo_pushed_dt).days
                if days_since_push <= 90:
                    active_repos += 1
                else:
                    inactive_repos += 1
            except ValueError:
                pass

        created_at_str = repo.get("created_at")
        days_since_creation = 9999
        if created_at_str:
            try:
                repo_created_dt = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
                days_since_creation = (now - repo_created_dt).days
            except ValueError:
                pass
                
        has_description = bool(repo.get("description"))
        
        repo_data = {
            "owner": username,
            "name": repo.get("name"),
            "size": repo.get("size", 0),
            "stars": stars,
            "is_fork": is_fork,
            "has_description": has_description,
            "last_updated": pushed_at_str,
            "pushed_dt": repo_pushed_dt,
            "days_since_push": days_since_push,
            "days_since_creation": days_since_creation,
            "language_prop": repo.get("language")
        }
        
        # Inject quality using engine
        repo_data["quality"] = calculate_repo_quality(repo_data)
        parsed_repos.append(repo_data)

    # Repository Selection Optimization for Language Fetching
    def selection_score(r):
        score = 0
        if not r["is_fork"]:
            score += 1000
        if r["language_prop"]:
            score += 500
        
        # Mix in size and recency explicitly
        recency_multiplier = math.exp(-r["days_since_push"] / 365.0)
        size_score = min(r["size"], 100000) / 100.0
        score += size_score * recency_multiplier
        return score

    repos_to_fetch = sorted(parsed_repos, key=selection_score, reverse=True)[:30]
    
    global_lang_bytes = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_repo = {
            executor.submit(fetch_repo_languages, session, username, r["name"]): r
            for r in repos_to_fetch
        }
        for future in concurrent.futures.as_completed(future_to_repo):
            langs = future.result()
            for lang, bytes_count in langs.items():
                global_lang_bytes[lang] = global_lang_bytes.get(lang, 0) + bytes_count
                
    total_bytes = sum(global_lang_bytes.values())
    top_languages = []
    
    if total_bytes > 0:
        for l, b in global_lang_bytes.items():
            pct = round((b / total_bytes) * 100)
            if pct > 0:
                top_languages.append({"language": l, "percentage": pct})
        top_languages.sort(key=lambda x: x["percentage"], reverse=True)
        top_languages = top_languages[:5]
        
    primary_language = top_languages[0]["language"] if top_languages else None

    # Fallback to pure counts logically internally
    if not top_languages:
        simple_lang_counts = {}
        for r in parsed_repos:
            if r["language_prop"]:
                simple_lang_counts[r["language_prop"]] = simple_lang_counts.get(r["language_prop"], 0) + 1
        if simple_lang_counts:
            tc = sum(simple_lang_counts.values())
            for l, c in simple_lang_counts.items():
                top_languages.append({"language": l, "percentage": round((c / tc) * 100)})
            top_languages.sort(key=lambda x: x["percentage"], reverse=True)
            top_languages = top_languages[:5]
            primary_language = top_languages[0]["language"] if top_languages else None

    valid_dates = [r["pushed_dt"] for r in parsed_repos if r["pushed_dt"]]
    last_push_dt = max(valid_dates) if valid_dates else None
    last_push = last_push_dt.isoformat().replace('+00:00', 'Z') if last_push_dt else None

    account_days_since_push = (now - last_push_dt).days if last_push_dt else 9999
    recent_activity_level = get_recent_activity_level(account_days_since_push)
    activity_score, activity_level = calculate_activity_score(parsed_repos, account_days_since_push)

    sorted_by_quality = sorted(parsed_repos, key=lambda x: x["quality"], reverse=True)
    top_quality_repos = sorted_by_quality[:10]
    repo_quality_score = int(sum(r["quality"] for r in top_quality_repos) / len(top_quality_repos)) if top_quality_repos else 0

    language_percentages = [l["percentage"] for l in top_languages]
    language_diversity_score = compute_shannon_entropy(language_percentages)

    top_projects = rank_top_projects(parsed_repos)
    avg_stars = round(total_stars / total_repos, 2) if total_repos > 0 else 0.0

    return {
        "total_repos": total_repos,
        "original_repos": original_repos,
        "forked_repos": forked_repos,
        "total_stars": total_stars,
        "avg_stars": avg_stars,
        
        "top_languages": top_languages,
        "primary_language": primary_language,
        
        "activity": {
            "active_repos": active_repos,
            "inactive_repos": inactive_repos,
            "last_push": last_push,
            "activity_score": activity_score,
            "activity_level": activity_level,
            "recent_activity_level": recent_activity_level
        },
        
        "repo_quality_score": repo_quality_score,
        "language_diversity_score": language_diversity_score,
        
        "top_projects": top_projects,
        
        # UI Fallbacks
        "repo_count": total_repos,
        "languages": {l["language"]: l["percentage"] for l in top_languages}
    }
