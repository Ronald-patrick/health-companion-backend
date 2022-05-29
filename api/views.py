from datetime import datetime
from unittest import result
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import InfoSerializer, PostSerializer
from .models import AddictionInfo, Post, User, UserAddiction
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import cloudinary.uploader
import urllib.request
import hashlib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from api.apps import ChestApiConfig
from rest_framework import status
import numpy as np


@api_view(['GET'])
def getRoutes(request):
    return Response("Hello Django")

# Serialize Data to get JSON response -> Serializer

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# def getPost(request,pk):
#     post = Post.objects.get(id=pk)
#     serializer = PostSerializer(post, many = False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# def updatePost(request,pk):
#     post = Post.objects.get(id=pk)
#     serializer = PostSerializer(post, data=request.data)
#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)


# @api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# def deletePost(request,pk):
#     post = Post.objects.get(id=pk)
#     post.delete()

#     return Response('POST Deleted')

def mdhash(s):
    hashed = hashlib.md5(s.encode())
    return hashed.hexdigest()


@api_view(['POST'])
def registerUser(request):

    email = request.data["email"]
    password = mdhash(request.data["password"])
    username = request.data["username"]

    # UserModel.objects.create(
    #     email = email,
    #     password = password,
    #     username = username
    # )
    user = User.objects.create_user(username, email, password)
    user.save()

    token_obj, _ = Token.objects.get_or_create(user=user)
    print(token_obj)
    return Response({'status': 'Created', 'payload': {username, email}, 'token': str(token_obj)}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def loginUser(request):
    username = request.data["username"]
    password = mdhash(request.data["password"])
    user = authenticate(username=username, password=password)
    if user is not None:
        token_obj, _ = Token.objects.get_or_create(user=user)
        return Response({'status': 'Success', 'payload': f'Logged in : {user.id}', 'token': str(token_obj)}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'Error', 'payload': 'Invalid Auth'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createAddiction(request):
    data = request.data
    print(request.user.id)
    serializer = InfoSerializer(data=data, many=False)

    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)

    UserAddiction.objects.create(
        userid=request.user.id,
        aid=serializer.data["aid"]
    )

    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createPost(request):
    data = request.data
    serializer = PostSerializer(data=data, many=False)

    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)

    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def getInfo(request):
    id = request.user.id

    data = UserAddiction.objects.filter(userid=id).values("aid")
    if(len(data) == 0 ):
        return Response([])
    n = len(data)
    arr = []
    for x in data:
        aid = x['aid']
        arr.append(AddictionInfo.objects.filter(aid=aid).values()[0])

    return Response(arr)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getPosts(request):

    aid = request.data["aid"]
    data = Post.objects.filter(aid=aid).values()
    print(data)

    return Response(data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def explore(request):
    id = request.user.id
    data = UserAddiction.objects.filter(userid=id).values("aid")
    arr = []
    for x in data:
        arr.append(x['aid'])
    
    data = AddictionInfo.objects.all().exclude(aid__in=arr).values()
    print(data)
    return Response(data)


@api_view(['GET'])
def getInfoExplore(request, pk):

    data = AddictionInfo.objects.filter(aid=pk).values()
    return Response({"info": data[0]})


@api_view(['GET'])
def getPostExplore(request, pk):

    data = AddictionInfo.objects.filter(aid=pk).values("aid")
    aid = data[0]['aid']

    data = Post.objects.filter(aid=aid).values()

    return Response(data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search(request, pk):
    id = request.user.id
    data = UserAddiction.objects.filter(userid=id).values("aid")
    aid = data[0]['aid']
    data = AddictionInfo.objects.filter(
        title__icontains=pk).exclude(aid=aid).values()

    return Response(data)


def download_image(url, file_path, file_name):
    full_path = file_path + file_name + '.jpg'
    urllib.request.urlretrieve(url, full_path)


def predict(cloud_data):
    filename = cloud_data["img_public_id"]
    imglink = cloud_data["imgId"]

    download_image(imglink, 'staticfiles/', filename)
    data_list_dict = {
        0: 'NORMAL',
        1: 'PNEUMONIA'
    }

    img = image.load_img('staticfiles/'+filename+".jpg", target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    img_data = preprocess_input(x)
    p_classes = ChestApiConfig.model.predict(img_data)
    print(p_classes)
    predict_score = np.argmax(p_classes[0])
    print(predict_score)
    result = data_list_dict[predict_score]

    return result


@api_view(['POST'])
def ImgCloudinaryUpload(request):
    if (request.method == 'POST' and request.FILES):
        userid = "bhaven"
        try:
            imgFile = request.FILES.get('Xray')
            cloud_file = cloudinary.uploader.upload(imgFile)
            cloud_file_data = {
                "imgId": cloud_file['url'], "img_public_id": cloud_file['public_id'], 'UID': userid, }

            if cloud_file_data != None:
                result = predict(cloud_file_data)

            return Response({
            'status': 'success',
            'result': result}, status=201)

        except Exception as e:
            print(e)
        

