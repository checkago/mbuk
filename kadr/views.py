from django.shortcuts import render, get_object_or_404
from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from kadr.models import EmployeeCard
from kadr.forms import EmployeeCardCreateForm


class EmployeeCardListView(LoginRequiredMixin, ListView):

    model = EmployeeCard
    template_name = 'mainapp/../templates/kadr/employeecard_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EmployeeCardCreateView(views.View):
    def get(self, request, *args, **kwargs):
        form = EmployeeCardCreateForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'kadr/employeecard_create.html', context)

    def post(self, request, *args, **kwargs):
        form = EmployeeCardCreateForm(request.POST or None)
        if form.is_valid():
            new_employeecard = form.save(commit=False)
            new_employeecard.employee = form.cleaned_data['employee']
            new_employeecard.r_first_name = form.cleaned_data['r_first_name']
            new_employeecard.r_last_name = form.cleaned_data['r_last_name']
            new_employeecard.r_middle_name = form.cleaned_data['r_middle_name']
            new_employeecard.d_first_name = form.cleaned_data['d_first_name']
            new_employeecard.d_last_name = form.cleaned_data['d_last_name']
            new_employeecard.d_middle_name = form.cleaned_data['d_middle_name']
            new_employeecard.position = form.cleaned_data['position']
            new_employeecard.birthday = form.cleaned_data['birthday']
            new_employeecard.save()
            return HttpResponseRedirect('/employees')
        context = {
            'form': form
        }
        return render(request, 'kadr/employeecard_create.html', context)


class EmployeeCardChangeView(views.View):
    def get(self, request, *args, **kwargs):
        form = EmployeeCardCreateForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'kadr/employeecard_change.html', context)

    def post(self, request, *args, **kwargs):
        form = EmployeeCardCreateForm(request.POST or None)
        if form.is_valid():
            new_employeecard = form.save(commit=False)
            new_employeecard.employee = form.cleaned_data['employee']
            new_employeecard.r_first_name = form.cleaned_data['r_first_name']
            new_employeecard.r_last_name = form.cleaned_data['r_last_name']
            new_employeecard.r_middle_name = form.cleaned_data['r_middle_name']
            new_employeecard.d_first_name = form.cleaned_data['d_first_name']
            new_employeecard.d_last_name = form.cleaned_data['d_last_name']
            new_employeecard.d_middle_name = form.cleaned_data['d_middle_name']
            new_employeecard.position = form.cleaned_data['position']
            new_employeecard.birthday = form.cleaned_data['birthday']
            new_employeecard.save()
            return HttpResponseRedirect('/employees')
        context = {
            'form': form
        }
        return render(request, 'kadr/employeecard_change.html', context)



def employee_card_view(request, pk):
    employee = get_object_or_404(EmployeeCard, pk=pk)
    title = employee.employee.last_name
    return render(request, 'kadr/employeecard_view.html', {'title': title, 'employee': employee})
