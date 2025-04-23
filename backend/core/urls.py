from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ResumeUploadView, ResumeAnalysisView
from .views_auth import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('resumes/', ResumeUploadView.as_view(), name='resume-upload'),
    path('resumes/<int:resume_id>/', ResumeUploadView.as_view(), name='resume-delete'),
    path('analysis/', ResumeAnalysisView.as_view(), name='resume-analysis'),
]
