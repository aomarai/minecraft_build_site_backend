from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='avatar_images/', blank=True, null=True)

class Build(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='builds')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, max_length=5120)
    file = models.FileField(upload_to='build_files/')
    thumbnail = models.ImageField(upload_to='build_thumbnails')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    build = models.ForeignKey(Build, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=2048,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # For comment editing

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    build = models.ForeignKey(Build, on_delete=models.CASCADE, related_name='comments')
    score = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # For editing a rating later

class Material(models.Model): # TODO: Add support for modded blocks
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="materials/", blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BillOfMaterials(models.Model):
    build = models.ForeignKey(Build, on_delete=models.CASCADE, related_name='bom')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('build', 'material') # Prevent duplicate entries for the same material in a build

    def __str__(self):
        return f'{self.material.name} - {self.quantity}'