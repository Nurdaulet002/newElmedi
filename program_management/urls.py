from django.urls import path
from . import views
app_name = 'program_management'

urlpatterns = [
    path('program/list/', views.ProgramListView.as_view(), name='program_list'),
    path('program/create/', views.ProgramCreateView.as_view(), name='program_create'),
    path('program/<int:pk>/update/', views.ProgramUpdateView.as_view(), name='program_update'),
    path('program/<int:pk>/delete/', views.ProgramDeleteView.as_view(), name='program_delete'),

    path('program/<int:program>/package/list/', views.ProgramPackageListView.as_view(),
         name='program_package_list'),
    path('program/<int:program>/package/create/', views.ProgramPackageCreateView.as_view(),
         name='program_package_create'),
    path('program/<int:program>/package/<int:pk>/update/', views.ProgramPackageUpdateView.as_view(),
         name='program_package_update'),
    path('program/<int:program>/package/<int:pk>/delete/', views.ProgramPackageDeleteView.as_view(),
         name='program_package_delete'),

    path('program/<int:program>/package_blank/create', views.PackageBlankCreateView.as_view(),
         name='package_blank_create'),

    path('program/<int:program>/package/<int:package>/service/list/', views.PackageServiceListView.as_view(),
         name='package_service_list'),
    path('package/<int:package>/service/<int:service>/delete', views.PackageServiceDeleteView.as_view(),
         name="package_service_delete"),

    path('program/<int:program>/package/<int:package>/service/setting/',
         views.ProgramPackageServiceSettingView.as_view(),
         name='program_package_service_setting'),

    path('program/<int:program>/package/<int:package>/service/setting/form',
         views.ProgramPackageServiceSettingFormView.as_view(),
         name="program_package_service_setting_form"),
]
