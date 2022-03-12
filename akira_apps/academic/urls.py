from django.urls import path
from . import views

urlpatterns = [
    path('manage_academic/', views.manage_academic, name='manage_academic'),

    path('create_block_save/', views.create_block_save, name='create_block_save'),
    path('delete_block/<block_id>/', views.delete_block, name='delete_block'),

    path('create_floor_save/', views.create_floor_save, name='create_floor_save'),
    path('delete_floor/<floor_id>/', views.delete_floor, name='delete_floor'),
    path('getFloorbyBlock/', views.getFloorbyBlock, name="getFloorbyBlock"),

    path('create_room_save/', views.create_room_save, name='create_room_save'),
    path('delete_room/<room_id>/', views.delete_room, name='delete_room'),

    path('bulk_upload_academic_info_save/', views.bulk_upload_academic_info_save, name='bulk_upload_academic_info_save'),
    path('academic_info_csv/', views.academic_info_csv, name='academic_info_csv'),

    path('add_branch/', views.add_branch, name='add_branch'),
    path('getAllBranches/', views.getAllBranches, name='getAllBranches'),
    # path('update_branch/<block_id>/', views.update_branch, name='update_branch'),
    # path('delete_branch/<block_id>/', views.delete_branch, name='delete_branch'),

    path('TestingMet/', views.TestingMet, name='TestingMet'),
]