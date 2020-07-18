from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.views.generic import (ListView, DetailView, CreateView, UpdateView)
from core.models import Movie, Person, Vote
from django.urls import reverse
from core.forms import VoteForm, MovieImageForm

from django.contrib.auth.mixins import LoginRequiredMixin

class MovieList(ListView):
    model = Movie

class MovieDetail(DetailView):
    # model = Movie
    queryset = Movie.objects.all_with_related_persons_and_score()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["image_form"] = self.movie_image_form()
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                                            movie=self.object, 
                                            user=self.request.user)
            if vote.id:
                vote_form_url = reverse(
                                'core:update_vote',
                                kwargs={
                                    'movie_id': vote.movie.id,
                                    'pk': vote.id})
            else:
                vote_form_url = reverse(
                                    'core:create_vote',
                                    kwargs={
                                    'movie_id':self.object.id})
                # print(vote_form_url)
            vote_form = VoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_form_url'] = vote_form_url
        
        return ctx

    def movie_image_form(self):
        if self.request.user.is_authenticated:
            return MovieImageForm
        return None

class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()

class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']

        return initial
    
    def get_success_url(self):
        movie_id = self.object.movie.id
        print(movie_id)

        return reverse(
                    'core:movie_detail',
                        kwargs={
                        'pk': movie_id})
    
    def render_to_response(self, context, **response_kwargs):
        movie_id = context['movie_id']
        print(movie_id)

        movie_detail_url = reverse(
                    'core:movie_detail',
                    kwargs={
                        'pk': movie_id})
        return redirect(to=movie_detail_url)

class UpdateVote(LoginRequiredMixin, UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied("cannot change vote. Users vote")

        return vote
        
    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse(
                    "core:movie_detail",
                    kwargs = {
                        "pk": movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context["movie_id"]
        movie_detail_url = reverse(
                            "core:movie_detail",
                            kwargs = {
                                "pk": movie_id})
        return redirect(to=movie_detail_url)

class MovieImageUpload(LoginRequiredMixin, CreateView):
    print("if it worked")
    form_class = MovieImageForm
    print(form_class)

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial["movie"] = self.kwargs["movie_id"]

        return initial

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse(
                    "core:movie_detail",
                    kwargs = {
                        "pk": movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = self.kwargs["movie_id"]
        movie_detail_url = reverse("core:movie_detail",
                         kwargs={"pk": movie_id})
        return redirect(to=movie_detail_url)
        

class TopView(ListView):
    template_name = "core/top_movies_list.html"
    queryset = Movie.objects.top_movies(limit=10)
    context_object_name = "top_movies"
    

        
        