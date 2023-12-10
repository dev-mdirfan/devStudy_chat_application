from django.db import models
from django.contrib.auth.models import User
from PIL import Image

def user_avatar_directory_path(instance, filename):
    from time import gmtime, strftime
    date_path = strftime("%Y/%m/%d", gmtime())
    return "user_{0}/avatar/{1}/{2}".format(instance.user.id, date_path, filename)

def user_cover_directory_path(instance, filename):
    from time import gmtime, strftime
    date_path = strftime("%Y/%m/%d", gmtime())
    return "user_{0}/cover/{1}/{2}".format(instance.user.id, date_path, filename)

class Profile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    avatar = models.ImageField(default='avatar.png', upload_to=user_avatar_directory_path)
    # cover image here
    cover = models.ImageField(default='cover.png', upload_to=user_cover_directory_path)
    # city
    city = models.CharField(max_length=100, default='City')
    # role
    # role = models.CharField(max_length=100, default='Role')
    # country
    # country = models.CharField(max_length=100, default='Country')
    # language
    
    
    # Override the __str__() method to return out something meaningful!
    def __str__(self):
        return f'{self.user.username}\'s Profile'
    
    # Override the save() method of the model to resize the image.
    # This is done to ensure that all profile pictures are the same size.
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # Run the save() method of the parent class.
        
        avatar_img = Image.open(self.avatar.path) # Open the image of the current instance.
        
        # If the image is larger than 300px by 300px, resize it.
        if avatar_img.height > 300 or avatar_img.width > 300:
            output_size = (300, 300) # Set the output size.
            avatar_img.thumbnail(output_size) # Resize the image.
            avatar_img.save(self.avatar.path) # Save the resized image to the same path.