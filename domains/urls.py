from django.urls import path
from . import views as domains_view
urlpatterns = [
    path('peer-data/', domains_view.PeerLinkView.as_view()),
    path('user-data/', domains_view.UserView.as_view()),
]
