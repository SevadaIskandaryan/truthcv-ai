from rest_framework import serializers

class UploadCVSerializer(serializers.Serializer):
    file = serializers.FileField(
        required=True,
        error_messages={
            "required": "No file uploaded. Use 'file' field.",
            "empty": "No file uploaded. Use 'file' field."
        }
    )

    def validate_file(self, value):
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are supported.")
        return value
