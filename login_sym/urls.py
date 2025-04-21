from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),  # ✅ Fix: Added admin path
    path("", views.homepage, name="home"),
    path("login/", views.loginpage, name="login"),
    path("register/", views.registerpage, name="signup"),
    path("logout/", views.logoutpage, name="logout"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    path("inside/", views.Homepage, name="inside"),

    # Pose Detection
    

    path("get-landmarks/<str:pose_name>/", views.get, name="get_landmarks"),
    # path("process-pose/", views.process_pose, name="process_pose"),
    path('pose_detection/<str:pose_name>/', views.pose_detection, name='pose_detection'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
