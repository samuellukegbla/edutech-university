from rest_framework import serializers

from .models import (
    Faculty,
    Department,
    Programme,
)

from rest_framework import serializers

from apps.academics.models import (
    Curriculum,
    CurriculumCourse,
)

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class ProgrammeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programme
        fields = "__all__"


class CurriculumSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = Curriculum
        fields = "__all__"


class CurriculumCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumCourse
        fields = "__all__"


class ProgrammeStudyPlanSerializer(serializers.Serializer):
    programme = serializers.DictField()
    study_plan = serializers.ListField()