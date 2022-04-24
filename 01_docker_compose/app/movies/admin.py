"""Admin panel models."""

from django.contrib import admin
from django.db.models import Prefetch

from movies import models as mov_model


@admin.register(mov_model.Genre)
class GenreAdmin(admin.ModelAdmin):
    """Admin model for ORM model "Genre"."""


@admin.register(mov_model.Person)
class PersonAdmin(admin.ModelAdmin):
    """Admin model for ORM model "Person"."""
    ordering = ['full_name']
    search_fields = ['full_name']


class _GenreFilmWorkInline(admin.TabularInline):
    model = mov_model.GenreFilmWork


class _PersonFilmWorkInline(admin.StackedInline):
    model = mov_model.PersonFilmWork
    autocomplete_fields = ['person']
    list_prefetch_related = (Prefetch('film_work'), Prefetch('person'))

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            *self.list_prefetch_related
        ).all()


@admin.register(mov_model.FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    """Admin model for ORM model "FilmWork"."""

    inlines = (_GenreFilmWorkInline, _PersonFilmWorkInline)
    list_display = (
        'title',
        'type',
        'creation_date',
    )
    search_fields = ('title', 'description')
    list_filter = ('type',)
    list_prefetch_related = (Prefetch('genres'), Prefetch('person'))

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            *self.list_prefetch_related
        ).all()
