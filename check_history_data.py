
import os
import django
import sys
from django.db.models import Count

# Setup Django environment
sys.path.append('e:/github/blood_Group/New folder/blood_deatction')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blood_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from blood_app.models import BloodAnalysis

User = get_user_model()

print("--- Scan Ownership Analysis ---")
# Check scans with NO user
orphaned_scans = BloodAnalysis.objects.filter(user__isnull=True).count()
print(f"Scans with NO user assigned: {orphaned_scans}")

# Check scans by user
user_counts = BloodAnalysis.objects.values('user__username', 'user__id').annotate(count=Count('id')).order_by('-count')

for entry in user_counts:
    print(f"User: {entry['user__username']} (ID: {entry['user__id']}) - Scans: {entry['count']}")

print("-" * 30)
# Check total
print(f"Total Scans: {BloodAnalysis.objects.count()}")
