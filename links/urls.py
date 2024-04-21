from django.urls import path

from .views import (CollectionListCreateAPIView,
                    CollectionRetrieveUpdateDestroyAPIView,
                    LinkListCreateAPIView, LinkRetrieveUpdateDestroyAPIView)

urlpatterns = [
    path(
        "collections/",
        CollectionListCreateAPIView.as_view(),
        name="collection-list"),
    path(
        "collections/<int:pk>/",
        CollectionRetrieveUpdateDestroyAPIView.as_view(),
        name="collection-detail",
    ),
    path("links/", LinkListCreateAPIView.as_view(), name="link-list"),
    path(
        "links/<int:pk>/",
        LinkRetrieveUpdateDestroyAPIView.as_view(),
        name="link-detail",
    ),
]
