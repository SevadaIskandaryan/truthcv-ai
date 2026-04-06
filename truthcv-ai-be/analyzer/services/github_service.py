import requests

def get_github_data(username):
   url = f"https://api.github.com/users/{username}/repos"
   response = requests.get(url)

   if response.status_code != 200:
       return {"error": "User not found"}

   repos = response.json()

   repo_count = len(repos)
   languages = {}

   for repo in repos:
       lang = repo.get("language")
       if lang:
           languages[lang] = languages.get(lang, 0) + 1

   return {
       "repo_count": repo_count,
       "languages": languages,
       "recent_repo": repos[0]["name"] if repos else None
   }
