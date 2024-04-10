from django.views.generic import RedirectView, CreateView


class SteamAuthView(RedirectView):
    def get(self, request, *args, **kwargs):
        return
