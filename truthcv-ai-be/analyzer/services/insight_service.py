import json
# simple template to work on insights generation logic
def generate_insights(github_data):
   insights = []

   if github_data.get("repo_count", 0) < 5:
       insights.append("Low public repository activity")

   if "Python" in github_data.get("languages", {}):
       insights.append("Strong Python presence")

   if github_data.get("repo_count", 0) > 20:
       insights.append("Highly active developer")

   return insights

def generate_resume_insights(data: dict) -> dict:
    d = data.get("data", {})

    # ---------------------------
    # SCORE CALCULATION (0–100)
    # ---------------------------
    score = 0

    # Base from confidence + evidence
    confidence_map = {"low": 40, "medium": 50, "high": 65}
    overall_conf = d.get("confidence_assessment", {}).get("overall_confidence", "medium")
    score += confidence_map.get(overall_conf, 60)

    evidence = d.get("confidence_assessment", {}).get("evidence_coverage", 50)
    score += (evidence * 0.15)  # max +20

    # Skills consistency
    score += d.get("skills", {}).get("consistency_score", 0) * 0.1  # max +10

    # Impact quality
    score += d.get("impact_analysis", {}).get("metrics_quality_score", 0) * 0.1  # max +10

    # GitHub consistency (if exists)
    github_score = d.get("github_supporting", {}).get("consistency_score")
    if github_score:
        score += github_score * 0.1  # max +10

    # Penalties
    if d.get("experience_analysis", {}).get("overlapping_roles"):
        score -= 10

    if d.get("impact_analysis", {}).get("inflated_metrics_flag"):
        score -= 10

    if d.get("skill_validation", {}).get("skill_mismatch_flag"):
        score -= 10

    # Clamp score
    score = max(0, min(99, int(score)))

    # ---------------------------
    # ✅ CONFIDENT INSIGHTS
    # ---------------------------
    confident_insights = []

    # Strong skills
    for skill in d.get("skill_validation", {}).get("strongly_supported_skills", []):
        confident_insights.append(f"Strong evidence of {skill} expertise")

    # System complexity
    if d.get("system_complexity", {}).get("level") == "high":
        confident_insights.append("Experience working on high-complexity systems")

    # Ownership
    if d.get("ownership_analysis", {}).get("overall_level") == "high":
        confident_insights.append("Demonstrated high ownership across projects")

    # Strength signals
    for s in d.get("strength_signals", []):
        if s.get("confidence") in ["high", "medium"]:
            confident_insights.append(s.get("description"))

    # ---------------------------
    # ⚠️ AMBIGUITY INSIGHTS
    # ---------------------------
    ambiguity_insights = []

    # Ambiguities from AI
    for a in d.get("ambiguities", []):
        ambiguity_insights.append(a.get("text"))

    # Weak GitHub support
    github = d.get("github_supporting", {})
    if github.get("consistency_score", 100) < 70:
        ambiguity_insights.append("Limited GitHub evidence supporting some claimed skills")

    # Weakly supported skills
    for skill in d.get("skill_validation", {}).get("weakly_supported_skills", []):
        ambiguity_insights.append(f"Weak supporting evidence for {skill}")

    # Overlapping roles
    if d.get("experience_analysis", {}).get("overlapping_roles"):
        ambiguity_insights.append("Overlapping roles detected in timeline")

    # ---------------------------
    # ❌ HIGH RISK
    # ---------------------------
    high_risk = []

    for r in d.get("risk_signals", []):
        if r.get("severity") == "high":
            high_risk.append(r.get("description"))

    # Severe mismatch case
    if d.get("skill_validation", {}).get("skill_mismatch_flag"):
        high_risk.append("Significant mismatch between claimed and demonstrated skills")

    # Extreme experience mismatch (example rule)
    claimed = d.get("summary_analysis", {}).get("years_of_experience_claimed", 0)
    actual = d.get("experience_analysis", {}).get("total_experience_years_actual", 0)

    if claimed > 0 and actual > 0 and claimed > actual * 2:
        high_risk.append("Claimed experience significantly exceeds actual work history")

    # ---------------------------
    # ❔ QUESTIONS
    # ---------------------------
    questions = []

    for q in d.get("interview_questions", []):
        questions.append(q.get("question"))

    # Add ambiguity-driven questions
    for a in d.get("ambiguities", []):
        if a.get("suggested_question"):
            questions.append(a.get("suggested_question"))

    # ---------------------------
    # 🐙 GITHUB SUMMARY
    # ---------------------------
    github_summary = None
    if "github_supporting" in d:
        github_summary = {
            "summary": github.get("github_profile_summary"),
            "consistency_score": github.get("consistency_score"),
            "supported_skills": github.get("supported_skills", []),
            "unsupported_skills": github.get("unsupported_skills", [])
        }

    # ---------------------------
    # FINAL OUTPUT
    # ---------------------------
    return {
        "total_score": score,
        "confident_insights": list(set(confident_insights)),
        "ambiguity_insights": list(set(ambiguity_insights)),
        "high_risk": list(set(high_risk)),
        "questions": list(set(questions)),
        "github_summary": github_summary
    }

if __name__ == "__main__":
    with open("analyzer/services/ai_response.json", "r") as file:
        data = json.load(file)  # parses JSON → dict
    result = generate_resume_insights(data)

    print(json.dumps(result, indent=4))