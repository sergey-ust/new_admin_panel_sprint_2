from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import QuerySet, Q
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

    @staticmethod
    def model_to_dict(fw_queryset: QuerySet) -> dict:
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
        queryset = fw_queryset.annotate(genre_list=genre_list).annotate(
            actors=actors).annotate(directors=directors).annotate(
            writers=writers)

        tmp = list(queryset.values().all())
        context = list()
        for entry in tmp:
            res = {
                ("genres" if k == "genre_list" else k): v for (k, v) in
                entry.items()
            }
            del res["created"], res["modified"]
            context.append(res)

        return context


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = MOVIES_PER_PAGE

    def get_context_data(self, *, object_list=None, **kwargs) -> MoviesList:
        queryset = self.object_list
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        context = {
            'count': paginator.count,
            "total_pages": paginator.num_pages,
            "prev":
                page.previous_page_number() if page.has_previous() else None,
            "next":
                page.next_page_number() if page.has_next() else None,
            "results": self.model_to_dict(queryset),
        }

        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get(self, request, pk, *args, **kwargs) -> JsonResponse:
        queryset = self.model.objects.filter(pk=pk)
        context = self.model_to_dict(queryset)
        return JsonResponse(context[0])
