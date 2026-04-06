
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
