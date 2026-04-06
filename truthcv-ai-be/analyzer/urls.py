from django.urls import path
from analyzer.views.health_check_view import health_check
from analyzer.views.github_summary_view import github_analysis

urlpatterns = [
   path('health/', health_check),
   path('github/', github_analysis)
]
