from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import User, CompanyDetails, Product, Political, Supporters, Party
from django.conf import settings
import requests
import os
from django.utils import timezone
from accounts.models.user import User
from django.contrib.auth.signals import user_logged_in


@receiver(user_logged_in)
def update_last_login(sender, user, request, **kwargs):
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])

def delete_media_from_service(image_url):
    if image_url:
        print('issue???', image_url)
        filename = image_url.split('/')[-1]
        try:
            delete_url = f'{settings.MEDIA_SERVER_URL}/upload/delete/userdetails/{filename}'

            response = requests.delete(delete_url)
            if response.status_code == 200:
                print(f"Deleted {filename} from Node.js")
            else:
                print(f"Failed to delete {filename} from Node.js: {response.status_code}")
        except Exception as e:
            print(f"Error deleting {filename} from Node.js: {e}")


def upload_media_to_service(sender, instance, created, **kwargs):
    if instance.media: 
        media_path = instance.media.path
        
        if created or getattr(instance, '_media_changed', False):
            instance._media_changed = False
            try:
                url = f'{settings.MEDIA_SERVER_URL}/upload/userdetails'
                print('url', url)

                # Open the file in a context manager so it's properly closed after use
                with open(media_path, 'rb') as f:
                    files = {'userdetails': f}
                    response = requests.post(url, files=files)

                print('response.status_code', response.status_code)
                if response.status_code == 200:
                    old_image = instance.image
                    instance.image = response.json().get('url')
                    instance.save(update_fields=['image'])
                    
                    # Now that file is closed, it’s safe to delete
                    os.remove(instance.media.path) 
                    print(f"Deleted local file: {media_path}")
                    delete_media_from_service(old_image)

            except Exception as e:
                print(f"Upload failed: {e}")

@receiver(pre_save, sender=CompanyDetails)
@receiver(pre_save, sender=Product)
@receiver(pre_save, sender=Political)
@receiver(pre_save, sender=Supporters)
@receiver(pre_save, sender=Party)
def track_media_change(sender, instance, **kwargs):
    if instance.pk:
        old_instance = sender.objects.filter(pk=instance.pk).first()
        if old_instance and old_instance.media != instance.media:
            instance._media_changed = True

# CompanyDetails image upload/delete
@receiver(post_save, sender=CompanyDetails)
def upload_companydetails_logo(sender, instance, created, **kwargs):
    if instance.media:
        upload_media_to_service(sender, instance, created, **kwargs)

@receiver(post_delete, sender=CompanyDetails)
def delete_companydetails_logo(sender, instance, **kwargs):
    if instance.image:
        delete_media_from_service(instance.image)

# Product image upload/delete
@receiver(post_save, sender=Product)
def upload_product_media(sender, instance, created, **kwargs):
    if instance.media:
        upload_media_to_service(sender, instance, created, **kwargs)

@receiver(post_delete, sender=Product)
def delete_product_media(sender, instance, **kwargs):
    if instance.image:
        delete_media_from_service(instance.image)

# Political leader image upload/delete
@receiver(post_save, sender=Political)
def upload_political_leader_file(sender, instance, created, **kwargs):
    if instance.media:
        upload_media_to_service(sender, instance, created, **kwargs)

@receiver(post_delete, sender=Political)
def delete_political_leader_file(sender, instance, **kwargs):
    if instance.image:
        delete_media_from_service(instance.image)

# Supporters image upload/delete
@receiver(post_save, sender=Supporters)
@receiver(post_save, sender=Party)
def upload_supporter_media(sender, instance, created, **kwargs):
    if instance.media:
        upload_media_to_service(sender, instance, created, **kwargs)

@receiver(post_delete, sender=Supporters)
@receiver(post_delete, sender=Party)
def delete_supporter_media(sender, instance, **kwargs):
    if instance.image:
        delete_media_from_service(instance.image)


@receiver(post_save, sender=User)
def create_related_data(sender, instance, created, **kwargs):
    if created:
        # Create CompanyDetails
        CompanyDetails.objects.create(user=instance, company_name="Default Company")

        # Create Political Profile
        political = Political.objects.create(user=instance, leader_name="Leader")
        
        # Create Political Party for the user
        Party.objects.create(political=political, party_name="Independent")

        # Create 3 Supporters linked to the created Political profile
        for i in range(3):
            Supporters.objects.create(political=political, supporter_name=f"Supporter {i+1}")

        # Create 3 Products
        for i in range(3):
            Product.objects.create(user=instance, name=f"Product {i+1}")