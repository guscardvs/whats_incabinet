from django.urls import path

from user_items import views

urlpatterns = [
    path('list-items', views.ListItems.as_view(), name='list_items'),
    path('create', views.CreateItem.as_view(), name='create_item'),
    path('remove/<str:pk>', views.remove_item, name='remove_item'),
    path('edit/<str:pk>', views.EditItem.as_view(), name='edit_item')
]
