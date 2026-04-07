from rest_framework import serializers

class GithubAnalysisSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        error_messages={
            "required": "username required",
            "blank": "username required"
        }
    )
