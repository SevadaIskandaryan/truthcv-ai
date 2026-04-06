from rest_framework.decorators import api_view
from rest_framework.response import Response
from analyzer.services.github_service import get_github_data
from analyzer.services.insight_service import generate_insights



@api_view(['GET'])
def github_analysis(request):
   username = request.GET.get('username')

   if not username:
       return Response({"error": "username required"}, status=400)

   github_data = get_github_data(username)
   insights = generate_insights(github_data)

   return Response({
       "github_data": github_data,
       "insights": insights
   })

