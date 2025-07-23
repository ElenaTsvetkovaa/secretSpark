import os
import django
from django.core.management.base import BaseCommand
from django.conf import settings
from cloudinary.uploader import upload
import cloudinary

from articles.models import Article, Section

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
    help = 'Migrate local Article and Section images to Cloudinary'

    def handle(self, *args, **kwargs):
        section_images_dir = os.path.join(settings.MEDIA_ROOT, 'section-images')
        migrated_count = 0

        # Migrate Article banners
        for article in Article.objects.all():
            if article.banner:
                banner_str = str(article.banner)

                # Skip if already uploaded (not a local path)
                if not banner_str.startswith('section-images/'):
                    print(f"Article {article.id} banner seems already uploaded: {banner_str}")
                    continue

                base_name = os.path.splitext(os.path.basename(banner_str))[0]  # remove extension

                possible_extensions = ['.jpeg', '.jpg', '.png']
                found_file = None
                for ext in possible_extensions:
                    candidate = os.path.join(section_images_dir, base_name + ext)
                    if os.path.exists(candidate):
                        found_file = candidate
                        break

                if found_file:
                    print(f"Uploading Article.banner: {found_file}")
                    result = upload(found_file, folder='section-images')
                    article.banner = result['public_id']
                    article.save()
                    migrated_count += 1
                else:
                    print(f"❌ File not found for Article.banner base: {base_name}")
            else:
                print(f"Article {article.id} has no banner")

        # Migrate Section images
        for section in Section.objects.all():
            if section.image:
                image_str = str(section.image)

                # Skip if already uploaded (not a local path)
                if not image_str.startswith('section-images/'):
                    print(f"Section {section.id} image seems already uploaded: {image_str}")
                    continue

                base_name = os.path.splitext(os.path.basename(image_str))[0]  # remove extension

                possible_extensions = ['.jpeg', '.jpg', '.png', '.webp']
                found_file = None
                for ext in possible_extensions:
                    candidate = os.path.join(section_images_dir, base_name + ext)
                    if os.path.exists(candidate):
                        found_file = candidate
                        break

                if found_file:
                    print(f"Uploading Section.image: {found_file}")
                    result = upload(found_file, folder='section-images')
                    section.image = result['public_id']
                    section.save()
                    migrated_count += 1
                else:
                    print(f"❌ File not found for Section.image base: {base_name}")
            else:
                print(f"Section {section.id} has no image")

        print(f"✅ Migration complete. Total images uploaded: {migrated_count}")
