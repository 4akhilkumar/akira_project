from django.urls import path
from . import views

urlpatterns = [
    path('create_semester/', views.create_semester, name='create_semester'),
    path('save_created_semester/', views.save_created_semester, name='save_created_semester'),
    path('manage_block/', views.manage_block, name='manage_block'),
    path('create_block/', views.create_block, name='create_block'),
    path('create_block_save/', views.create_block_save, name='create_block_save'),
    path('edit_block/<block_id>/', views.edit_block, name='edit_block'),
    path('edit_block_save/<block_id>/', views.edit_block_save, name='edit_block_save'),
    path('delete_block/<block_id>/', views.delete_block, name='delete_block'),

]