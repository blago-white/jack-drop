from django.shortcuts import render


def test_ws_view(request, k):
    return render(request,
                  "testsoc.html",
                  context={"k": k})
