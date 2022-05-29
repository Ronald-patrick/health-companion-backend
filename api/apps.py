from django.apps import AppConfig
from tensorflow.keras.models import load_model
from tensorflow import keras
from django.conf import settings
import os

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

class ChestApiConfig(AppConfig):
    name = 'chest_api'
    MODEL_FILE = os.path.join(settings.MODELS, 'vgg16_final.h5')
    # MODEL_FILE2 = os.path.join(settings.MODELS, 'vgg19_final.h5')
    model = load_model(MODEL_FILE)
    # model2 = load_model(MODEL_FILE2)
