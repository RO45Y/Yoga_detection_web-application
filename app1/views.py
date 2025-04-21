# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings

# Channels for WebSocket communication
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Standard libraries
import json
import base64
import numpy as np
import cv2
import time
from pathlib import Path

# App models
from .models import UserProfile, YogaPose

# Utilities
from .utils import get_landmarks_from_image, compare_landmarks_with_reference, draw_landmarks

# ------------------------- User Authentication Views -------------------------

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("Username or password is incorrect!")
    return render(request, 'login.html')

def registerpage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        weight = request.POST.get('weight')
        level = request.POST.get('level')
        injury_history = request.POST.get('injury_history')

        if pass1 != pass2:
            return HttpResponse("Passwords do not match!")

        user = User.objects.create_user(username=uname, email=email, password=pass1)
        UserProfile.objects.create(
            user=user, age=age, gender=gender, weight=weight, level=level, injury_history=injury_history
        )
        return redirect('login')

    return render(request, 'register.html')

def logoutpage(request):
    logout(request)
    return redirect('home')

# ------------------------- Page Rendering Views -------------------------

def homepage(request):
    return render(request, "index2.html")

@login_required(login_url='login')
def Homepage(request):
    return render(request, 'inside.html')

@login_required(login_url='login')
def dashboard(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    poses = YogaPose.objects.filter(level=user_profile.level)
    return render(request, 'dashboard.html', {'poses': poses})

# @login_required
# def dashboard(request):
#     # This line will ensure the UserProfile exists
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)

#     # Now you can safely use user_profile
#     poses = user_profile.recommended_poses.all()[:10]  # Or however you fetch poses

#     return render(request, 'dashboard.html', {'poses': poses})


def try_pose(request, pose_name):
    pose = YogaPose.objects.filter(name=pose_name).first()
    return render(request, 'try_pose.html', {'pose': pose})

# ------------------------- Pose Data API -------------------------

def get(request, pose_name):
    if request.method == "GET":
        pose = get_object_or_404(YogaPose, name=pose_name)
        return JsonResponse({"landmarks": pose.reference_landmarks})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

# ------------------------- Pose Detection API -------------------------

def get_reference_landmarks(pose_name):
    try:
        yoga_pose = YogaPose.objects.get(name=pose_name)
        return yoga_pose.reference_landmarks
    except YogaPose.DoesNotExist:
        return None

@csrf_exempt
def pose_detection(request, pose_name):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            image_data = data.get('image')

            if not image_data:
                return JsonResponse({'error': 'Image data is required'}, status=400)

            reference_landmarks = get_reference_landmarks(pose_name)
            if not reference_landmarks:
                return JsonResponse({'error': 'Pose not found'}, status=404)

            nparr = np.frombuffer(base64.b64decode(image_data.split(',')[1]), np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            detected_landmarks = get_landmarks_from_image(frame)
            if not detected_landmarks:
                return JsonResponse({'error': 'No landmarks detected'}, status=400)

            pose_status = compare_landmarks_with_reference(detected_landmarks, reference_landmarks)

            frame_with_landmarks = draw_landmarks(frame, detected_landmarks)
            ret, jpeg = cv2.imencode('.jpg', frame_with_landmarks)
            img_base64 = base64.b64encode(jpeg.tobytes()).decode('utf-8')

            return JsonResponse({
                'poseStatus': pose_status,
                'landmarkImage': img_base64
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

# ------------------------- Unused / Commented Experimental Code -------------------------

# import mediapipe as mp
# import pygame
# BASE_DIR = Path(settings.BASE_DIR)
# correct_pose_sound = pygame.mixer.Sound(str(BASE_DIR / "success.mp3"))

# mp_pose = mp.solutions.pose
# pose_model = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# def play_correct_pose_sound():
#     print("✅ Correct pose detected! Playing sound...")

# def pose_detection_view(request, pose_name):
#     return render(request, "pose_detection.html", {"pose_name": pose_name})

# def compare_landmarks(reference_landmarks, current_landmarks):
#     if len(reference_landmarks) != len(current_landmarks):
#         return 0.0
#     threshold = 0.35
#     matching_keypoints = sum(
#         np.linalg.norm([ref["x"] - cur["x"], ref["y"] - cur["y"], ref["z"] - cur["z"]])**2 < threshold**2
#         for ref, cur in zip(reference_landmarks, current_landmarks)
#     )
#     return matching_keypoints / len(reference_landmarks)
