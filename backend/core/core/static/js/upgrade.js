import { renderItemPrize } from "./prize.js";
import { useAnim, printPrizeItem } from "./animations.js";

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

function getCardColor(itemsCount, indexCurrent) {
    if (indexCurrent <= itemsCount*0.3) {
        return "blue"
    } else if (indexCurrent <= itemsCount * 0.55) {
        return "purple"
    } else if (indexCurrent <= itemsCount * 0.75) {
        return "pink"
    } else if (indexCurrent <= itemsCount * 0.9) {
        return "red"
    } else {
        return "yellow"
    }
}

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
        `https://${location.hostname}/products/inventory/upgrade/`,
        requestOptions
    );

    const result = await response.json();
    let rareColor;
    let c = 0;

    console.log(result)

    if (result) {
        result.forEach((element) => {
            rareColor = getCardColor(result.length, c);

            const elem = `
                <article class="item-card" style="background: url(/core/static/img/card-bg-${rareColor}.png);background-size:cover;cursor: pointer;" id="mg${element.id}"onclick="selectGrantedItem(this)">
                    <div class="dropped-content">
                        <div class="item-numeric-info">
                            <span class="item-price ${rareColor}"><span>${element.item.price}</span> <img src="/core/static/img/gear.png"></span>
                        </div>

                        <div style="display: grid;grid-template-rows: 1fr;grid-template-columns: 1fr;width: 100%;max-width: 100%;justify-items: center;align-items: center;">
                            <img src="/core/static/img/card-jd-logo.png" style="grid-row: 1;grid-column: 1;width: 100%;">
                            <img src="${element.item.image_path}" style="width: 100%;grid-row: 1;grid-column: 1;">
                        </div>

                        <span class="item-title">${element.item.title}</span>
                    </div>
                </article>
            `;

            const elemDesc = `
                <article class="item-card" style="background: url(/core/static/img/card-bg-${rareColor}.png);
                background-size:cover;
                cursor: pointer;" id="dg${element.id}"
                onclick="selectGrantedItem(this)">
                    <div class="dropped-content">
                        <div class="item-numeric-info">
                            <span class="item-price ${rareColor}"><span>${element.item.price}</span> <img src="/core/static/img/gear.png"></span>
                        </div>

                        <div style="display: grid;grid-template-rows: 1fr;grid-template-columns: 1fr;width: 100%;max-width: 100%;justify-items: center;align-items: center;">
                            <img src="/core/static/img/card-jd-logo.png" style="grid-row: 1;grid-column: 1;width: 100%;">
                            <img src="${element.item.image_path}" style="width: 100%;grid-row: 1;grid-column: 1;">
                        </div>

                        <span class="item-title">${element.item.title}</span>
                    </div>
                </article>
            `;

            available.innerHTML += elem;
            availableDesctop.innerHTML += elemDesc;

            grantedItems.set(element.id, element.item);

            c++;
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
        `https://${location.hostname}/products/items/all/`,
        requestOptions
    );

    const result = await response.json();
    let rareColor;
    let c = 0;

    let receiveHTML = '';
    let receiveDesctopHTML = '';

    if (result) {
        result.forEach((element) => {
            rareColor = getCardColor(result.length, c);

            const elem = `
                <article class="item-card" style="background: url(/core/static/img/card-bg-${rareColor}.png);background-size:cover;cursor: pointer;" id="mr${element.id}" onclick="selectReceiveItem(this)">
                    <div class="dropped-content">
                        <div class="item-numeric-info">
                            <span class="item-price ${rareColor}"><span>${element.price}</span> <img
                            src="/core/static/img/gear.png"></span>
                        </div>

                        <div style="display: grid;grid-template-rows: 1fr;grid-template-columns: 1fr;width: 100%;max-width: 100%;justify-items: center;align-items: center;">
                            <img src="/core/static/img/card-jd-logo.png" style="grid-row: 1;grid-column: 1;width: 100%;">
                            <img src="${element.image_path}" style="width: 100%;grid-row: 1;grid-column: 1;">
                        </div>

                        <span class="item-title">${element.title}</span>
                    </div>
                </article>
            `;

            const elemDesc = `
                <article class="item-card" style="background: url(/core/static/img/card-bg-${rareColor}.png);background-size:cover;cursor: pointer;"
                id="dr${element.id}"
                onclick="selectReceiveItem(this)">
                    <div class="dropped-content">
                        <div class="item-numeric-info">
                            <span class="item-price ${rareColor}"><span>${element.price}</span> <img
                            src="/core/static/img/gear.png"></span>
                        </div>

                        <div style="display: grid;grid-template-rows: 1fr;grid-template-columns: 1fr;width: 100%;max-width: 100%;justify-items: center;align-items: center;">
                            <img src="/core/static/img/card-jd-logo.png" style="grid-row: 1;grid-column: 1;width: 100%;">
                            <img src="${element.image_path}" style="width: 100%;grid-row: 1;grid-column: 1;">
                        </div>

                        <span class="item-title">${element.title}</span>
                    </div>
                </article>
            `;

            receiveHTML += elem;
            receiveDesctopHTML += elemDesc;

            receiveItems.set(element.id, element);

            c++;
        })

        receive.innerHTML += receiveHTML;
        receiveDesctop.innerHTML += receiveDesctopHTML;
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
        document.getElementById(selectedGranted).style.filter = "none";
    }

    console.log(elem.id, elem);

    const raw_id = parseInt(elem.id.slice(2));

    document.getElementById('u-m-1').src = grantedItems.get(raw_id).image_path;
    document.getElementById('u-d-1').src = grantedItems.get(raw_id).image_path;

    selectedGranted = elem.id;
    elem.style.filter = 'grayscale(1)';

    updateReceiveList(grantedItems.get(raw_id).price, undefined);
    updatePercent();
}

function selectReceiveItem(elem) {
    if (selectedReceive) {
        document.getElementById(selectedReceive).style.filter = "none";
    }

    const raw_id = parseInt(elem.id.slice(2));

    document.getElementById('u-m-2').src = receiveItems.get(raw_id).image_path;
    document.getElementById('u-d-2').src = receiveItems.get(raw_id).image_path;

    selectedReceive = elem.id;
    elem.style.filter = 'grayscale(1)';

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
        "granted_item_id": (selectedGranted ? parseInt(selectedGranted.slice(2)) : null),
        "granted_funds": selectedGrantedBalance,
        "receive_item_id": receiveItems.get(parseInt(selectedReceive.slice(2))).id,
      }),
      redirect: "follow"
    };

    const response = await sendRequest(
        `https://${location.hostname}/products/games/upgrade/`,
        requestOptions
    );

    const responseSuccess = response.ok;

    const result = await response.json();

    if (!responseSuccess) {
        location.href = location.href;
    }

    let item = null;

    await animateResult(result);
}

async function animateResult(result) {
    let item;

    if (result.success) {
        item = receiveItems.get(parseInt(selectedReceive.slice(2)));

        await useAnim(false, "upgrade2");
        await printPrizeItem(item.image_path, 0, item.title);
//        renderItemPrize(`You receice ${item.title}!`, item.price, item.image_path, "Amazing!");
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

        await useAnim(false, "upgrade1");
        await useAnim(true, "unlucky");

	    setTimeout(() => {location.href = location.href}, 3000)
	    //renderItemPrize(`You lose ${item.title}!`, item.price, item.image_path, "Ok!");
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

    if (newPercent > 100) {newPercent = 100} else if (newPercent < 0) {newPercent = 0};

    chanceCicle.src = `/core/static/img/upgrade-chance-${25*(Math.ceil(newPercent / 25))}.png`;

    if (((selectedGrantedBalance>0) | (selectedGranted != null)) && (selectedReceive != null)) {
        document.getElementById('upgrade-percent').innerHTML = `${newPercent}%`;

        if (newPercent == 100) {
            return false;
        }

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

async function changeBtn() {
    if (!(await getAuthenticated())) {
        let c = false;
        Array.from(document.getElementById('make-upgrade').children).forEach((element) => {
            if (c) {
                element.innerHTML = document.getElementById('long-enter-text').innerHTML;
            } else {
                element.style = '';
            }

            c = true;
        })

        document.getElementById('make-upgrade').onclick = () => {
            location.href = '/auth/';
        };
    }
}

function updateReceiveList(from, to) {
    from = from ? from : 0;
    to = to ? to : 10**9;

    if (from >= to) {
        location.href = location.href;
    }

    Array.from(receiveItems.keys()).forEach((elementId) => {
        if (receiveItems.get(elementId).price < from || receiveItems.get(elementId).price > to) {
            document.getElementById(`dr${elementId}`).style.display = 'none';
            document.getElementById(`mr${elementId}`).style.display = 'none';
        } else {
            document.getElementById(`dr${elementId}`).style.display = 'flex';
            document.getElementById(`mr${elementId}`).style.display = 'flex';
        }
    });
}


grantedBalance.addEventListener('input', inputBalanceFunds)

getInevntoryItems();
getReceiveItems();
changeBtn();


window.inputBalanceFunds = inputBalanceFunds;
window.clearInputBalance = clearInputBalance;
window.updatePercent = updatePercent;
window.makeUpgrade = makeUpgrade;
window.selectReceiveItem = selectReceiveItem;
window.selectGrantedItem = selectGrantedItem;
window.getReceiveItems = getReceiveItems;
window.getInevntoryItems = getInevntoryItems;
window.updateReceiveList = updateReceiveList;
