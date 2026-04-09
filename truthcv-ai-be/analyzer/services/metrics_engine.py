import math

def compute_shannon_entropy(percentages):
    """
    Computes Shannon entropy for language distribution and normalizes it to a 0-100 scale.
    """
    if not percentages:
        return 0
    
    entropy = 0.0
    for pct in percentages:
        p = pct / 100.0
        if p > 0:
            entropy -= p * math.log2(p)
            
    # Max entropy occurs when all languages are equally distributed.
    max_entropy = math.log2(len(percentages)) if len(percentages) > 1 else 1.0
    
    normalized = (entropy / max_entropy) * 100 if max_entropy > 0 else 0
    return int(min(100, max(0, normalized)))

def calculate_repo_quality(repo_data):
    """
    Computes a 0-100 score based on logarithmic star scaling, consistency, and patterns.
    """
    is_fork = repo_data.get("is_fork", False)
    has_description = repo_data.get("has_description", False)
    stars = repo_data.get("stars", 0)
    days_since_push = repo_data.get("days_since_push", 9999)
    days_since_creation = repo_data.get("days_since_creation", 9999)
    
    score = 0
    if not is_fork: 
        score += 20
    if has_description:
        score += 10
        
    # Logarithmic scaling for stars
    star_score = math.log1p(stars) * 4.5
    score += min(40, star_score)
    
    # Recency: Exponential decay
    recency_score = 20 * math.exp(-days_since_push / 90.0)
    score += recency_score
    
    # Age consistency
    active_lifespan = max(0, days_since_creation - days_since_push)
    lifespan_score = 10 * min(1.0, active_lifespan / 365.0)
    score += lifespan_score
    
    return int(min(100, max(0, score)))

def calculate_activity_score(parsed_repos, account_days_since_push):
    """
    Exponential decay based model for scoring developer activity curve realistically.
    """
    if account_days_since_push >= 9999:
        return 0, "low"

    recency_points = 50 * math.exp(-account_days_since_push / 60.0)
    
    total = len(parsed_repos)
    if total == 0:
        return int(recency_points), "low"
        
    density_sum = sum(math.exp(-r.get("days_since_push", 9999)/120.0) for r in parsed_repos)
    density_ratio = density_sum / total
    density_points = density_ratio * 50
    
    score = int(min(100, max(0, recency_points + density_points)))
    
    if score > 70:
        level = "high"
    elif score > 30:
        level = "medium"
    else:
        level = "low"
        
    return score, level

def rank_top_projects(parsed_repos, max_projects=5):
    """
    Selects projects based on: final_score = stars + quality_weight + recency_weight
    """
    def compute_rank_score(r):
        stars = r.get("stars", 0)
        quality = r.get("quality", 0)
        days_since_push = r.get("days_since_push", 9999)
        
        # recency weight converges dynamically
        recency_weight = 100 * math.exp(-days_since_push / 180.0) 
        quality_weight = quality * 1.5
        
        return stars + quality_weight + recency_weight
        
    ranked = sorted(parsed_repos, key=compute_rank_score, reverse=True)
    
    top_projects = []
    for r in ranked[:max_projects]:
        top_projects.append({
            "name": r["name"],
            "stars": r.get("stars", 0),
            "language": r.get("language_prop"),
            "last_updated": r.get("last_updated")
        })
    return top_projects

def get_recent_activity_level(account_days_since_push):
    if account_days_since_push <= 30:
        return "high"
    elif account_days_since_push <= 90:
        return "medium"
    return "low"
