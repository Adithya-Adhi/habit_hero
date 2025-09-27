
from rest_framework import serializers
from .models import Habit, CheckIn, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = "__all__"

class HabitSerializer(serializers.ModelSerializer):
    checkins = CheckInSerializer(many=True, read_only=True)

    class Meta:
        model = Habit
        fields = "__all__"
