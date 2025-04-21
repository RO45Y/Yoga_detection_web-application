from django.db import models
from django.contrib.auth.models import User

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
#     age = models.PositiveIntegerField(blank=True, null=True)

#     GENDER_CHOICES = [
#         ("Male", "Male"),
#         ("Female", "Female"),
#         ("Other", "Other"),
#     ]
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)

#     LEVEL_CHOICES = [
#         ("Beginner", "Beginner"),
#         ("Moderate", "Moderate"),
#         ("Advanced", "Advanced"),
#     ]
#     level = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True)

#     injury_history = models.TextField(blank=True, null=True)
#     weight = models.FloatField(blank=True, null=True)

#     def __str__(self):
#         return self.user.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.PositiveIntegerField(blank=True, null=True)

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)

    LEVEL_CHOICES = [
        ("Beginner", "Beginner"),
        ("Moderate", "Moderate"),
        ("Advanced", "Advanced"),
    ]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True)

    injury_history = models.TextField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)

    # Change the reference to a string
    recommended_poses = models.ManyToManyField('YogaPose', blank=True, related_name="recommended_for_users")

    def __str__(self):
        return self.user.username



class YogaPose(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=[
        ("Beginner", "Beginner"),
        ("Moderate", "Moderate"),
        ("Advanced", "Advanced")
    ])
    reference_image = models.ImageField(upload_to='poses/')
    reference_landmarks = models.JSONField(default=list, blank=True)  # Will store x, y, z, visibility

    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    tags = models.JSONField(default=list, blank=True)
    restricted_for_injuries = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save image first so file exists on disk

        if self.reference_image and not self.reference_landmarks:
            try:
                import mediapipe as mp
                import cv2
                import numpy as np
                from PIL import Image

                mp_pose = mp.solutions.pose
                pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

                # Load image using PIL and convert to OpenCV format
                image_path = self.reference_image.path
                image = Image.open(image_path).convert('RGB')
                image_np = np.array(image)
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

                # Run MediaPipe pose detection
                results = pose.process(image_np)

                if results.pose_landmarks:
                    landmarks = [
                        {
                            'x': lm.x,
                            'y': lm.y,
                            'z': lm.z,
                            'visibility': lm.visibility
                        }
                        for lm in results.pose_landmarks.landmark
                    ]
                    self.reference_landmarks = landmarks
                    super().save(update_fields=['reference_landmarks'])  # Save only the updated field

            except Exception as e:
                print("Error extracting pose landmarks:", e)
