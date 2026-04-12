from django.urls import path
from analyzer.views.health_check_view import health_check
from analyzer.views.github_summary_view import GithubAnalysisView
from analyzer.views.upload_cv_view import UploadCVView
from analyzer.views.analyze_view import AnalyzeView
from analyzer.views.ai_analysis_view import AiAnalysisView

urlpatterns = [
   path('health/', health_check),
   path('github/', GithubAnalysisView.as_view()),
   path('upload-cv/', UploadCVView.as_view()),
   path('analyze/', AnalyzeView.as_view()),
   path('ai-analysis/', AiAnalysisView.as_view()),
]
