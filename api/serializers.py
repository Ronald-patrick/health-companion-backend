from rest_framework.serializers import ModelSerializer
from .models import AddictionInfo, Post
from .models import User


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class InfoSerializer(ModelSerializer):
    class Meta:
        model = AddictionInfo
        fields = '__all__'