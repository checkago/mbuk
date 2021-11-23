from django import views
from django.shortcuts import render
from mainapp.models import Organization, BranchOffice, Department, Employee, BankAccount
from guide.models import Bank, Address


class IndexView(views.View):

    def get(self, request, *args, **kwargs):
        organization = Organization.objects.all()
        branch_offices = BranchOffice.objects.all()
        departments = Department.objects.all()
        bank_accounts = BankAccount.objects.all()
        employees = Employee.objects.all()
        context = {
            'organization': organization,
            'branch_offices': branch_offices,
            'departments': departments,
            'bank_accounts': bank_accounts,
            'employees': employees
        }
        return render(request, 'index.html', context)

class LoginView(views.View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'auth/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/catalog')

        context = {
            'form': form
        }
        return render(request, 'sign-in.html', context)


class RegistrationView(views.View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'auth/registration.html', context)

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
        return render(request, 'sign-up.html', context)
