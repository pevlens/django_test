from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .forms import RegisterUserForm, LoginUserForm, UrlForm
from django.contrib.auth.decorators import login_required
from .models import Link
from django.db.utils import IntegrityError

import random
# Create your views here.

@login_required
def homepage(request, slug):
    l = Link.objects.get(slug = slug)
    return redirect(l.link)

class LoginForm(LoginView):

    form_class = LoginUserForm
    template_name = "login.html"

    def get_success_url(self):
        return reverse_lazy('startpage')



class HomePage(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = ""
    form_class = UrlForm 
    template_name = "link_input.html"
    success_url = reverse_lazy("startpage")
    context_object_name = 'post'
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            form.instance.slug = slug_generic()
            resault = super().form_valid(form)
            return resault
        except IntegrityError:
            return redirect("startpage")
                
            
        
    def get_context_data(self, object_list = None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['link'] = Link.objects.filter(user=self.request.user).count()
        return context


class RegisterUser(CreateView):
    
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('startpage')



class ListLink(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = "link"
    model = Link
    template_name = 'list_link.html'
    context_object_name  = "links"
     
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = f"{self.request.META.get('REMOTE_ADDR')}:{self.request.META.get('SERVER_PORT')}"
        context['ip'] = str(ip)
        return context
    

    def get_queryset(self):
        return Link.objects.filter(user = self.request.user).all()

def logout_user(request):
    logout(request)
    return redirect('login')









def slug_generic():
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    while True:
        length = random.randint(1, 10)
        password = ''
        for i in range(length):
            password += random.choice(chars)
        try:
            _ = Link.objects.get(slug = password)

        except  Link.DoesNotExist:
            return password
           