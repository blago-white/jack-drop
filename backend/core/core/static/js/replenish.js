import { renderItemPrize } from "./prize.js";

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

    const response = await sendRequest('/auth/balances/api/v1/public/add_deposit/', {
        method: "POST",
        body: JSON.stringify({"amount": amount}),
        headers: headers
    });

    if (!response.ok) {
        document.getElementById('replenish-form').style.outline = '5px solid firebrick'
    } else {
        renderItemPrize("Scrap", amount, "/core/static/img/scrap.png", "Receive")
    }

    return false;
}

window.addDeposit = addDeposit;
window.setPaymentMethod = setPaymentMethod;

document.getElementById("agreement").addEventListener('input', updateSubmitBtn);
document.getElementById("amount").addEventListener('input', updateSubmitBtn);
