from django.urls import path, include

urlpatterns = [
    path('profile/', include('profiles.urls')),
    path('user-item/', include('user_items.urls'))
]
