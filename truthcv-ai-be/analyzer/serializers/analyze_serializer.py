import re
from rest_framework import serializers

class AnalyzeSerializer(serializers.Serializer):
    file = serializers.FileField(
        required=True,
        error_messages={
            "required": "No file uploaded. Use 'file' field.",
            "empty": "No file uploaded. Use 'file' field."
        }
    )
    github_link = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate_file(self, value):
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are supported.")
        return value

    def validate_github_link(self, value):
        if not value:
            return value
            
        # Try to extract username if a full url is provided
        match = re.search(r"(?:https?://)?(?:www\.)?github\.com/([^/\s]+)", value.strip())
        if match:
            return match.group(1)
            
        # Or assume the value is the username itself
        return value.strip()
