from django.urls import path
from . import views
app_name = 'hospital_service_management'

urlpatterns = [

     path('hospital/list/', views.HospitalListView.as_view(), name='hospital_list'),
     path('hospital/create/', views.HospitalCreateView.as_view(), name='hospital_create'),
     path('hospital/<int:pk>/update', views.HospitalUpdateView.as_view(), name='hospital_update'),
     path('hospital/<int:pk>/delete', views.HospitalDeleteView.as_view(), name='hospital_delete'),

     path('hospital/<int:hospital>/package/list/', views.HospitalPackageListView.as_view(),
          name='hospital_package_list'),
     path('hospital/<int:hospital>/package/create/', views.HospitalPackageCreateView.as_view(),
          name='hospital_package_create'),
     path('hospital/<int:hospital>/package/<int:pk>/update/', views.HospitalPackageUpdateView.as_view(),
          name='hospital_package_update'),
     path('hospital/<int:hospital>/package/<int:pk>/delete/', views.HospitalPackageDeleteView.as_view(),
          name='hospital_package_delete'),

     path('hospital/<int:hospital>/package/evaluation/list/',
          views.HospitalPackageEvaluationListView.as_view(),
          name='hospital_package_evaluation_list'),

     path('hospital/<int:hospital>/package/<int:hospital_package>/service/list/',
          views.HospitalPackageServiceListView.as_view(),
          name='hospital_package_service_list'),

     path('hospital/<int:hospital>/package/<int:hospital_package>/service/evaluation/list/',
          views.HospitalPackageServiceEvaluationListView.as_view(),
          name='hospital_package_service_evaluation_list'),

     path('hospital/<int:hospital>/package/<int:hospital_package>/service/setting/',
          views.HospitalPackageServiceSettingView.as_view(), name='hospital_package_service_setting'),
     path('hospital/<int:hospital>/package/<int:hospital_package>/service/form',
          views.HospitalPackageServiceFormView.as_view(), name="hospital_package_service_form"),
     path('hospital/<int:hospital>/package/<int:hospital_package>/service/<int:service>/delete',
          views.HospitalPackageServiceDeleteView.as_view(), name="hospital_package_service_delete"),

    # path('contract/<int:contract_hospital>/hospital/<int:hospital>/package/list/',
    #     views.ContractHospitalPackageListView.as_view(),
    #     name='contract_hospital_package_list'),
    # path('contract/<int:contract_hospital>/hospital/<int:hospital>/package/<int:pk>/update/',
    #     views.ContractHospitalPackageUpdateView.as_view(),
    #     name='contract_hospital_package_update'),
    # path('contract/<int:contract_hospital>/hospital/<int:hospital>/package/<int:pk>/delete/',
    #     views.ContractHospitalPackageDeleteView.as_view(),
    #     name='contract_hospital_package_delete'),
    #
    # path('contract/<int:contract_hospital>/hospital/<int:hospital>/package/<int:hospital_package>/service/list/',
    #     views.ContractHospitalPackageServiceListView.as_view(),
    #     name='contract_hospital_package_service_list'),
]
