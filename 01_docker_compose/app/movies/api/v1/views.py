from django.db.models import QuerySet
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import FilmWork

MoviesList = dict[int, int, int, int, list]

MOVIES_PER_PAGE = 50


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self) -> QuerySet[FilmWork]:
        return self.model.objects.all()

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(BaseListView, MoviesApiMixin):
    paginate_by = MOVIES_PER_PAGE

    # def get_queryset(self) -> QuerySet[FilmWork]:
    #     return self.model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs) -> MoviesList:
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        context = {
            'count': paginator.count,
            "total_pages": 0,
            "prev": 0,
            "next": 0,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return {
            "comments": "no"
        }
