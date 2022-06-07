from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.manage_courses, name='manage_courses'),
    path('createCourse/', views.updateCourse, name='updateCourse'),
    path('createCourseAjax/', views.createCourseAjax, name='createCourseAjax'),
    path('bulkCreateCourses', views.bulkCreateCourses, name = 'bulkCreateCourses'),

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

    path('editCourse/<course_id>/', views.editCourse, name='editCourse'),
    path('viewCourse/<course_code>/', views.view_course, name='view_course'),
    path('deleteCourse/<course_id>/', views.delete_course, name='delete_course'),

    re_path(r'^searchCourses/?$', views.searchCourses, name='searchCourses'),

    path('fetchTeachingStaff', views.fetchTeachingStaff, name='fetchTeachingStaff'),

    path('teachingstaffCourseEnrollAjax/', views.teachingstaffCourseEnrollAjax, name='teachingstaffCourseEnrollAjax'),
    path('studentCourseEnrollAjax/', views.studentCourseEnrollAjax, name='studentCourseEnrollAjax'),

    path('courseComponent/', views.course_component, name='course_component'),
    path('subComponent/', views.sub_component, name='sub_component'),
    path('courseTask/', views.course_task, name='course_task'),
    path('taskAnswer/', views.task_answer, name='task_answer'),
    path('subComponentsbyComponents/', views.subComponentsbyComponents, name='subComponentsbyComponents'),

    path('submitSolutionPage/<uuid:task_id>/', views.submitSolutionPage, name='submitSolutionPage'),
]