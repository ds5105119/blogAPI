from django.urls import path, include

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("posts/", include("posts.urls")),
    path("follows/", include("follows.urls")),
    # path('comments/', include('comments.urls')),
    path("profiles/", include("profiles.urls")),
    # path('likes/', include('likes.urls')),
]
