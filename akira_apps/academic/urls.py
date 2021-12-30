from django.urls import path
from . import views

urlpatterns = [
    path('manage_academic/', views.manage_academic, name='manage_academic'),
    
    path('create_semester_save/', views.create_semester_save, name='create_semester_save'),
    path('fetch_semester/<semester_id>/', views.fetch_semester, name='fetch_semester'),
    path('update_semester_save/<semester_id>/', views.update_semester_save, name='update_semester_save'),
    path('delete_semester/<semester_id>/', views.delete_semester, name='delete_semester'),

    path('create_block_save/', views.create_block_save, name='create_block_save'),
    path('delete_block/<block_id>/', views.delete_block, name='delete_block'),

    path('create_floor_save/', views.create_floor_save, name='create_floor_save'),
    path('delete_floor/<floor_id>/', views.delete_floor, name='delete_floor'),
    path('getFloorbyBlock/', views.getFloorbyBlock, name="getFloorbyBlock"),

    path('create_room_save/', views.create_room_save, name='create_room_save'),
    path('delete_room/<room_id>/', views.delete_room, name='delete_room'),
]