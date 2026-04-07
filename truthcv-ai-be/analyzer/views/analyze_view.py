from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from analyzer.services.cv_parser_service import parse_pdf, build_cv_data
from analyzer.services.github_service import get_github_data
from analyzer.services.insight_service import generate_insights
from analyzer.serializers.analyze_serializer import AnalyzeSerializer


class AnalyzeView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = AnalyzeSerializer(data=request.data)
        
        if not serializer.is_valid():
            # Get first error message to retain previous generic error behaviour shapes
            error_field = next(iter(serializer.errors))
            error_msg = serializer.errors[error_field][0]
            return Response(
                {"error": error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        file_obj = serializer.validated_data["file"]
        username = serializer.validated_data.get("github_link")

        # 1. Process CV
        try:
            text = parse_pdf(file_obj)
            parsed_data = build_cv_data(text)
        except Exception as e:
            return Response(
                {"error": f"Failed to parse PDF: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        response_data = {
            "cv_data": parsed_data
        }

        # 2. Process GitHub (optional)
        if username:
            github_data = get_github_data(username)
            
            # Handle github service errors (e.g. rate limit, bad username)
            if isinstance(github_data, dict) and "error" in github_data:
                return Response(
                    {"error": f"GitHub error: {github_data['error']}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            insights = generate_insights(github_data)
            
            response_data["github_data"] = github_data
            response_data["insights"] = insights
            
        return Response({
            "message": "Analysis completed successfully",
            "data": response_data
        }, status=status.HTTP_200_OK)
