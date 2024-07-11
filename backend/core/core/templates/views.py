from django.http.request import HttpRequest
from django.shortcuts import render


def main_page_view(request: HttpRequest):
    context = {}

    if request.GET.get("min"):
        context.update(min_case_price=request.GET.get("min"))
    if request.GET.get("max"):
        context.update(max_case_price=request.GET.get("max"))
    if request.GET.get("cat"):
        context.update(case_category=request.GET.get("cat"))

    return render(request,
                  template_name="mainpage.html",
                  context={
                      "min_case_price": request.GET.get("min"),
                      "max_case_price": request.GET.get("max"),
                      "case_category": request.GET.get("cat")
                  })


def account_view(request):
    return render(request,
                  template_name="account.html")


def mines_view(request):
    return render(request,
                  template_name="mines.html",
                  context={"section": "mines"})


def battle_view(request):
    return render(request,
                  template_name="battle.html",
                  context={"section": "battle"})


def upgrade_view(request):
    return render(request,
                  template_name="upgrade.html",
                  context={"section": "upgrade"})


def contract_view(request):
    return render(request,
                  template_name="contract.html",
                  context={"section": "contract"})


def case_view(request, case_id):
    return render(request,
                  template_name="case.html",
                  context={"case_id": case_id})


def case_drop_view(request, case_id):
    return render(request,
                  template_name="case-drop.html",
                  context={"case_id": case_id})


def inventory_view(request):
    return render(request,
                  template_name="inventory/inventory.html",
                  context={"case_id": "inventory"})


def replenish_view(request):
    return render(request,
                  template_name="replenish.html")


def fortune_wheel_view(request):
    return render(request=request,
                  template_name="fortune.html")


def privacy_policy_view(request):
    return render(request=request,
                  template_name="privacy.html")


def user_agreement_view(request):
    return render(request=request,
                  template_name="agreement.html")


def about_view(request):
    return render(
        request=request,
        template_name="about.html"
    )


def tos_view(request):
    return render(
        request=request,
        template_name="terms.html"
    )


def game_history_view(request):
    return render(
        request=request,
        template_name="game-history.html"
    )


def withdraws_view(request):
    return render(
        request=request,
        template_name="withdraws.html"
    )


def bonus_buy_view(request):
    return render(
        request=request,
        template_name="bonus-buy.html"
    )
