from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from mainapp.models import Organization, BranchOffice, Department, Employee, OrganizationBankAccount
from kadr.models import EmployeeCard
from mainapp.forms import LoginForm, UserCreateForm, EmployeeCreateForm
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginView(views.View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'accounts/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')

        context = {
            'form': form
        }
        return render(request, 'accounts/login.html', context)


class UserCreateView(views.View):

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']

            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return HttpResponseRedirect('/employees')
        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context)


class EmployeeCreateView(views.View):

    def get(self, request, *args, **kwargs):
        form = EmployeeCreateForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'mainapp/employee_create.html', context)

    def post(self, request, *args, **kwargs):
        form = EmployeeCreateForm(request.POST or None)
        if form.is_valid():
            new_employee = form.save(commit=False)
            new_employee.user = form.cleaned_data['user']
            new_employee.first_name = form.cleaned_data['first_name']
            new_employee.last_name = form.cleaned_data['last_name']
            new_employee.middle_name = form.cleaned_data['middle_name']
            new_employee.position = form.cleaned_data['position']
            new_employee.birthday = form.cleaned_data['birthday']
            new_employee.save()
            return HttpResponseRedirect('/employees')
        context = {
            'form': form
        }
        return render(request, 'mainapp/employee_create.html', context)


class IndexView(LoginRequiredMixin, views.View):

    def get(self, request, *args, **kwargs):
        organization = Organization.objects.all().filter(primary=True)
        branch_offices = BranchOffice.objects.all()
        departments = Department.objects.all()
        bank_accounts = OrganizationBankAccount.objects.all()
        employees = Employee.objects.all()
        context = {
            'organization': organization,
            'branch_offices': branch_offices,
            'departments': departments,
            'bank_accounts': bank_accounts,
            'employees': employees
        }
        return render(request, 'index.html', context)


class OrganizationListView(LoginRequiredMixin, ListView):

    model = Organization

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EmployeeListView(LoginRequiredMixin, ListView):

    model = EmployeeCard
    template_name = 'mainapp/employee_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
