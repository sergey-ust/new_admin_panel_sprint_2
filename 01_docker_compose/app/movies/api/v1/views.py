from django.http import JsonResponse
from django.views import View


class MoviesListApi(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return JsonResponse({})
