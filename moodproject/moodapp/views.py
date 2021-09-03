from datetime import datetime, date, timedelta
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from moodapp.models import UserMood, UserStatistics
from moodapp.serializers import UserMoodSerializer, UserSerializer, UserStatisticsSerializer
from statistics import quantiles
from scipy import stats
from django.utils.dateparse import parse_datetime

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class UserStatisticsViewSet(generics.ListAPIView):
    serializer_class = UserStatisticsSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserMoodViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    API endpoint that allows user moods to be viewed or edited.
    """
    
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserMood.objects.all()
    serializer_class = UserMoodSerializer


    def get(self, request, format=None):
        """
        GET all. Only return a list of all the moods
        for the currently authenticated user.
        """
        # Get the user's statistics
        current_user = User.objects.get(id=self.request.user.pk)
        # TODO: users that haven't submitted any moods have no statistics, therefore no longest_streak to use in percentile calc
        all_user_streaks = list(UserStatistics.objects.values_list('longest_streak', flat=True).order_by('longest_streak'))

        try:
            percentile = stats.percentileofscore(all_user_streaks, current_user.userstatistics.longest_streak) #, 'weak'
            if percentile >= 50:
                current_user.percentile = percentile
        except UserStatistics.DoesNotExist:
            pass

        # Return this user, with associated moods nested
        serializer = UserSerializer(instance=current_user, context={'request': request})

        return Response(serializer.data)

    def post(self, request, format=None):
        """
        POST the submitted user mood
        """
        #serializer_class = UserMoodSerializer
        serializer = UserMoodSerializer(data=request.data)

        if serializer.is_valid():

            # Get this user's last submitted mood to determine the current streak
            new_streak = 1
            last_mood = UserMood.objects.filter(user=self.request.user).last()

            # Check if there is at least one mood submitted yesterday 
            # TODO: base the previous day on users time zone instead of server timezone
            # TODO: how to handle streak recalculation is user wants to delete a mood
            thismooddate = serializer.validated_data['created']
            if last_mood == None:
                pass
            # If another submission today, then don't increment the streak
            elif last_mood.created.date() == thismooddate.date(): # date.today():
                new_streak = last_mood.streak
            # If new submission one day later, increment the streak
            elif abs((last_mood.created.date() - thismooddate.date()).days) == 1 :
                new_streak = last_mood.streak + 1
            
            
            # Get the user's statistics
            current_user = User.objects.get(id=self.request.user.pk)
            
            try:
                # If this is the longest streak, then update the user statistics
                if new_streak > current_user.userstatistics.longest_streak:
                    current_user.userstatistics.longest_streak = new_streak
                    #current_user.update()
                    current_user.userstatistics.save()
            except UserStatistics.DoesNotExist:
                # No statistics object yet, create
                newstat = UserStatistics.objects.create(user=current_user, longest_streak=new_streak)
                newstat.save()

            
            # Finally, save the mood
            serializer.save(user=self.request.user, streak=new_streak)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)