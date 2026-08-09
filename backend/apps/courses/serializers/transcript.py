from rest_framework import serializers


class TranscriptCourseSerializer(serializers.Serializer):
    course_code = serializers.CharField()
    course_title = serializers.CharField()
    credit_hours = serializers.IntegerField()
    letter_grade = serializers.CharField()
    grade_point = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
    )


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

    courses = TranscriptCourseSerializer(
        many=True,
    )