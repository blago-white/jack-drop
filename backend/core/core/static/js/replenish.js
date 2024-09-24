import { renderItemPrize, renderPrize } from "./prize.js";

const depoAmountField = document.getElementById('amount');
const agreementInput = document.getElementById('agreement');
const usedPromocode = document.getElementById('used-promo').innerHTML;
const hasPresetedPromocode = usedPromocode.length > 0;


function validate() {
    const amount = parseFloat(depoAmountField.value);

    const agree = agreementInput.checked;

    return (agree && amount >= 500);
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

    const amount = parseFloat(depoAmountField.value);
    const headers = new Headers();

    headers.append("Content-Type", "application/json");

    const response = await sendRequest('/transactions/payments/create/', {
        method: "POST",
        body: JSON.stringify({"amount": amount}),
        headers: headers
    });

    const responseJSON = await response.json();

    if (!response.ok) {
        document.getElementById('replenish-form').style.outline = '5px solid firebrick'

        alert(responseJSON.description)
    } else {
        location.href = responseJSON.payment_url;
    }
    return false;
}

window.addDeposit = addDeposit;

document.getElementById("agreement").addEventListener('input', updateSubmitBtn);
document.getElementById("amount").addEventListener('input', updateSubmitBtn);

function renderFreeCase(freeCase, caseImg, caseTitle) {
    const urlParams = new URLSearchParams(window.location.search);

    if (freeCase) {
        renderPrize(`
            <img src="${caseImg}">
            <h3 style="text-transform: none;">${caseTitle}</h3>
            <span style="font-size: xx-large;">0<img src="/core/static/img/scrap.png" style="width: 3ch"></span>
            <button class="super-button" style="font-family: 'Gilroy SemiBold'" onclick="closePrizeWindow('https://${location.hostname}')">
                <span class="super-button-bg"></span>
                <span class="super-button-text" style="font-size: x-large">Receive</span>
            </button>
        `);
    }
}


function renderDeposit(success, amount) {
    if (success) {
        renderPrize(`
            <img src="/core/static/img/scrap.png">
            <h3 style="text-transform: none;">Deposit: ${amount} scrap!</h3>
            <span style="font-size: xx-large;">${amount}<img src="/core/static/img/scrap.png" style="width: 3ch"></span>
            <button class="super-button" style="font-family: 'Gilroy SemiBold'" onclick="closePrizeWindow('https://${location.hostname}')">
                <span class="super-button-bg"></span>
                <span class="super-button-text" style="font-size: x-large">Receive</span>
            </button>
        `);
    } else {
    }
}


const urlParams = new URLSearchParams(window.location.search);

if (urlParams.get("deposit")) {
    renderDeposit(urlParams.get("success"), urlParams.get("amount"));
    const freeCase = urlParams.get('fc');

    if (freeCase) {
        const caseImg = urlParams.get('ci');
        const caseTitle = urlParams.get('ct');
    }

    if (freeCase && caseImg && caseTitle) {
        renderFreeCase(freeCase, caseImg, caseTitle);
    }
}
