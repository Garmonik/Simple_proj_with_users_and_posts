from django.urls import path
import accounts.views

urlpatterns = [
    path('profile/update/', accounts.views.UserProfileUpdateView.as_view()),
    path('profile/<int:pk>/', accounts.views.UserProfileView.as_view()),
    path('profile/', accounts.views.UserProfileListView.as_view()),
    path('profile/my_profile/', accounts.views.MyUserProfileView.as_view()),
    path('profile/my_profile/deactivate/', accounts.views.UserProfileDeleteView.as_view()),


]
