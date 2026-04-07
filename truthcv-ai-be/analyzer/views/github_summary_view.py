from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from analyzer.services.github_service import get_github_data
from analyzer.services.insight_service import generate_insights
from analyzer.serializers.github_analysis_serializer import GithubAnalysisSerializer


class GithubAnalysisView(APIView):

    def get(self, request):
        serializer = GithubAnalysisSerializer(data=request.query_params)
        
        if not serializer.is_valid():
            # Keep previous error shape for backwards compatibility with frontend
            error_msg = serializer.errors.get("username", ["Invalid request"])[0]
            return Response(
                {"error": error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        username = serializer.validated_data["username"]

        github_data = get_github_data(username)

        # Handle service errors
        if "error" in github_data:
            return Response(
                github_data,
                status=status.HTTP_400_BAD_REQUEST
            )

        insights = generate_insights(github_data)

        return Response({
            "github_data": github_data,
            "insights": insights
        }, status=status.HTTP_200_OK)