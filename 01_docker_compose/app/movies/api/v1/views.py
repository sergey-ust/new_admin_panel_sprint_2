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

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = MOVIES_PER_PAGE

    def get_queryset(self) -> QuerySet[FilmWork]:
        return self.model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs) -> MoviesList:
        page_number = int(self.request.GET.get('page', "0"))
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        pg = paginator.get_page(page_number)
        context = {
            'count': paginator.count,
            "total_pages": paginator.num_pages,
            "prev": pg.previous_page_number(),
            "next": pg.next_page_number(),
            'results': pg.object_list,
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_queryset(self) -> QuerySet[FilmWork]:
        return self.model.objects.filter(pk=self.kwargs.get('pk'))

    def get(self, request, pk, *args, **kwargs):
        queryset = self.get_queryset()
        movie = queryset.get()
        context = {
            "title": movie.title,
        }
        return JsonResponse(context)
