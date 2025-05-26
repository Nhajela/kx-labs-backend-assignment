from django.urls import path
from . import models

urlpatterns = [
    path('validate-syntax/', models.validate_syntax, name='validate_syntax'),
]