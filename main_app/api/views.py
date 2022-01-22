from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView

from main_app.models import Post, Comment, Vote
from main_app.api.serializers import (
    PostSerializer,
    AllCommentsSerializer,
    CommentSerializer,
)

SUCCESS = "success"
ERROR = "error"
DELETE_SUCCESS = "deleted"
UPDATE_SUCCESS = "updated"
CREATE_SUCCESS = "created"
UPVOTE_SUCCESS = "upnvote was success "
DOWNVOTE_SUCCESS = "downvote was success "

@api_view(
    [
        "GET",
    ]
)
def api_detail_post_view(request, title):
    try:
        post = Post.objects.get(title=title)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)


@api_view(
    [
        "GET",
    ]
)
def api_detail_comment_view(request, title, id_comment):
    try:
        post = Post.objects.get(title=title)
        comment = Comment.objects.get(id=id_comment, post=post)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = AllCommentsSerializer(comment)
        return Response(serializer.data)


@api_view(
    [
        "PUT",
    ]
)
@permission_classes((IsAuthenticated,))
def api_update_post_view(request, title):
    try:
        post = Post.objects.get(title=title)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if post.author != user:
        return Response({"response": "You don`t have permission to edit that."})

    if request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data[SUCCESS] = UPDATE_SUCCESS
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "PUT",
    ]
)
@permission_classes((IsAuthenticated,))
def api_update_comment_view(request, title, id_comment):
    try:
        post = Post.objects.get(title=title)
        comment = Comment.objects.get(id=id_comment, post=post)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if comment.author != user:
        return Response({"response": "You don`t have permission to edit that."})

    if request.method == "PUT":
        serializer = CommentSerializer(comment, data=request.data)
        data = {}
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            data[SUCCESS] = UPDATE_SUCCESS
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "DELETE",
    ]
)
@permission_classes((IsAuthenticated,))
def api_delete_post_view(request, title):
    try:
        post = Post.objects.get(title=title)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if post.author != user:
        return Response({"response": "You don`t have permission to delete that."})

    if request.method == "DELETE":
        operation = post.delete()
        data = {}
        if operation:
            data[SUCCESS] = DELETE_SUCCESS
        return Response(data=data)


@api_view(
    [
        "DELETE",
    ]
)
@permission_classes((IsAuthenticated,))
def api_delete_comment_view(request, title, id_comment):
    try:
        post = Post.objects.get(title=title)
        comment = Comment.objects.get(id=id_comment, post=post)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user
    if comment.author != user:
        return Response({"response": "You don`t have permission to delete that."})

    if request.method == "DELETE":
        operation = comment.delete()
        data = {}
        if operation:
            data[SUCCESS] = DELETE_SUCCESS
        return Response(data=data)


@api_view(
    [
        "POST",
    ]
)
@permission_classes((IsAuthenticated,))
def api_create_post_view(request):
    account = request.user

    post = Post(author=account)

    if request.method == "POST":
        serializer = PostSerializer(post, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data[SUCCESS] = CREATE_SUCCESS
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "POST",
    ]
)
@permission_classes((IsAuthenticated,))
def api_create_comment_view(request, title):
    account = request.user
    post = Post.objects.get(title=title)
    comment = Comment(author=account, post=post)

    if request.method == "POST":
        serializer = CommentSerializer(comment, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data[SUCCESS] = CREATE_SUCCESS
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "POST",
    ]
)
@permission_classes((IsAuthenticated,))
def api_vote_post_view(request, title, vote_request):
    account = request.user
    post = Post.objects.get(title=title)
    data={}
    if request.method == "POST":
        try:
            vote = Vote.objects.get(postID=post, userID=account)
        except Vote.DoesNotExist:
            vote = None
        if vote_request == "up":
            if vote is None:
                # find post by title and increment
                vote = Vote(postID=post, userID=request.user)
                post.amount_of_upvotes += 1
                vote.save()
                data[SUCCESS] = UPVOTE_SUCCESS
        elif vote_request == "down":
            if vote is not None:
                # find post by title and increment
                post.amount_of_upvotes -= 1
                vote.delete()
                data[SUCCESS] = DOWNVOTE_SUCCESS
        post.save()

        return Response(data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class ApiAllCommentsView(ListAPIView):
    serializer_class = AllCommentsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        post = Post.objects.get(title=self.kwargs.get("title"))
        return Comment.objects.filter(post=post)
