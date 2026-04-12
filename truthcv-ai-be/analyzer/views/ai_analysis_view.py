from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from analyzer.services.ai_analysis import analyze_resume


class AiAnalysisView(APIView):
    def post(self, request):
        # We expect JSON input with 'raw_resume_text' and 'optional_github_data'
        raw_resume_text = request.data.get("raw_resume_text")
        optional_github_data = request.data.get("optional_github_data", {})

        if not raw_resume_text:
            return Response(
                {"error": "raw_resume_text is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        resume_data = {
            "raw_resume_text": raw_resume_text,
            "optional_github_data": optional_github_data
        }

        try:
            analysis_result = analyze_resume(resume_data)
        except ValueError as e:
            # specifically for missing open AI API Key
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to perform AI analysis: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            "message": "AI Analysis completed successfully",
            "data": analysis_result
        }, status=status.HTTP_200_OK)
