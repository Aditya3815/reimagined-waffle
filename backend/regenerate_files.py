"""
Script to regenerate all deleted files for the doctor-patient-health system
Run with: python regenerate_files.py
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

def create_file(filepath, content):
    """Create a file with given content"""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {filepath}")

# Update settings.py
settings_content = """
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "doctors",
    "patients",
    "health_goals",
]

# Add to MIDDLEWARE (after SecurityMiddleware)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # Add this
    # ... rest of middleware
]

# Add at the end
CORS_ALLOW_ALL_ORIGINS = True  # For development
"""

# Update urls.py
urls_content = """from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/doctors/", include("doctors.urls")),
    path("api/patients/", include("patients.urls")),
    path("api/health-goals/", include("health_goals.urls")),
]
"""

print("\\n" + "="*60)
print("REGENERATING ALL SYSTEM FILES")
print("="*60 + "\\n")

print("Please manually update backend/settings.py with:")
print(settings_content)
print("\\nPlease manually update backend/urls.py with:")
print(urls_content)

print("\\n" + "="*60)
print("Run the following commands to regenerate app files:")
print("="*60)
print("1. Ensure apps exist: python manage.py startapp doctors")
print("2. Ensure apps exist: python manage.py startapp patients")
print("3. Ensure apps exist: python manage.py startapp health_goals")
print("\\nThen I'll regenerate all the code files...")
