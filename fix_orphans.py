
import os
import django
import sys

# Setup Django environment
sys.path.append('e:/github/blood_Group/New folder/blood_deatction')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blood_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from blood_app.models import BloodAnalysis

User = get_user_model()
# Get the first user (likely the admin/current user since there are few users)
# Ideally we'd ask which user, but assuming the active tester is the intended owner for dev purposes.
# Let's find the user 'ismaildevoops@gmail.com' or similar if possible, otherwise pick the first superuser or active user.

# For safety, let's just pick the first user found or a specific known username if we knew it.
# Based on previous output: shalika0801@gmail.com (ID: 1)
target_user = User.objects.first()

if target_user:
    print(f"Assigning orphaned scans to user: {target_user.username} (ID: {target_user.id})")
    updated_count = BloodAnalysis.objects.filter(user__isnull=True).update(user=target_user)
    print(f"Successfully updated {updated_count} records.")
else:
    print("No user found to assign records to.")
