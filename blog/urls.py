from django.urls import path
from . import views

urlpatterns = [
    path('',views.StartingPageView.as_view(),name='starting-page'),
    path('posts',views.AllPostsView.as_view(),name='posts'),
    path("posts/<slug:slug>",views.SinglePostView.as_view(),name="single-post-page"),
    path('thank-you',views.thank_you),
    path('read-later',views.ReadLater.as_view(),name="read-later"),
]