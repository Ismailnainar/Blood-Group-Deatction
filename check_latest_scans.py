
import os
import django
import sys

# Setup Django environment
sys.path.append('e:/github/blood_Group/New folder/blood_deatction')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blood_project.settings')
django.setup()

from blood_app.models import BloodAnalysis

print("--- Latest 5 Scan Records ---")
latest_scans = BloodAnalysis.objects.all().order_by('-created_at')[:5]

for scan in latest_scans:
    user_str = f"{scan.user.username} (ID: {scan.user.id})" if scan.user else "NONE"
    print(f"ID: {scan.id} | Date: {scan.created_at} | User: {user_str}")

print("-" * 30)
