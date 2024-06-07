from django.shortcuts import render


def main_page_view(request):
    return render(request, template_name="mainpage.html")


def account_view(request):
    return render(request, template_name="account.html")


def mines_view(request):
    return render(request, template_name="mines.html")


def battle_view(request):
    return render(request, template_name="battle.html")
