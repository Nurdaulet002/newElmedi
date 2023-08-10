from django.urls import path
from . import views
app_name = 'contract_management'

urlpatterns = [
    path('contract/list/', views.ContractListView.as_view(), name='contract_list'),
    path('contract/create/', views.ContractCreateView.as_view(), name='contract_create'),
    path('contract/<int:pk>/update/', views.ContractUpdateView.as_view(), name='contract_update'),
    path('contract/<int:pk>/delete/', views.ContractDeleteView.as_view(), name='contract_delete'),

    path('contract/<int:contract>/program/list/', views.ContractProgramListView.as_view(),
         name='contract_program_list'),
    path('contract/<int:contract>/program/create/', views.ContractProgramCreateView.as_view(),
         name='contract_program_create'),
    path('contract/<int:contract>/program/<int:pk>/update/', views.ContractProgramUpdateView.as_view(),
         name='contract_program_update'),
    path('contract/<int:contract>/program/<int:pk>/delete/', views.ContractProgramDeleteView.as_view(),
         name='contract_program_delete'),

    path('contract/<int:contract>/program/<int:program>/package/list/',
         views.ContractProgramPackageListView.as_view(), name='contract_program_package_list'),
    path('contract/<int:contract>/program/<int:program>/package/create/',
         views.ContractProgramPackageCreateView.as_view(), name='contract_program_package_create'),
    path('contract/<int:contract>/program/<int:program>/package/<int:pk>/update/',
         views.ContractProgramPackageUpdateView.as_view(), name='contract_program_package_update'),
    path('contract/<int:contract>/program/<int:program>/package/<int:pk>/delete/',
         views.ContractProgramPackageDeleteView.as_view(), name='contract_program_package_delete'),

    path('contract/<int:pk>/result/', views.ContractResultView.as_view(),
         name='contract_result'),

    path('hospital/list/', views.HospitalListView.as_view(),
         name='hospital_list'),
    path('hospital/<int:pk>/update', views.HospitalUpdateView.as_view(),
         name='hospital_update'),

    path('insurance/list/', views.InsuranceListView.as_view(),
         name='insurance_list'),
    path('insurance/<int:pk>/update', views.InsuranceUpdateView.as_view(),
         name='insurance_update'),

    

    path('contract/contract_customer/list/', views.ContractCustomerListView.as_view(),
         name='contract_customer_list'),
    path('contract/contract_customer/<int:pk>/detail/', views.ContractCustomerDetailView.as_view(),
         name='contract_customer_detail'),
    path('contract/contract_customer/create/', views.ContractCustomerCreateView.as_view(),
         name='contract_customer_create'),
    path('contract/contract_customer/<int:pk>/delete/', views.ContractCustomerDeleteView.as_view(),
         name='contract_customer_delete'),
    

    path('contract/contract_hospital/list/', views.ContractHospitalListView.as_view(),
         name='contract_hospital_list'),
    path('contract/contract_hospital/confirm/list/', views.ContractHospitalConfirmListView.as_view(),
         name='contract_hospital_confir_list'),
    path('contract/contract_hospital/create/', views.ContractHospitalCreateView.as_view(),
         name='contract_hospital_create'),
    path('contract/contract_hospital/<int:pk>/update/', views.ContractHospitalUpdateView.as_view(),
         name='contract_hospital_update'),
    path('contract/contract_hospital/<int:pk>/delete/', views.ContractHospitalDeleteView.as_view(),
         name='contract_hospital_delete'),

    path('contract/<int:contract>/program/<int:program>/package/<int:package>/service/list/',
         views.ContractProgramPackageServiceListView.as_view(),
         name='contract_program_package_service_list'),
    path('contract/<int:contract>/program/<int:program>/package/<int:package>/service/result/list/',
         views.ContractProgramPackageResultListView.as_view(),
         name='contract_program_package_service_result_list'),
    path('package/<int:package>/service/<int:service>/delete', views.PackageServiceDeleteView.as_view(),
         name="package_service_delete"),

    path('hospital_package_status_update/<int:pk>',
         views.HospitalPackageStatusUpdate.as_view(),
         name='hospital_package_status_update'),
    path('hospital_package/service_export/<int:contract_hospital>', views.HospitalPackageServiceExportView.as_view(),
         name='hospital_package_service_export'),

    path('contract/<int:contract>/program_blank/create',
         views.ProgramBlankCreateView.as_view(), name='program_blank_create'),

    path('program_by_contract/<int:contract>', views.ProgramByContractView.as_view(),
         name='program_by_contract'),

    path('contract/<int:contract_hospital>/hospital/<int:hospital>/package/list/',
         views.ContractHospitalPackageListView.as_view(),
         name='contract_hospital_package_list'),

    path('contract/<int:contract_hospital>/hospital/<int:hospital>/package/<int:pk>/update/',
         views.ContractHospitalPackageUpdateView.as_view(),
         name='contract_hospital_package_update'),
    path('contract/<int:contract_hospital>/hospital/<int:hospital>/package/<int:pk>/delete/',
         views.ContractHospitalPackageDeleteView.as_view(), name='contract_hospital_package_delete'),

    path('contract/<int:contract_hospital>/hospital/<int:hospital>/package/<int:hospital_package>/service/list/',
         views.ContractHospitalPackageServiceListView.as_view(),
         name='contract_hospital_package_service_list'),
    path('contract/<int:contract_hospital>/hospital/<int:hospital>/service/list/',
         views.ContractHospitalServiceListView.as_view(),
         name='contract_hospital_service_list'),

    path('contract/<int:contract_hospital>/hospital/<int:hospital>/service/excel/',
         views.ContractHospitalServiceExcelView.as_view(),
         name='contract_hospital_service_excel'),
    path('contract/<int:contract_hospital>/hospital/<int:hospital>/service/treaty_list/',
         views.ContractHospitalServiceTreatyListView.as_view(),
         name='contract_hospital_service_treaty_list'),
    
    path('hospital/<int:hospital>/package/<int:hospital_package>/service/form',
         views.HospitalPackageServiceFormView.as_view(), name="hospital_package_service_form"),

    path('contract_hospital/status_update',
         views.ContractHospitalStatusUpdateView.as_view(), name="contract_hospital_status_update"),

    
    
    
]
