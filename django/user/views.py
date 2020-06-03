from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class RegisterView(CreateView):
    templates = 'user/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('core:MovieList')