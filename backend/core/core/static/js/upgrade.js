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

    const result = await response.json();

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
    if (selectedGrantedBalance && selectedGranted) {
        return false;
    }

    const myHeaders = new Headers();

    myHeaders.append("X-CSRFToken", document.cookie.split("=")[1].split(";")[0]);
    myHeaders.append("Content-Type", "application/json");

    if (!selectedGrantedBalance && document.getElementById(selectedGranted)) {
        document.getElementById(selectedGranted).remove();
    }

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

    const response = sendRequest(
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
    const start = Date.now();

    document.getElementById('u-m-1').style.filter = 'brightness(250)';
    document.getElementById('u-d-1').style.filter = 'brightness(250)';
    document.getElementById('u-m-2').style.filter = 'brightness(250)';
    document.getElementById('u-d-2').style.filter = 'brightness(250)';

    let m = 40;
    let c = 0;
    let wChanged = false;
    let randomYfactor1 = 0;
    let randomYfactor2 = 0;
    let item;

    while ((Date.now() - start) < 3000) {
        await sleep(30);

        let factor = randomIntFromInterval(0, 40);

        if (!wChanged) {
            randomYfactor1 = randomIntFromInterval(-40, 40);
            randomYfactor2 = randomIntFromInterval(-40, 40);
        } else {
            randomYfactor1 = 0;
            randomYfactor2 = 0;
        }

        if (c > m) {
            document.getElementById('u-m-1').style.transform = `translateY(${-factor}px translateX(${randomYfactor1}px))`;
            document.getElementById('u-d-1').style.transform = `translateY(${-factor}px translateX(${randomYfactor1}px))`;
            document.getElementById('u-m-2').style.transform = `translateY(${-factor}px translateX(${randomYfactor2}px))`;
            document.getElementById('u-d-2').style.transform = `translateY(${-factor}px translateX(${randomYfactor2}px))`;

            c -= factor;
        } else {
            document.getElementById('u-m-1').style.transform = `translateY(${factor}px) translateX(${randomYfactor2}px)`;
            document.getElementById('u-d-1').style.transform = `translateY(${factor}px) translateX(${randomYfactor2}px)`;
            document.getElementById('u-m-2').style.transform = `translateY(${factor}px) translateX(${randomYfactor1}px)`;
            document.getElementById('u-d-2').style.transform = `translateY(${factor}px) translateX(${randomYfactor1}px)`;

            c += factor;
        }

        wChanged = !wChanged;
    };

    document.getElementById('u-m-1').style.opacity = `0`;
    document.getElementById('u-d-1').style.opacity = `0`;
    document.getElementById('u-m-2').style.opacity = `0`;
    document.getElementById('u-d-2').style.opacity = `0`;

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

    console.log(newPercent, (((selectedGrantedBalance>0) | (selectedGranted != null)) && (selectedReceive != null)), "---")

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
