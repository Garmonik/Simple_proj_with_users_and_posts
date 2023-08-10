from django.urls import path, include

import facecontrol.views

urlpatterns = [
    path('register/', facecontrol.views.RegisterView.as_view()),
    path('verification_email/', facecontrol.views.VerificationView.as_view()),
    path('password_recovery/', facecontrol.views.PasswordRecoveryView.as_view()),
    path('login/', facecontrol.views.LoginView.as_view()),
    path('change_password/', facecontrol.views.ChangePasswordView.as_view()),
    path('refresh_token/', facecontrol.views.RefreshTokenView.as_view()),
]
