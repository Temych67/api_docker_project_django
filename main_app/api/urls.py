from django.urls import path
from main_app.api.views import (
    api_detail_post_view,
    api_update_post_view,
    api_delete_post_view,
    api_create_post_view,
    #
    ApiAllCommentsView,
    api_detail_comment_view,
    api_update_comment_view,
    api_create_comment_view,
    api_delete_comment_view,
    #
    api_vote_post_view,
)

app_name = "main_app"

urlpatterns = [
    # post url
    path("post_view/<title>", api_detail_post_view, name="detail_post"),
    path("post_view/<title>/update", api_update_post_view, name="update"),
    path("post_view/<title>/delete", api_delete_post_view, name="delete"),
    path("post_view/create", api_create_post_view, name="create"),
    # comment url
    path("all_comments/<title>", ApiAllCommentsView.as_view(), name="detail_all_comments"),
    path(
        "comment/<title>-<id_comment>", api_detail_comment_view, name="detail_comment"
    ),
    path(
        "comment/<title>-<id_comment>/update",
        api_update_comment_view,
        name="update_comment",
    ),
    path("comment/<title>/create", api_create_comment_view, name="create_comment"),
    path(
        "comment/<title>-<id_comment>/delete",
        api_delete_comment_view,
        name="delete_comment",
    ),
    # vote post url
    path("vote/<title>-<vote_request>", api_vote_post_view, name="vope_comment"),
]
