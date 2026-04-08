import requests
from datetime import datetime, timezone

def get_github_data(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "User not found"}

    repos = response.json()
    if not isinstance(repos, list):
        return {"error": "Unexpected format from GitHub API"}

    now = datetime.now(timezone.utc)
    
    total_repos = 0
    original_repos = 0
    forked_repos = 0
    total_stars = 0
    
    language_counts = {}
    valid_language_repos = 0
    
    active_repos = 0
    inactive_repos = 0
    
    parsed_repos = []

    for repo in repos:
        # 1. Repository Filtering
        if repo.get("private"):
            continue
            
        total_repos += 1
        
        if repo.get("fork"):
            forked_repos += 1
        else:
            original_repos += 1
            
        # 4. Popularity Metrics
        stars = repo.get("stargazers_count", 0)
        total_stars += stars
        
        # 2. Language Analysis
        lang = repo.get("language")
        if lang:
            language_counts[lang] = language_counts.get(lang, 0) + 1
            valid_language_repos += 1
            
        # 3. Activity Detection
        pushed_at_str = repo.get("pushed_at")
        repo_pushed_dt = None
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
                
        parsed_repos.append({
            "name": repo.get("name"),
            "stars": stars,
            "language": lang,
            "last_updated": pushed_at_str,
            "pushed_dt": repo_pushed_dt
        })

    # Language Percentages
    top_languages = []
    if valid_language_repos > 0:
        for l, count in language_counts.items():
            pct = round((count / valid_language_repos) * 100)
            top_languages.append({"language": l, "percentage": pct})
        
        top_languages.sort(key=lambda x: x["percentage"], reverse=True)
        top_languages = top_languages[:5]

    # Activity: last_push
    valid_dates = [r["pushed_dt"] for r in parsed_repos if r["pushed_dt"]]
    last_push = max(valid_dates).isoformat().replace('+00:00', 'Z') if valid_dates else None

    # Top Projects Selection
    parsed_repos.sort(
        key=lambda r: (r["stars"], r["pushed_dt"] or datetime.min.replace(tzinfo=timezone.utc)), 
        reverse=True
    )
    
    top_projects = []
    for r in parsed_repos[:5]:
        top_projects.append({
            "name": r["name"],
            "stars": r["stars"],
            "language": r["language"],
            "last_updated": r["last_updated"]
        })

    avg_stars = round(total_stars / total_repos, 2) if total_repos > 0 else 0.0

    return {
        "total_repos": total_repos,
        "original_repos": original_repos,
        "forked_repos": forked_repos,
        "total_stars": total_stars,
        "avg_stars": avg_stars,
        "top_languages": top_languages,
        "activity": {
            "active_repos": active_repos,
            "inactive_repos": inactive_repos,
            "last_push": last_push
        },
        "top_projects": top_projects,
        
        # Retain backward compatibility so ResultCard.jsx doesn't break
        "repo_count": total_repos,
        "languages": language_counts
    }
