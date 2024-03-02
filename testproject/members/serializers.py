from rest_framework import serializers
from .models import Product, Lesson, StudentProductAccess, Group

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title']

class ProductSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Product
        fields = ['id', 'name', 'lesson_count', 'start_date_time', 'price']

class AccessibleProductSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'lessons']

    def to_representation(self, instance):
        user = self.context['request'].user

        student_access = StudentProductAccess.objects.filter(student=user, product=instance).first()
        if student_access and student_access.has_access:
            data = super().to_representation(instance)
            return data

class ProductStatsSerializer(serializers.ModelSerializer):
    total_students = serializers.SerializerMethodField()
    group_completion_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'total_students', 'group_completion_percentage']

    def get_total_students(self, obj):
        total_students = StudentProductAccess.objects.filter(product=obj, has_access=True).count()
        return total_students

    def get_group_fill_rate(self, obj):
        if obj.max_group_size > 0:
            fill_rate = (obj.total_students_with_access / (obj.max_group_size * obj.group_count)) * 100
            return fill_rate
        return 0

    def get_group_completion_percentage(self, obj):
        groups = Group.objects.filter(product=obj)
        group_users_count = [group.users.count() for group in groups]
        stat = []
        if len(group_users_count) != 0:
            for i in range(len(group_users_count)):
                stat.append((group_users_count[i] / obj.max_group_size) * 100)
        else:
            return 0
        group_completion_percentage = sum(stat) / len(stat)
        return f'{group_completion_percentage:.2f}%'