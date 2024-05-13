from django.views.generic import RedirectView


class SteamAuthView(RedirectView):
    def get(self, request, *args, **kwargs):
        # TODO: Make steam authentication view

        return
