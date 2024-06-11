from django.shortcuts import render


def test_ws_view(request):
    return render(request, "testsoc.html")
