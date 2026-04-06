from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from analyzer.services.github_service import get_github_data
from analyzer.services.insight_service import generate_insights


class GithubAnalysisView(APIView):

    def get(self, request):
        username = request.query_params.get("username")

        if not username:
            return Response(
                {"error": "username required"},
                status=status.HTTP_400_BAD_REQUEST
            )

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