from django import views
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from mainapp.models import Organization, BranchOffice, Department, Employee, OrganizationBankAccount
from kadr.models import EmployeeCard
from guide.models import Bank, Address
from mainapp.forms import LoginForm, RegistrationForm


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


class RegistrationView(views.View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']

            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                birth_date=form.cleaned_data['birth_date'],
                phone=form.cleaned_data['phone'],
                agreement=form.cleaned_data['agreement'],
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/catalog')
        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context)


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
