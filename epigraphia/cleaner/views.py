from django.shortcuts import render, redirect
from django.views import View
from . import forms
from epiclean import clean_epigraphia

# Create your views here.


class Cleaner(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect('/admin/login/?next=/cleaner/')

        form = forms.CleanerForm()
        context = {
            'form': form
        }
        return render(request, 'cleaner_page.html', context)

    def post(self, request):

        if not request.user.is_authenticated:
            return redirect('/admin/login/?next=/cleaner/')

        form = forms.CleanerForm(request.POST)
        if form.is_valid():
            output_str = clean_epigraphia.processor(form.cleaned_data['input_str'], form.cleaned_data['lang'],
                                                    form.cleaned_data['process_e'], form.cleaned_data['process_o'],
                                                    form.cleaned_data['process_s'], form.cleaned_data['process_n'])
            context = {
                'form': form,
                'output_str': output_str
            }
        else:
            context = {
                'form': form,
                'error_msg': 'Something went wrong'
            }
        return render(request, 'cleaner_page.html', context)
