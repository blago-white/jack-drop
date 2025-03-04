import { printPrizeItem } from "./animations.js";

const depoAmountField = document.getElementById('amount');
const agreementInput = document.getElementById('agreement');
let usedPromocode = document.getElementById('used-promocode');
let selectedProvider;

const SKINIFYSELECTOR = "S";
const NICEPAYSELECTOR = "N";

if (usedPromocode && (usedPromocode != "None")) {
    usedPromocode = usedPromocode.innerHTML
    const hasPresetedPromocode = usedPromocode.length > 0;
}

async function getBenefitPercent(promocode) {
    if (!promocode) {
        return
    }

    const headers = new Headers();

    headers.append("Content-Type", "application/json");

    const response = await sendRequest(`/auth/discount/api/v1/public/promo-benefits/?promocode=${promocode}`, {
        method: "GET",
        headers: headers
    });

    if (!response.ok) {
        return 0;
    }

    const responseJSON = await response.json();

    return parseInt(responseJSON.discount);
}

async function showBenegits(promocode) {
    const benefitPercent = await getBenefitPercent(promocode);

    if (benefitPercent > 0) {
        document.getElementById("promocodeBenefits").style = "";
        document.getElementById("promocodeBenefits").innerHTML = `Вы получите: +${benefitPercent}% к депозиту!`;
    }

    return false;
}

function validate() {
    const amount = parseFloat(depoAmountField.value);

    const agree = agreementInput.checked;

    if (selectedProvider == NICEPAYSELECTOR) {
        return (agree && amount >= 500);
    } else {
        return agree;
    }
}

function updateSubmitBtn() {
    if (validate()) {
        document.getElementById('replenish-btn-bg').classList.remove("noactive");
        document.getElementById('replenish-btn-bg').onclick = () => {addDeposit()};
    } else {
        document.getElementById('replenish-btn-bg').classList.add("noactive");
        document.getElementById('replenish-btn-bg').onclick = () => {return false};
    }
}

async function addDeposit() {
    if (!agreement) {return}

    const user = await getAuthenticated();

    if (!user) {
        return makeWarn("Всего пара шагов до вашей первой победы", "Зарегистрируйтесь и пополните баланс прямо сейчас!")
    }

    const amount = parseFloat(depoAmountField.value);
    const headers = new Headers();

    const promocode = document.getElementById('promocode').value;

    headers.append("Content-Type", "application/json");

    let response;

    if (selectedProvider == NICEPAYSELECTOR) {
        response = await sendRequest('/transactions/payments/create/', {
            method: "POST",
            body: JSON.stringify({"amount": amount, "promocode": promocode}),
            headers: headers
        });
    } else {
        response = await sendRequest('/transactions/payments/create-skinify/', {
            method: "POST",
            body: JSON.stringify({"promocode": promocode}),
            headers: headers
        });
    }

    const responseJSON = await response.json();

    if (!response.ok) {
        document.getElementById('replenish-form').style.outline = '1px solid firebrick'

        makeWarn(responseJSON.description)
    } else {
        location.href = responseJSON.payment_url;
    }

    return false;
}

window.addDeposit = addDeposit;

if (document.getElementById("agreement") && document.getElementById("amount")) {
    document.getElementById("agreement").addEventListener('input', updateSubmitBtn);
    document.getElementById("amount").addEventListener('input', updateSubmitBtn);
}

function usePreset(preset) {
    document.getElementById('amount').value = preset;

    updateSubmitBtn();
    return false;
}

function selectSkinify() {
    document.getElementById("nicepaySelector").classList.remove("selected");
    document.getElementById("skinifySelector").classList.add("selected");

    document.getElementById("amountSelectorRow").classList.add("blocked");

    selectedProvider = SKINIFYSELECTOR;

    updateSubmitBtn();
}

function selectNicepay() {
    document.getElementById("skinifySelector").classList.remove("selected");
    document.getElementById("nicepaySelector").classList.add("selected");

    document.getElementById("amountSelectorRow").classList.remove("blocked");

    selectedProvider = NICEPAYSELECTOR;

    updateSubmitBtn();
}

function getRandomArbitrary(min, max) {
    return Math.random() * (max - min) + min;
}

const urlParams = new URLSearchParams(window.location.search);

window.usePreset = usePreset;

if (document.getElementById("promocode").value.length>1) {
    document.getElementById("promocode").style.outline = "3px solid #602ccd";

    showBenegits(document.getElementById("promocode").value);
}

document.getElementById("nicepaySelector").addEventListener("click", selectNicepay);
document.getElementById("skinifySelector").addEventListener("click", selectSkinify);

window.showBenegits = showBenegits;

selectedProvider = SKINIFYSELECTOR;
