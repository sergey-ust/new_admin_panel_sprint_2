from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import QuerySet, Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import FilmWork

MoviesList = dict[int, int, int, int, list]

MOVIES_PER_PAGE = 50


def prepare_answer(queryset: QuerySet) -> dict:
    genre_list = ArrayAgg('genres__name', distinct=True)
    actors = ArrayAgg(
        'person__full_name',
        filter=Q(person__personfilmwork__role="actor"),
        distinct=True
    )
    directors = ArrayAgg(
        'person__full_name',
        filter=Q(person__personfilmwork__role="director"),
        distinct=True
    )
    writers = ArrayAgg(
        'person__full_name',
        filter=Q(person__personfilmwork__role="writer"),
        distinct=True
    )
    queryset = queryset.annotate(genre_list=genre_list)
    queryset = queryset.annotate(actors=actors)
    queryset = queryset.annotate(directors=directors)
    queryset = queryset.annotate(writers=writers)

    context = queryset.values()[0]
    context["genres"] = context.pop("genre_list")
    return context


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self) -> QuerySet[FilmWork]:
        return self.model.objects.all()

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = MOVIES_PER_PAGE

    @staticmethod
    def filwork_to_dict(filmwork: FilmWork):
        context = dict(vars(filmwork))
        del context["_state"], context["created"], context["modified"]
        context["genres"] = list(
            filmwork.genres.values_list("name", flat=True)
        )
        persons = list(
            filmwork.person.values("personfilmwork__role", "full_name")
        )
        context["actors"] = list()
        context["directors"] = list()
        context["writers"] = list()
        roles = {
            "actor": context["actors"],
            "director": context["directors"],
            "writer": context["writers"]
        }
        for entry in persons:
            if (role := entry["personfilmwork__role"]) in roles:
                roles[role].append(entry["full_name"])
        return context

    def get_context_data(self, *, object_list=None, **kwargs) -> MoviesList:
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        context = {
            'count': paginator.count,
            "total_pages": paginator.num_pages,
            "prev":
                page.previous_page_number() if page.has_previous() else page.number,
            "next":
                page.next_page_number() if page.has_next() else page.number,
            'results': [self.filwork_to_dict(entry) for entry in queryset],
        }

        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        filmwork: FilmWork = kwargs["object"]
        context = dict(vars(filmwork))
        del context["_state"], context["created"], context["modified"]
        context["genres"] = list(
            filmwork.genres.values_list("name", flat=True)
        )
        persons = list(
            filmwork.person.values("personfilmwork__role", "full_name")
        )
        context["actors"] = list()
        context["directors"] = list()
        context["writers"] = list()
        roles = {
            "actor": context["actors"],
            "director": context["directors"],
            "writer": context["writers"]
        }
        for entry in persons:
            if (role := entry["personfilmwork__role"]) in roles:
                roles[role].append(entry["full_name"])
        return context
