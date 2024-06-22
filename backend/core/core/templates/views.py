from django.shortcuts import render


def main_page_view(request):
    return render(request, template_name="mainpage.html")


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
