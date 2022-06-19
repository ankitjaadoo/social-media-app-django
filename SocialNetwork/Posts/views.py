from django.shortcuts import render
from datetime import datetime
from SNUsers.models import SNUser
from SNUsers.views import is_autherized
from Posts.models import SNPost
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Posts.serializer import SNPostsSerializer,SNPostValidator
from django.core.paginator import Paginator
import json
import logging

# Create your views here.


logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log',level=logging.DEBUG)

def get_user_obj(user=None):
    #Returns User Objects corresponding to the username
    return SNUser.objects.get(username=user)

@api_view(['POST'])
def CreatePost(request):
    '''
    Purpose: Creates a new Post
    Input: 
    username: (mandatory) <str> Account user
    post_text: (mandatory) <str> post
    Output: SNPost Object of the created post
    '''
    if request.method == "POST":
        username = request.query_params.get('username')
        text = request.query_params.get('tweet_text')
        if is_autherized(request,username):
            validate = SNPostValidator(request.query_params,request.FILES)
            if not validate.is_valid():
                error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Invalid username or tweet_text"}
                logger.error(error)                    
                return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)

            try:
                user = get_user_obj(username)
                new_tweet = SNPost(username=user,tweet_text=text)
                new_tweet.save()
                serializer = SNPostsSerializer(new_tweet)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "User Does not exist"}
                logger.error(e)                    
                return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                                'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)        

@api_view(['GET'])
def Timeline(request,username):
    '''
    Purpose: Returns the Timeline of the User in a Paginated Fashion
    Input: page (mandatory) <int>  
    Output: Post object with all the posts in the page
    '''
    if is_autherized(request,username):
        try:
            page_no = int(request.query_params.get('page',1))
            userObj = get_user_obj(username)
            if page_no < 1:
                error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Please pass an integer value (starting with 1) as Page Number"}
                logger.error(error)                    
                return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)
            
            posts = SNPost.objects.filter(username=userObj)
            paginator = Paginator(posts,5) #shows 5 tweets per page
            page_num = paginator.get_page(page_no)
            post_objs = page_num.object_list 
            serializer = SNPostsSerializer(post_objs,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "No Tweets to show"}
            logger.error(e)                    
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST) 
    else:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Authentication failed. Please login"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)        

@api_view(['DELETE'])
def DeletePost(request,post_id=None):
    '''
    Purpose: Deletes the post having the id in the URL
    Input: None  
    Output: Post object that was deleted
    '''
    try:
        post = SNPost.objects.get(id=post_id)
        username = post.username.username
        if is_autherized(request,username):
            serializer = SNPostsSerializer(post)
            post.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                                'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)       
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                    'Error_Message': "This tweet no longer exists"}
        logger.error(e)    
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)     

@api_view(['GET'])
def ShowPost(request,post_id=None):
    '''
    Purpose: displays the post with the id in the URL
    Input: None  
    Output: post with given id
    '''
    try:
        post = SNPost.objects.get(id=post_id)
        username = post.username.username
        if is_autherized(request,username): 
            serializer = SNPostsSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                                'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(e)
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                    'Error_Message': "This tweet no longer exists"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def Like(request,post_id=None):
    '''
    Purpose: Like the post with the id in the URL
    Input: username (mandatory) <str> Account user 
    Output: post object that was liked
    '''
    try:
        user = request.query_params.get('username',None)
        validate = SNPostValidator(request.query_params,request.FILES)
        if not validate.is_valid():
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Invalid username"}
            logger.error(error)                    
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)

        if is_autherized(request,user):
            post = SNPost.objects.get(id=post_id)
            post.like.add(get_user_obj(user))
            post.save()
            serializer = SNPostsSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                                'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Error liking the tweet!"}
        logger.error(e)                    
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
def Search(request):
    '''
    Search for a post using a hashtag and a region
    Input:
    username <str> (mandatory) Account User
    hashtag <str> (mandatory) text (with hashtag) to search with
    '''
    user = request.query_params.get('username')
    hashtag = request.query_params.get('hashtag')
    if is_autherized(request,user):
        try:
            post_match = SNPost.objects.filter(post_text__contains=hashtag[1:])
            if post_match:
                serializer = SNPostsSerializer(post_match,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                message = {"Message": "No Match found!"}
                return Response(message,status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error = {'Error_code': status.HTTP_204_NO_CONTENT,
                            'Error_Message': "Please enter a valid search string"}
            logger.error(e)
        return Response(error, status=status.HTTP_204_NO_CONTENT)
    else:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Authentication failed. Please login"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def all_tweets(request):
    '''
    Debugging
    '''
    posts = SNPost.objects.all()
    serializer = SNPostsSerializer(posts,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)