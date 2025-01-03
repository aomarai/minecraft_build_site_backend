from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=32, blank=True)
    profile_picture = models.ImageField(upload_to='avatar_images/', blank=True, null=True)
    bio = models.TextField(max_length=512, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return self.display_name if self.display_name and self.display_name.strip() else self.user.username

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
    build = models.ForeignKey(Build, on_delete=models.CASCADE, related_name='rating')
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

class BuildLayer(models.Model):
    build = models.ForeignKey(Build, on_delete=models.CASCADE, related_name='layers')
    layer_number = models.PositiveIntegerField()
    data = models.JSONField()

    class Meta:
        unique_together = ('build', 'layer_number')

    def __str__(self):
        return f'Layer {self.layer_number}'

class BuildTag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    builds = models.ManyToManyField(Build, related_name='tags')

    def __str__(self):
        return self.name

class FavoriteBuild(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    build = models.ForeignKey(Build, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'build')

    def __str__(self):
        return f'{self.user.username} - {self.build.title}'