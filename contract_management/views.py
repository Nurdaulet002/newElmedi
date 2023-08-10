from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .resources import HospitalPackageServiceResource
from .models import Contract, ContractCustomer, ContractHospital, Program,\
    PackageService, Package, HospitalPackage, HospitalPackageService
from .forms import ContractForm, ContractCustomerForm,\
    ContractHospitalForm, ProgramForm, PackageForm, ProgramBlankForm, HospitalPackageForm,\
    HospitalPackageServiceForm
from referral_management.models import Referral
from invoice_management.models import Invoice
from package_icd_management.models import PackageICD
from directory.models import Service, Hospital, Insurance,Insurer


# Mixin программы
class ContractMixin(LoginRequiredMixin):
    model = Contract
    success_url = reverse_lazy('contract_management:contract_list')


class ContractEditMixin(ContractMixin):
    form_class = ContractForm


class ContractListView(ContractMixin, ListView):
    template_name = 'contract_management/contract/list.html'
    context_object_name = 'contracts'
    paginate_by = 100


class ContractCreateView(ContractEditMixin, CreateView):
    template_name = 'contract_management/contract/create.html'


# Обновить программу
class ContractUpdateView(ContractEditMixin, UpdateView):
    template_name = 'contract_management/contract/update.html'


# Удалить
class ContractDeleteView(ContractMixin, DeleteView):
    template_name = 'contract_management/contract/delete.html'


# Mixin пакета программы
class ContractProgramMixin(LoginRequiredMixin):
    model = Program

    def get_queryset(self):
        qs = super().get_queryset()
        contract = self.kwargs.get('contract')
        return qs.filter(contract=contract)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['contract'] = get_object_or_404(Contract, pk=self.kwargs.get('contract'))
        return context

    def get_success_url(self):
        contract = self.kwargs.get('contract')
        return reverse_lazy('contract_management:contract_program_list', kwargs={'contract': contract})


class ContractProgramEditMixin:
    form_class = ProgramForm


# Список пакетов программы
class ContractProgramListView(ContractProgramMixin, ListView):
    template_name = 'contract_management/contract_program/list.html'
    context_object_name = 'contract_programs'


# Создать пакет программ
class ContractProgramCreateView(ContractProgramMixin, ContractProgramEditMixin, CreateView):
    template_name = 'contract_management/contract_program/create.html'


# Обновить программу
class ContractProgramUpdateView(ContractProgramMixin, ContractProgramEditMixin, UpdateView):
    template_name = 'contract_management/contract_program/update.html'


# Обновить программу
class ContractProgramDeleteView(ContractProgramMixin, DeleteView):
    template_name = 'contract_management/contract_program/delete.html'


class ContractResultView(TemplateResponseMixin, View):
    template_name = 'contract_management/contract_result/result.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        contract = Contract.objects.get(pk=pk)
        contract_exclusions = PackageICD.objects.filter(package_id=1).all()
        before_contract_exclusions = PackageICD.objects.filter(package_id=2).all()
        return self.render_to_response({
            'contract': contract,
            'contract_exclusions': contract_exclusions,
            'before_contract_exclusions': before_contract_exclusions
        })


# Mixin программы
class ContractProgramPackageMixin(LoginRequiredMixin):
    model = Package
    context_object_name = 'packages'
    contract = None
    program = None

    def dispatch(self, *args, **kwargs):
        self.contract = get_object_or_404(Contract, pk=self.kwargs.get('contract'))
        self.program = get_object_or_404(Program, pk=self.kwargs.get('program'))
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        contract = self.kwargs.get('contract')
        program = self.kwargs.get('program')
        return reverse_lazy('contract_management:contract_program_package_list',
                            kwargs={'contract': contract, 'program': program})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['contract'] = self.contract
        context['program'] = self.program
        return context


# Mixin программы
class ContractProgramPackageEditMixin:
    form_class = PackageForm


class ContractProgramPackageListView(ContractProgramPackageMixin, ListView):
    template_name = 'contract_management/contract_program_package/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(program=self.program)


class ContractProgramPackageCreateView(ContractProgramPackageMixin, ContractProgramPackageEditMixin, CreateView):
    template_name = 'contract_management/contract_program_package/create.html'

    def form_valid(self, form):
        form.instance.program = get_object_or_404(Program, pk=self.kwargs.get('program'))
        return super(ContractProgramPackageCreateView, self).form_valid(form)


class ContractProgramPackageUpdateView(ContractProgramPackageMixin, ContractProgramPackageEditMixin, UpdateView):
    template_name = 'contract_management/contract_program_package/update.html'


# Удалить
class ContractProgramPackageDeleteView(ContractProgramPackageMixin, DeleteView):
    template_name = 'contract_management/contract_program_package/delete.html'
    

# Услуги пакета
class ContractProgramPackageServiceListView(LoginRequiredMixin, ListView):
    template_name = 'contract_management/contract_program_package_service/list.html'
    model = Service
    context_object_name = 'services'
    contract = None
    program = None
    package = None

    def dispatch(self, *args, **kwargs):
        self.contract = get_object_or_404(Contract, pk=self.kwargs.get('contract'))
        self.program = get_object_or_404(Program, pk=self.kwargs.get('program'))
        self.package = get_object_or_404(Package, pk=self.kwargs.get('package'))
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        package_services = PackageService.objects.filter(
            package=self.package).values_list('service')
        return qs.filter(id__in=package_services)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contract'] = self.contract
        context['program'] = self.program
        context['package'] = self.package
        return context
        
# Result list yeldos
class ContractProgramPackageResultListView(ContractProgramPackageServiceListView, ListView):
    template_name = 'contract_management/contract_result/list_result.html'

# Услуги пакета
class PackageServiceDeleteView(View):

    def post(self, request, *args, **kwargs):
        package = get_object_or_404(Package, pk=kwargs.get('package'))
        service = get_object_or_404(Service, pk=kwargs.get('service'))
        service_descendants = service.get_descendants(include_self=True)
        package_service = PackageService.objects.filter(package=package, service__in=service_descendants)
        if package_service.exists():
            package_service.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


# Услуги пакета
class HospitalPackageStatusUpdate(View):

    def post(self, request, *args, **kwargs):
        hospital_package = get_object_or_404(HospitalPackage, pk=kwargs.get('pk'))
        hospital_package.status = request.POST.get('status')
        hospital_package.save()
        return JsonResponse({'success': True})


class ProgramBlankCreateView(LoginRequiredMixin, CreateView):
    template_name = 'contract_management/program_blank/create.html'
    model = Program
    form_class = ProgramBlankForm
    contract = None

    def dispatch(self, *args, **kwargs):
        self.contract = get_object_or_404(Contract, pk=self.kwargs.get('contract'))
        return super(ProgramBlankCreateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        contract = self.kwargs.get('contract')
        return reverse_lazy('contract_management:contract_program_list',
                            kwargs={'contract': contract})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contract'] = self.contract
        return context

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(ProgramBlankCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["contract"] = self.contract
        return form_kwargs


# Mixin программы
class ContractCustomerMixin(LoginRequiredMixin):
    model = ContractCustomer
    success_url = reverse_lazy('contract_management:contract_customer_list')


class ContractCustomerEditMixin:
    form_class = ContractCustomerForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['contracts'] = Contract.objects.all()
        return context


# Список карт клиентов
class ContractCustomerListView(ContractCustomerMixin, ListView):
    template_name = 'contract_management/contract_customer/list.html'
    context_object_name = 'customer_cards'
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset()
        self.insurance = self.request.GET.get('insurance', None)
        self.insurer = self.request.GET.get('insurer', None)
        self.contract = self.request.GET.get('contract', None)
        self.program = self.request.GET.get('program', None)
        self.customer = self.request.GET.get('customer', None)
        if self.insurance:
            qs = qs.filter(contract__insurance__id=self.insurance)
        if self.insurer:
            qs = qs.filter(contract__insurer__id=self.insurer)
        if self.contract:
            qs = qs.filter(contract__id=self.contract)
        if self.program:
            qs = qs.filter(program__id=self.program)
        if self.customer:
            qs = qs.filter(customer__iin__icontains=self.customer)    
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        insurances = Insurance.objects.all()
        insurer = Insurer.objects.all()
        contracts = Contract.objects.all()
        programs = Program.objects.all()
        if self.insurance:
            contracts = contracts.filter(insurance__id=self.insurance)
        if self.insurer:
            contracts = contracts.filter(insurer__id=self.insurer)
        if self.contract:
            programs = programs.filter(contract__id=self.contract)
        context['referrals'] = Program.objects.values('contract__id', 'contract__number').distinct()
        context['insurances'] = insurances
        context['insurer'] = insurer
        context['contracts'] = contracts
        context['programs'] = programs
        return context


class ContractCustomerCreateView(ContractCustomerMixin, ContractCustomerEditMixin, CreateView):
    template_name = 'contract_management/contract_customer/create.html'


class ContractCustomerDetailView(ContractCustomerMixin, ContractCustomerEditMixin, DetailView):
    template_name = 'contract_management/contract_customer/detail.html'
    context_object_name = 'contract_customer'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['referrals'] = Referral.objects.filter(contract_customer=self.object).all()
        context['invoices'] = Invoice.objects.filter(contract_customer=self.object).all()
        return context


class ContractCustomerDeleteView(ContractCustomerMixin, DeleteView):
    template_name = 'contract_management/contract_customer/delete.html'


# Mixin программы
class ContractHospitalMixin(LoginRequiredMixin):
    model = ContractHospital
    success_url = reverse_lazy('contract_management:contract_hospital_list')
    context_object_name = 'contract_hospitals'
    paginate_by = 100


class ContractHospitalEditMixin:
    form_class = ContractHospitalForm


# Список карт клиентов
class ContractHospitalListView(ContractHospitalMixin, ListView):
    template_name = 'contract_management/contract_hospital/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.values('hospital', 'contract').distinct()


# Список карт клиентов
class ContractHospitalConfirmListView(ContractHospitalMixin, ListView):
    template_name = 'contract_management/contract_hospital_confirm/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        hospital = self.request.user.hospital
        return qs.filter(hospital=hospital).values('hospital', 'contract').distinct()


class ContractHospitalCreateView(ContractHospitalMixin, ContractHospitalEditMixin, CreateView):
    template_name = 'contract_management/contract_hospital/create.html'


class ContractHospitalUpdateView(ContractHospitalMixin, ContractHospitalEditMixin, UpdateView):
    template_name = 'contract_management/contract_hospital/update.html'


class ContractHospitalDeleteView(ContractHospitalMixin, DeleteView):
    template_name = 'contract_management/contract_hospital/delete.html'


# Получить список программ, при выборе контракта (ajax)
class ProgramByContractView(TemplateResponseMixin, View):
    template_name = 'contract_management/program_by_contract/list.html'

    def get(self, request, *args, **kwargs):
        contract = kwargs.get('contract')
        programs = Program.objects.filter(contract_id=contract)
        return self.render_to_response({'programs': programs})


class ContractHospitalPackageMixin(LoginRequiredMixin):
    model = HospitalPackage
    context_object_name = 'hospital_packages'

    def get_queryset(self):
        qs = super().get_queryset()
        contract_hospital = self.kwargs.get('contract_hospital')
        hospital = self.kwargs.get('hospital')
        return qs.filter(hospital=hospital, contract_hospital=contract_hospital)

    def get_success_url(self):
        contract_hospital = self.kwargs.get('contract_hospital')
        hospital = self.kwargs.get('hospital')
        return reverse_lazy('contract_management:contract_hospital_package_list',
                            kwargs={'hospital': hospital, 'contract_hospital': contract_hospital})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hospital'] = get_object_or_404(Hospital, pk=self.kwargs.get('hospital'))
        context['contract_hospital'] = get_object_or_404(ContractHospital, pk=self.kwargs.get('contract_hospital'))
        return context


class HospitalPackageEditMixin:
    form_class = HospitalPackageForm


# Услуги пакета
class ContractHospitalPackageListView(ContractHospitalPackageMixin, ListView):
    template_name = 'contract_management/contract_hospital_package/list.html'


# Обновить программу
class ContractHospitalPackageUpdateView(ContractHospitalPackageMixin, HospitalPackageEditMixin, UpdateView):
    template_name = 'contract_management/contract_hospital_package/update.html'


class ContractHospitalPackageDeleteView(ContractHospitalPackageMixin, DeleteView):
    template_name = 'contract_management/contract_hospital_package/delete.html'


class ContractHospitalPackageServiceMixin:
    model = Service
    context_object_name = 'services'
    hospital = None
    hospital_package = None
    contract_hospital = None

    def dispatch(self, *args, **kwargs):
        self.hospital = get_object_or_404(Hospital, pk=self.kwargs.get('hospital'))
        self.hospital_package = get_object_or_404(HospitalPackage, pk=self.kwargs.get('hospital_package'))
        self.contract_hospital = get_object_or_404(ContractHospital, pk=self.kwargs.get('contract_hospital'))
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        hospital_package_services = HospitalPackageService.objects.filter(
            hospital_package=self.hospital_package).values_list('service', flat=True)
        return qs.filter(id__in=hospital_package_services)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hospital'] = self.hospital
        context['hospital_package'] = self.hospital_package
        context['contract_hospital'] = self.contract_hospital
        return context


# Услуги пакета
class ContractHospitalPackageServiceListView(ContractHospitalPackageServiceMixin, ListView):
    template_name = 'contract_management/contract_hospital_package_service/list.html'







class ContractHospitalServiceMixin:
    model = HospitalPackage
    context_object_name = 'hospital_packages'
    hospital = None
    hospital_packages = None
    contract_hospital = None

    def dispatch(self, *args, **kwargs):
        self.hospital = get_object_or_404(Hospital, pk=self.kwargs.get('hospital'))
        self.contract_hospital = get_object_or_404(ContractHospital, pk=self.kwargs.get('contract_hospital'))
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(contract_hospital=self.contract_hospital)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hospital'] = self.hospital
        context['contract_hospital'] = self.contract_hospital
        return context


# Услуги пакета
class ContractHospitalServiceListView(ContractHospitalServiceMixin, ListView):
    template_name = 'contract_management/contract_hospital_service/list.html'



# Услуги пакета
class ContractHospitalServiceExcelView(ContractHospitalPackageMixin, ListView):
    template_name = 'contract_management/contract_hospital_service/excel.html'

# Услуги пакета договор
class ContractHospitalServiceTreatyListView(ContractHospitalPackageMixin, ListView):
    template_name = 'contract_management/contract_hospital_service/treaty_list.html'


# Услуги пакета
class HospitalPackageServiceFormView(View):

    def post(self, request, *args, **kwargs):
        hospital_package = get_object_or_404(HospitalPackage, pk=kwargs.get('hospital_package'))
        service = get_object_or_404(Service, pk=request.POST.get('service'))
        hospital_package_service, created = HospitalPackageService.objects.get_or_create(
            hospital_package=hospital_package, service=service
        )
        form = HospitalPackageServiceForm(request.POST, instance=hospital_package_service)
        print('test..........')
        print(form.errors)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})



# Услуги пакета
class HospitalPackageServiceExportView(View):

    def get(self, request, *args, **kwargs):
        contract_hospital = self.kwargs.get('contract_hospital')
        resource = HospitalPackageServiceResource()
        queryset = HospitalPackageService.objects.filter(
            hospital_package__contract_hospital__id=contract_hospital)
        dataset = resource.export(queryset)
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="persons.xls"'
        return response


# Услуги пакета
class ContractHospitalPackageServiceListView(ContractHospitalPackageServiceMixin, ListView):
    template_name = 'contract_management/contract_hospital_package_service/list.html'


# Услуги пакета
class HospitalListView(ListView):
    model = Hospital
    context_object_name = 'hospitals'
    template_name = 'contract_management/hospital/list.html'


# Услуги пакета
class HospitalUpdateView(View):
    
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        is_checked = request.POST.get('is_checked', 'true')
        if is_checked == 'true':
            is_checked = True
        else:
            is_checked = False
        hospital = get_object_or_404(Hospital, pk=pk)
        hospital.is_checked =  is_checked
        hospital.save() 
        return JsonResponse({'success': True})


# Услуги пакета
class InsuranceListView(ListView):
    model = Insurance
    context_object_name = 'insurances'
    template_name = 'contract_management/insurance/list.html'


# Услуги пакета
class InsuranceUpdateView(View):
    
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        is_checked = request.POST.get('is_checked', 'true')
        if is_checked == 'true':
            is_checked = True
        else:
            is_checked = False
        insurance = get_object_or_404(Insurance, pk=pk)
        insurance.is_checked =  is_checked
        insurance.save() 
        return JsonResponse({'success': True})


# Услуги пакета
class ContractHospitalStatusUpdateView(View):
    
    def post(self, request, *args, **kwargs):
        contract = request.POST.get('contract')
        hospital = request.POST.get('hospital')
        status = request.POST.get('status')
        contract_hospital = ContractHospital.objects.filter(
            contract__id=contract, hospital__id=hospital).update(status=status)
        return JsonResponse({'success': True})

