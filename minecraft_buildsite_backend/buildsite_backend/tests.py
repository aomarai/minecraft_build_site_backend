import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Build, Comment, Rating, Material, BillOfMaterials, BuildLayer, BuildTag, FavoriteBuild

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def build(user):
    return Build.objects.create(user=user, title='Test Build', description='A test build')

@pytest.fixture
def material():
    return Material.objects.create(name='Test Material', image='test_image.png')

def creates_comment_successfully(user, build):
    client = APIClient()
    client.login(username='testuser', password='testpass')
    response = client.post(reverse('comment-list'), {'build': build.id, 'content': 'Nice build!'})
    assert response.status_code == 201
    assert Comment.objects.filter(build=build, user=user).exists()

def creates_rating_successfully(user, build):
    client = APIClient()
    client.login(username='testuser', password='testpass')
    response = client.post(reverse('rating-list'), {'build': build.id, 'score': 5})
    assert response.status_code == 201
    assert Rating.objects.filter(build=build, user=user).exists()

def creates_material_successfully(material):
    assert Material.objects.filter(name='Test Material').exists()

def creates_bill_of_materials_successfully(build, material):
    bom = BillOfMaterials.objects.create(build=build, material=material, quantity=10)
    assert BillOfMaterials.objects.filter(build=build, material=material).exists()

def creates_build_layer_successfully(build):
    layer = BuildLayer.objects.create(build=build, layer_number=1, data={})
    assert BuildLayer.objects.filter(build=build, layer_number=1).exists()

def creates_build_tag_successfully(build):
    tag = BuildTag.objects.create(name='Test Tag')
    tag.builds.add(build)
    assert BuildTag.objects.filter(name='Test Tag', builds=build).exists()

def creates_favorite_build_successfully(user, build):
    favorite = FavoriteBuild.objects.create(user=user, build=build)
    assert FavoriteBuild.objects.filter(user=user, build=build).exists()