from django.urls import path
from .views import *

urlpatterns = [
#     path('', key_generator_view, name='key_generator'),  # Show the key generation form
#     path('generate-key/', generate_key_endpoint, name='generate_key'),
    path('', youtube_automation, name='youtube_automation'),
]