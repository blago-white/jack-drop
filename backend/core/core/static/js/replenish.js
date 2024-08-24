import { renderItemPrize, renderPrize } from "./prize.js";

const paymentsMethodsMapping = {
    1: "card",
    2: "crypto",
    3: "skinify"
}

const depoAmountField = document.getElementById('amount');
const agreementInput = document.getElementById('agreement');
let paymentMethodId;


function validate() {
    const amount = parseFloat(depoAmountField.value);

    const agree = agreementInput.checked;

    return (agree && amount >= 500 && paymentMethodId);
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

function setPaymentMethod(methodid) {
    if (!paymentsMethodsMapping[methodid]) {
        alert("Not correct payment method choosen")
        return false;
    }

    paymentMethodId = methodid;

    updateSubmitBtn();
}

async function addDeposit() {
    if (!agreement) {
        return
    }

    const amount = parseFloat(depoAmountField.value);
    const headers = new Headers();

    headers.append("Content-Type", "application/json");

    const response = await sendRequest('/transactions/payments/create/', {
        method: "POST",
        body: JSON.stringify({"amount": amount, "pay_method": paymentMethodId == 1 ? "R" : "C"}),
        headers: headers
    });

    if (!response.ok) {
        document.getElementById('replenish-form').style.outline = '5px solid firebrick'
    } else {
        const result = await response.json();

//        const responseAddCase = await sendRequest('/products/bonus-buy/add-for-deposit/', {
//            method: "POST",
//            body: JSON.stringify({"deposit_id": result.id, "deposit_amount": amount}),
//            headers: headers
//        });
//
//        if (!responseAddCase.ok) {
//            renderItemPrize(
//            "Scrap", amount, "/core/static/img/scrap.png", "Receive"
//            );
//            return;
//        }
//
//        const resultAddCase = await responseAddCase.json();
//
//        renderPrize(`
//            <img src="/core/static/img/scrap.png">
//            <h3 style="text-transform: none;">Scrap</h3>
//            <span style="font-size: xx-large;">${amount}<img src="/core/static/img/scrap.png" style="width: 3ch"></span>
//            <button class="super-button"
//                    style="font-family: 'Gilroy SemiBold'"
//                    onclick="location.href += '?fc=1&ci=${resultAddCase.case.image_path}&ct=${resultAddCase.case.title}';">
//                <span class="super-button-bg"></span>
//                <span class="super-button-text" style="font-size: x-large">Receive</span>
//            </button>
//        `);
    }

    return false;
}

window.addDeposit = addDeposit;
window.setPaymentMethod = setPaymentMethod;

document.getElementById("agreement").addEventListener('input', updateSubmitBtn);
document.getElementById("amount").addEventListener('input', updateSubmitBtn);

function renderFreeCase() {
    const urlParams = new URLSearchParams(window.location.search);

    const freeCase = urlParams.get('fc');

    if (freeCase) {
        const caseImg = urlParams.get('ci');
        const caseTitle = urlParams.get('ct');

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

function renderDeposit() {
    const urlParams = new URLSearchParams(window.location.search);

    const depositResult = urlParams.get('d');
    const depositSuccess = urlParams.get('s');

    if (depositResult) {
        if (depositSuccess) {
            const amount = urlParams.get('a');

            renderPrize(`
                <img src="/core/static/img/scrap.png">
                <h3 style="text-transform: none;">Deposit: ${amount} scrap!</h3>
                <span style="font-size: xx-large;">${amount}<img src="/core/static/img/scrap.png" style="width: 3ch"></span>
                <button class="super-button" style="font-family: 'Gilroy SemiBold'" onclick="closePrizeWindow('http://${location.hostname}')">
                    <span class="super-button-bg"></span>
                    <span class="super-button-text" style="font-size: x-large">Receive</span>
                </button>
            `);
        }
    }
}

renderDeposit();
renderFreeCase();
