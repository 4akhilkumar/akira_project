from django.urls import path
from . import views

urlpatterns = [
    path('manage_courses/', views.manage_courses, name='manage_courses'),
    path('createCourseAjax/', views.createCourseAjax, name='createCourseAjax'),
    path('createCourse/', views.updateCourse, name='updateCourse'),
    path('editCourse/<course_id>/', views.editCourse, name='editCourse'),
    path('createCourseExtraFieldAjax/', views.createCourseExtraFieldAjax, name='createCourseExtraFieldAjax'),
    path('setCourseExtraFieldValueAjax/', views.setCourseExtraFieldValueAjax, name='setCourseExtraFieldValueAjax'),
    path('deleteCourseExtraFieldValueAjax/', views.deleteCourseExtraFieldValueAjax, name='deleteCourseExtraFieldValueAjax'),

    path('createCourseCOTAjax/', views.createCourseCOTAjax, name='createCourseCOTAjax'),
    path('getAllCurrentCOTAjax/', views.getAllCurrentCOTAjax, name='getAllCurrentCOTAjax'),
    path('setCreatedCOTFieldAjax/', views.setCreatedCOTFieldAjax, name='setCreatedCOTFieldAjax'),
    path('deleteCreatedCOTFieldAjax/', views.deleteCreatedCOTFieldAjax, name='deleteCreatedCOTFieldAjax'),

    path('createCourseCOTExtraFieldAjax/', views.createCourseCOTExtraFieldAjax, name='createCourseCOTExtraFieldAjax'),
    path('setCourseCOTExtraFieldValueAjax/', views.setCourseCOTExtraFieldValueAjax, name='setCourseCOTExtraFieldValueAjax'),
    path('deleteCourseCOTExtraFieldValueAjax/', views.deleteCourseCOTExtraFieldValueAjax, name='deleteCourseCOTExtraFieldValueAjax'),

    path('submitcourseformAjax/', views.submitcourseformAjax, name='submitcourseformAjax'),
    
    path('view_course/<course_code>/', views.view_course, name='view_course'),
    path('search_course/', views.search_course, name='search_course'),
    path('delete_course/<course_id>/', views.delete_course, name='delete_course'),

    path('course_component/', views.course_component, name='course_component'),
    path('sub_component/', views.sub_component, name='sub_component'),
    path('course_task/', views.course_task, name='course_task'),
    path('task_answer/', views.task_answer, name='task_answer'),
    path('subComponentsbyComponents/', views.subComponentsbyComponents, name='subComponentsbyComponents'),

    path('submitSolutionPage/<uuid:task_id>/', views.submitSolutionPage, name='submitSolutionPage'),
]