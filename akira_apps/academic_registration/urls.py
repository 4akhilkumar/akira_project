from django.urls import path
from . import views

urlpatterns = [
    path('aca_Registration/', views.aca_Registration, name='aca_Registration'),

    path('createsemester/', views.createsemester, name='createsemester'),
    path('createsemesterAjax/', views.createsemesterAjax, name='createsemesterAjax'),
    path('getAllSemestersAjax/', views.getAllSemestersAjax, name='getAllSemestersAjax'),
    path('setSemesterStatusAjax/', views.setSemesterStatusAjax, name='setSemesterStatusAjax'),

    path('setTeachingStaffSemesterRegistrationAjax/', views.setTeachingStaffSemesterRegistrationAjax, name='setTeachingStaffSemesterRegistrationAjax'),
    path('setStudentSemesterRegistrationAjax/', views.setStudentSemesterRegistrationAjax, name='setStudentSemesterRegistrationAjax'),
    
    path('createbranchAjax/', views.createbranchAjax, name='createbranchAjax'),
    path('createbranch/', views.createbranch, name='createbranch'),
    path('getAllBranchesAjax/', views.getAllBranchesAjax, name='getAllBranchesAjax'),
    path('studentAcaReg/', views.studentAcaReg, name='studentAcaReg'),
    path('allocatedCourseForSemester/', views.allocatedCourseForSemester, name='allocatedCourseForSemester'),
    path('allocateCourseForSemester/', views.allocateCourseForSemester, name='allocateCourseForSemester'),
    path('allocateCourseForSemesterAjax/', views.allocateCourseForSemesterAjax, name='allocateCourseForSemesterAjax'),
    path('fetcheachallocatedCourseForSemester/<uuid:id>/', views.fetcheachallocatedCourseForSemester, name='fetcheachallocatedCourseForSemester'),
    path('editallocatedCourseForSemesterAjax/', views.editallocatedCourseForSemesterAjax, name='editallocatedCourseForSemesterAjax'),
]