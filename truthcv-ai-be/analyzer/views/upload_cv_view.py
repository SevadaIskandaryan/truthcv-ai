from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from analyzer.services.cv_parser_service import parse_pdf, build_cv_data
from analyzer.serializers.upload_cv_serializer import UploadCVSerializer


class UploadCVView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):

        serializer = UploadCVSerializer(data=request.data)
        
        if not serializer.is_valid():
            # Keep previous error shape for backwards compatibility
            error_msg = serializer.errors.get("file", ["Invalid request"])[0]
            return Response(
                {"error": error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        file_obj = serializer.validated_data["file"]

        try:
            text = parse_pdf(file_obj)
            parsed_data = build_cv_data(text)

            return Response({
                "message": "CV parsed successfully",
                "data": parsed_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to parse PDF: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )