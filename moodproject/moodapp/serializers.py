from django.contrib.auth.models import User, Group
from moodapp.models import UserMood, UserStatistics
from rest_framework import serializers

class UserMoodSerializer(serializers.ModelSerializer):
    streak = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserMood
        fields = ['mood', 'created', 'streak', 'user'] 

class UserStatisticsSerializer(serializers.ModelSerializer):
    longest_streak = serializers.ReadOnlyField()
    percentile = serializers.ReadOnlyField()
    class Meta:
        model = UserStatistics
        fields = ['longest_streak', 'percentile']

class UserSerializer(serializers.ModelSerializer):
    usermood_set = UserMoodSerializer(many=True)
    percentile = serializers.ReadOnlyField()
    longest_streak = serializers.ReadOnlyField(source='userstatistics.longest_streak')

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'usermood_set',  'percentile', 'longest_streak']




