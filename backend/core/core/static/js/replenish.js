import { printPrizeItem } from "./animations.js";

const depoAmountField = document.getElementById('amount');
const agreementInput = document.getElementById('agreement');
let usedPromocode = document.getElementById('used-promocode');

if (usedPromocode) {
    usedPromocode = usedPromocode.innerHTML
    const hasPresetedPromocode = usedPromocode.length > 0;
}

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

if (document.getElementById("agreement") && document.getElementById("amount")) {
    document.getElementById("agreement").addEventListener('input', updateSubmitBtn);
    document.getElementById("amount").addEventListener('input', updateSubmitBtn);
}

function usePreset(preset) {
    document.getElementById('amount').value = preset;
    return false;
}

function getRandomArbitrary(min, max) {
    return Math.random() * (max - min) + min;
}

const urlParams = new URLSearchParams(window.location.search);

document.getElementById('amount').value = getRandomArbitrary(1000, 10000).toFixed(0);

window.usePreset = usePreset;
