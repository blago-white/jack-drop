from django.shortcuts import render


def test_base_view(request):
    return render(request,
                  template_name="base.html")
