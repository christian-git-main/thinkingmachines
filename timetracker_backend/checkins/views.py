# views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import CheckIn
from django.contrib.auth.models import User
from .serializers import CheckInSerializer, UserSerializer,UserLoginSerializer,CheckInSerializerNew
from rest_framework.views import APIView
from django.db.models import Sum
from django.utils import timezone
class CheckInListCreateAPIView(generics.ListCreateAPIView):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for creating/checking check-ins

    # Override create method to associate check-ins with authenticated user
    def create(self, request, *args, **kwargs):
        # Add the authenticated user to the check-in data before creating
        checkin_data = request.data.copy()
        checkin_data['user'] = request.user.id  # Add the authenticated user ID to the check-in data
        serializer = self.get_serializer(data=checkin_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        # Retrieve check-in instance
        checkin_instance = self.get_object()
        # Check if the user is authorized to delete the check-in
        if request.user == checkin_instance.user:
            checkin_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'You are not authorized to delete this check-in'}, status=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        # Filter queryset to only show check-ins of the authenticated user
        queryset = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserLoginAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CheckAdminStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        is_admin = user.is_staff
        return Response({'is_admin': is_admin})



class CheckInListAPIView(generics.ListAPIView):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializerNew
    # permission_classes = [IsAdminUser]

class UsersWith45HoursAPIView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        # Get start and end dates from query parameters
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date is None or end_date is None:
            return Response({'error': 'Please provide both start_date and end_date as query parameters.'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert start_date and end_date to datetime objects
        try:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Please provide dates in YYYY-MM-DD format.'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter check-ins within the specified date range and annotate the total hours for each user
        queryset = CheckIn.objects.filter(
            created_at__range=[start_date, end_date]
        ).values('user').annotate(total_hours=Sum('hours'))

        # Filter users with a total of 45 hours in the given date range
        users_with_45_hours = []
        for item in queryset:
            if item['total_hours'] >= 45:
                user = User.objects.get(pk=item['user'])
                users_with_45_hours.append(user)
        print("users_with_45_hours",users_with_45_hours)
        return users_with_45_hours