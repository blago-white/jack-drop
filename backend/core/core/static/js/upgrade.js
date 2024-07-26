import { renderItemPrize } from "./prize.js";

const available = document.getElementById('items-feed');
const availableDesctop = document.getElementById('items-feed-desctop');

const receive = document.getElementById('receive-items-feed');
const receiveDesctop = document.getElementById('receive-items-feed-desctop');

const chanceCicle = document.getElementById('update-chance-circle');

const grantedBalance = document.getElementById('granted-balance');

let receiveItems = new Map();
let grantedItems = new Map();

let selectedGranted = null;
let selectedReceive = null;
let selectedGrantedBalance = null;


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function gcd () {
    const w = screen.width;
    const h = screen.height;

    return w/h;
}

function randomIntFromInterval(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

async function getInevntoryItems() {
    const formdata = new FormData();
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    const response = await sendRequest(
        `http://localhost/products/inventory/upgrade/`,
        requestOptions
    );

    const result = await response.json();

    if (result) {
        result.forEach((element) => {
            const elem = `
                <article class="dropped mono" style="cursor: pointer;" id="mg${element.id}" onclick="selectGrantedItem(this)">
                    <div class="w-line"></div>
                    <div class="dropped-content">
                        <span>${element.item.title}</span>
                        <span class="item-price rose"><span>${element.item.price}</span> <img src="/core/static/img/gear.png"></span>
                        <img src="${element.item.image_path}">
                    </div>
                </article>
            `;

            const elemDesc = `
                <article class="dropped mono" style="cursor: pointer;" id="dg${element.id}" onclick="selectGrantedItem(this)">
                    <div class="w-line"></div>
                    <div class="dropped-content">
                        <span>${element.item.title}</span>
                        <span class="item-price rose"><span>${element.item.price}</span> <img src="/core/static/img/gear.png"></span>
                        <img src="${element.item.image_path}">
                    </div>
                </article>
            `;

            available.innerHTML += elem;
            availableDesctop.innerHTML += elemDesc;

            grantedItems.set(element.id, element.item);
        })
    } else {
        available.style = "display:flex;align-content: center;justify-content: center;"
        available.innerHTML = "Нет предметов для апгрейда";

        availableDesctop.style = "display:flex;align-content: center;justify-content: center;"
        availableDesctop.innerHTML = "Нет предметов для апгрейда";
    }
}

async function getReceiveItems(minItemPrice) {
    const formdata = new FormData();
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    const response = await sendRequest(
        `http://localhost/products/items/all/`,
        requestOptions
    );

    const result = await    response.json();

    if (result) {
        result.forEach((element) => {
            const elem = `
                <article class="dropped mono" style="cursor: pointer;" id="mr${element.id}" onclick="selectReceiveItem(this)">
                    <div class="w-line"></div>
                    <div class="dropped-content">
                        <span>${element.title}</span>
                        <span class="item-price rose"><span>${element.price}</span> <img src="/core/static/img/gear.png"></span>
                        <img src="${element.image_path}">
                    </div>
                </article>
            `;

            const elemDesc = `
                <article class="dropped mono" style="cursor: pointer;"
                id="dr${element.id}"
                onclick="selectReceiveItem(this)">
                    <div class="w-line"></div>
                    <div class="dropped-content">
                        <span>${element.title}</span>
                        <span class="item-price rose"><span>${element.price}</span> <img src="/core/static/img/gear.png"></span>
                        <img src="${element.image_path}">
                    </div>
                </article>
            `;

            receive.innerHTML += elem;
            receiveDesctop.innerHTML += elemDesc;

            receiveItems.set(element.id, element);
        })
    } else {
        receive.style = "display:flex;align-content: center;justify-content: center;"
        receive.innerHTML = "Нет предметов для апгрейда";

        receiveDesctop.style = "display:flex;align-content: center;justify-content: center;"
        receiveDesctop.innerHTML = "Нет предметов для апгрейда";
    }
}

function selectGrantedItem(elem) {
    clearInputBalance();

    if (selectedGranted) {
        document.getElementById(selectedGranted).style.border = "none";
    }

    const raw_id = parseInt(elem.id.slice(2));

    document.getElementById('u-m-1').src = grantedItems.get(raw_id).image_path;
    document.getElementById('u-d-1').src = grantedItems.get(raw_id).image_path;

    selectedGranted = elem.id;
    elem.style.border = '.5ch solid darkseagreen';

    updatePercent();
}

function selectReceiveItem(elem) {
    if (selectedReceive) {
        document.getElementById(selectedReceive).style.border = "none";
    }

    const raw_id = parseInt(elem.id.slice(2));

    document.getElementById('u-m-2').src = receiveItems.get(raw_id).image_path;
    document.getElementById('u-d-2').src = receiveItems.get(raw_id).image_path;

    selectedReceive= elem.id;
    elem.style.border = '.5ch solid darkseagreen';

    updatePercent();
}

async function makeUpgrade() {
    console.log("EEEE");

    if (selectedGrantedBalance && selectedGranted) {
        return false;
    }

    const myHeaders = new Headers();

    myHeaders.append("X-CSRFToken", document.cookie.split("=")[1].split(";")[0]);
    myHeaders.append("Content-Type", "application/json");

    if (!selectedGrantedBalance && document.getElementById(selectedGranted)) {
        document.getElementById(selectedGranted).remove();
    }

    console.log("WOW", selectedGranted, grantedItems, parseInt(selectedGranted.slice(2)), grantedItems.get(parseInt(selectedGranted.slice(2))));

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify({
        "receive_item_id": receiveItems.get(parseInt(selectedReceive.slice(2))).id,
        "granted_item_id": selectedGranted ? grantedItems.get(parseInt(selectedGranted.slice(2))).id : null,
        "granted_funds": selectedGrantedBalance
      }),
      redirect: "follow"
    };

    const response = await sendRequest(
        `http://localhost/products/games/upgrade/`,
        requestOptions
    );

    const responseSuccess = response.ok;

    const result = await response.json();

    if (!responseSuccess) {
        alert(result);
        location.href = location.href;
    }

    let item = null;

    await animateResult(result);
}

async function animateResult(result) {
    if (gcd() > 1/1) {
        document.getElementById('receive-item-glow').style.transform = "scale(1)";
        document.getElementById('receive-item-glow').style.opacity = "1";
        document.getElementById('receive-item-glow').style.animation = "1s ease-in-out 2s infinite glow-flickering, ease-in-out 2s infinite glow-rotate";
        await sleep(3000);

        document.getElementById('receive-item-glow').style.opacity = "0";
    }

    let item;

    if (result.success) {
        item = receiveItems.get(parseInt(selectedReceive.slice(2)));
        renderItemPrize(`You receice ${item.title}!`, item.price, item.image_path, "Amazing!");
    } else {
        if (selectedGrantedBalance) {
            item = {
                title: "scrap",
                price: selectedGrantedBalance,
                image_path: "/core/static/img/scrap.png"
            };
        } else {
            item = grantedItems.get(parseInt(selectedGranted.slice(2)));
        }
        renderItemPrize(`You lose ${item.title}!`, item.price, item.image_path, "Ok!");
    }
}

function updatePercent() {
    console.log(selectedGranted, selectedReceive, selectedGrantedBalance);

    let newPercent = 0;

    if (selectedGranted && selectedReceive) {
        const rawSelectedGranted = grantedItems.get(parseInt(selectedGranted.slice(2))).price;
        const rawSelectedReceive = receiveItems.get(parseInt(selectedReceive.slice(2))).price;

        newPercent = Math.round(Math.min(
            (rawSelectedGranted / rawSelectedReceive)*100, 100
        ))
    } else if (selectedReceive && selectedGrantedBalance) {
        const rawSelectedReceive = receiveItems.get(parseInt(selectedReceive.slice(2))).price;

        newPercent = Math.round(Math.min(
            (selectedGrantedBalance / rawSelectedReceive)*100, 100
        ))
    }

    chanceCicle.src = `/core/static/img/upgrade-chance-${25*(Math.ceil(newPercent / 25))}.png`;

    if (((selectedGrantedBalance>0) | (selectedGranted != null)) && (selectedReceive != null)) {
        document.getElementById('upgrade-percent').innerHTML = `${newPercent}%`;

        document.getElementById('make-upgrade-bg').style = '';
        document.getElementById('make-upgrade').addEventListener(
            'click',
            async function() {await makeUpgrade();}
        )

        console.log(document.getElementById('make-upgrade-bg').parentElement);
    }
}


function clearInputBalance() {
    selectedGrantedBalance = null;
    grantedBalance.value = null;
}

function inputBalanceFunds() {
    if (selectedGranted) {
        document.getElementById(selectedGranted).style = '';
        selectedGranted = null;
    }

    selectedGrantedBalance = parseInt(grantedBalance.value);

    updatePercent();
}

grantedBalance.addEventListener('input', inputBalanceFunds)

getInevntoryItems();
getReceiveItems();

window.inputBalanceFunds = inputBalanceFunds;
window.clearInputBalance = clearInputBalance;
window.updatePercent = updatePercent;
window.makeUpgrade = makeUpgrade;
window.selectReceiveItem = selectReceiveItem;
window.selectGrantedItem = selectGrantedItem;
window.getReceiveItems = getReceiveItems;
window.getInevntoryItems = getInevntoryItems;
