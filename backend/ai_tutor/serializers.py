from rest_framework import serializers


class AITutorRequestSerializer(serializers.Serializer):
    problem = serializers.CharField(max_length=20000)
    code = serializers.CharField(max_length=20000, allow_blank=True)
    error_log = serializers.CharField(max_length=8000, allow_blank=True, required=False)

