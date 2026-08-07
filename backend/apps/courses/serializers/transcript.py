from rest_framework import serializers


class TranscriptSerializer(serializers.Serializer):
    academic_session = serializers.CharField()
    semester = serializers.CharField()
    semester_gpa = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
    )
    cumulative_gpa = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
    )
    standing = serializers.CharField()
    courses = serializers.ListField()