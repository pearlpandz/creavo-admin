# signals.py

import os
import requests
from django.conf import settings
from django.dispatch import receiver
from .models.event import EventMedia
from .models.media import Media
from django.db.models.signals import pre_save, post_save, post_delete

def delete_image_from_nodejs(image_url):
    if image_url:
        filename = image_url.split('/')[-1]
        try:
            delete_url = f'{settings.MEDIA_SERVER_URL}/upload/delete/media/{filename}'
            response = requests.delete(delete_url)
            if response.status_code == 200:
                print(f"Deleted {filename} from Node.js")
            else:
                print(f"Failed to delete {filename} from Node.js: {response.status_code}")
        except Exception as e:
            print(f"Error deleting {filename} from Node.js: {e}")

@receiver(pre_save, sender=Media)
@receiver(pre_save, sender=EventMedia)
def track_media_change(sender, instance, **kwargs):
    if instance.pk:
        old_instance = sender.objects.filter(pk=instance.pk).first()
        if old_instance and old_instance.media != instance.media:
            instance._media_changed = True
      
@receiver(post_save, sender=Media)
@receiver(post_save, sender=EventMedia)
def upload_to_nodejs_after_save(sender, instance, created, **kwargs):
    if instance.media: 
        media_path = instance.media.path
        
        if created or getattr(instance, '_media_changed', False):
            instance._media_changed = False
            try:
                url = f'{settings.MEDIA_SERVER_URL}/upload/media'
                print('url', url)

                # Open the file in a context manager so it's properly closed after use
                with open(media_path, 'rb') as f:
                    files = {'media': f}
                    response = requests.post(url, files=files)

                print('response.status_code', response.status_code)
                if response.status_code == 200:
                    old_image = instance.image
                    instance.image = response.json().get('url')
                    instance.save(update_fields=['image'])
                    
                    # Now that file is closed, it’s safe to delete
                    os.remove(instance.media.path) 
                    print(f"Deleted local file: {media_path}")
                    delete_image_from_nodejs(old_image)

            except Exception as e:
                print(f"Upload failed: {e}")

@receiver(post_delete, sender=Media)
@receiver(post_delete, sender=EventMedia)
def delete_from_nodejs_after_delete(sender, instance, **kwargs):
    delete_image_from_nodejs(instance.image)