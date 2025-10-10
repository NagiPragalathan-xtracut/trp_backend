from rest_framework import serializers
from .models.department_model import DepartmentStatistics


class DepartmentStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentStatistics
        fields = ['id', 'department', 'name', 'number', 'suffix', 'description', 'featured', 'display_order']
        read_only_fields = ['id']
