from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from analyzer.services.cv_parser_service import parse_pdf, build_cv_data


class UploadCVView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):

        file_obj = request.FILES.get("file")

        if not file_obj:
            return Response(
                {"error": "No file uploaded. Use 'file' field."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not file_obj.name.lower().endswith(".pdf"):
            return Response(
                {"error": "Only PDF files are supported."},
                status=status.HTTP_400_BAD_REQUEST
            )

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