from analyzer.services.github_service import get_github_data
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def github_analysis(request):
   username = request.GET.get('username')

   if not username:
       return Response({"error": "username required"}, status=400)

   data = get_github_data(username)
   return Response(data)
