from django import forms
from core.models import Movie, Vote, MovieImage
from django.contrib.auth import get_user_model

class VoteForm(forms.ModelForm):

    user = forms.ModelChoiceField(
                            widget=forms.HiddenInput,
                            queryset=get_user_model().objects.all(),
                            disabled=True)
    movie = forms.ModelChoiceField(
                            widget=forms.HiddenInput,
                            queryset=Movie.objects.all(),
                            disabled=True)
    value = forms.ChoiceField(
                            label='Vote',
                            widget=forms.RadioSelect,
                            choices=Vote.VALUE_CHOICES)
    
    class Meta:
        model = Vote
        fields = ('user', 'movie', 'value')

class MovieImageForm(forms.ModelForm):

    user = forms.ModelChoiceField(
                            widget=forms.HiddenInput,
                            queryset=get_user_model().objects.all(),
                            disabled=True)
                            
    movie = forms.ModelChoiceField(
                            widget=forms.HiddenInput,
                            queryset=Movie.objects.all(),
                            disabled=True)
    
    class Meta:
        model = MovieImage
        fields = ('user', 'movie', 'image')