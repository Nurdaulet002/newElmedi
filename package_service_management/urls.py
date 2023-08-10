from django.urls import path
from . import views
app_name = 'package_service_management'

urlpatterns = [
    path('package/list/', views.PackageListView.as_view(), name='package_list'),
    path('package/create/', views.PackageCreateView.as_view(), name='package_create'),
    path('package/<int:pk>/update/', views.PackageUpdateView.as_view(), name='package_update'),
    path('package/<int:pk>/delete/', views.PackageDeleteView.as_view(), name='package_delete'),
    path('package/evaluation/list/', views.PackageEvaluationListView.as_view(), name='package_evaluation_list'),
    path('package/<int:package>/service/list/', views.PackageServiceListView.as_view(),
         name='package_service_list'),
    path('package/<int:package>/service/evaluation/list/', views.PackageServiceEvaluationListView.as_view(),
         name='package_service_evaluation_list'),
    path('package/<int:package>/service/form', views.PackageServiceFormView.as_view(),
         name="package_service_form"),
    path('package/<int:package>/service/setting/form',
         views.PackageServiceSettingFormView.as_view(),
         name="package_service_setting_form"),
    path('service/setting',
         views.ServiceSettingView.as_view(),
         name="service_setting"),
    path('service/setting/form',
         views.ServiceSettingFormView.as_view(),
         name="service_setting_form"),

    path('package/<int:package>/service/setting/', views.PackageServiceSettingView.as_view(),
         name='package_service_setting'),
    path('package/<int:package>/service/<int:service>/delete', views.PackageServiceDeleteView.as_view(),
         name="package_service_delete"),
]
