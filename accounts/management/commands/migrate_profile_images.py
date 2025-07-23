import os
import django
from django.core.management.base import BaseCommand
from django.conf import settings
from cloudinary.uploader import upload
import cloudinary

from accounts.models import Profile  # Adjust if needed

# Set environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secretSpark.settings')

# Setup Django
django.setup()

# Configure Cloudinary SDK with environment variables
from decouple import config

cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET'),
    secure=True
)

class Command(BaseCommand):
    help = 'Migrate local profile pictures to Cloudinary'

    def handle(self, *args, **kwargs):
        profile_pictures_dir = os.path.join(settings.MEDIA_ROOT, 'profile-pictures')
        migrated_count = 0

        for profile in Profile.objects.all():
            if profile.profile_picture:
                pic_str = str(profile.profile_picture)

                # Skip if already a Cloudinary public ID (no extension and no local path)
                if not pic_str.startswith('profile-pictures/'):
                    print(f"Profile {profile.id} profile_picture seems already uploaded: {pic_str}")
                    continue

                base_name = pic_str.split('/')[-1]  # filename without extension

                possible_extensions = ['.jpeg', '.jpg', '.png']
                found_file = None
                for ext in possible_extensions:
                    candidate = os.path.join(profile_pictures_dir, base_name + ext)
                    if os.path.exists(candidate):
                        found_file = candidate
                        break

                if found_file:
                    print(f"Uploading {found_file}")
                    result = upload(found_file, folder='profile-pictures')
                    profile.profile_picture = result['public_id']
                    profile.save()
                    migrated_count += 1
                else:
                    print(f"❌ File not found for profile picture base: {base_name}")
            else:
                print(f"Profile {profile.id} has no profile_picture")

        print(f"✅ Migration complete. Total profile pictures uploaded: {migrated_count}")
