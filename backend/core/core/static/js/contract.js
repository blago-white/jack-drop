import { renderItemPrize } from "./prize.js";
import { useAnim, printPrizeItem } from "./animations.js";

const startRange = document.getElementById('prst');
const stopRange = document.getElementById('prsp');
let newAmount;

let emptyPos = new Set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
let selected = new Map();

let grantedItems = new Map();
let grantedItemsFull = new Map();

let priceMapping = new Map();

function gcd () {
    const w = screen.width;
    const h = screen.height;

    return w/h;
}

function addAnimationCard(id) {
    const element = grantedItemsFull.get(id);
    console.log(grantedItemsFull, id);

    if (gcd() > 1/1) {
        document.getElementById("contract-field").innerHTML += `
            <article class="item-card selected-item-view-card" style="background: url(/core/static/img/card-bg-yellow.png);
            background-size:cover;cursor: pointer;" onclick="selectItem(${element.id})" id='v${element.id}'>
                <div class="dropped-content">
                    <div class="item-numeric-info">
                        <span class="item-price yellow"><span>${element.item.price}</span> <img src="/core/static/img/gear.png"></span>
                    </div>

                    <div style="display: grid;grid-template-rows: 1fr;grid-template-columns: 1fr;width: 100%;max-width: 100%;justify-items: center;align-items: center;">
                        <img src="/core/static/img/card-jd-logo.png" style="grid-row: 1;grid-column: 1;width: 100%;">
                        <img src="${element.item.image_path}" class="item-card-img" style="width: 100%;grid-row: 1;grid-column: 1;">
                    </div>

                    <span class="item-title">${element.item.title}</span>
                </div>
            </article>
        `;
    } else {
        document.getElementsByClassName('contract')[0].innerHTML = `
            <article class="item-card selected-item-view-card" style="background: url(/core/static/img/card-bg-yellow.png);
            background-size:cover;cursor: pointer;margin-left: ${25+(2.7*selected.size-1)}vw;"
            onclick="selectItem(${element.id})"
            id='mv${element.id}'>
                <div class="dropped-content">
                    <div class="item-numeric-info">
                        <span class="item-price yellow"><span>${element.item.price}</span> <img src="/core/static/img/gear.png"></span>
                    </div>

                    <div style="display: grid;grid-template-rows: 1fr;grid-template-columns: 1fr;width: 100%;max-width: 100%;justify-items: center;align-items: center;">
                        <img src="/core/static/img/card-jd-logo.png" style="grid-row: 1;grid-column: 1;width: 100%;">
                        <img src="${element.item.image_path}" class="item-card-img" style="width: 100%;grid-row: 1;grid-column: 1;">
                    </div>

                    <span class="item-title">${element.item.title}</span>
                </div>
            </article>
        ` + document.getElementsByClassName('contract')[0].innerHTML;

        document.getElementById(`mv${element.id}`).style.opacity = 1;
    }
}

function dropAnimationCard(id) {
    console.log(id);
    if (gcd() > 1/1) {
        document.getElementById(`v${id}`).remove()
    } else {
        document.getElementById(`mv${id}`).remove()
    }
}

function getCardColor(max, min, price) {
    const relativeRate = 1 - (price / max);

    if (relativeRate < 0.1) {
        return "yellow"
    } else if (relativeRate < 0.25) {
        return "red"
    } else if (relativeRate < 0.45) {
        return "pink"
    } else if (relativeRate < 0.7) {
        return "purple"
    } else {
        return "blue"
    }
}

function getExtremiums(resultList) {
    let max=0;
    let min=99999999999;

    resultList.forEach((element) => {
        console.log(element.item.price);

        max = Math.max(element.item.price, max)
        min = Math.min(element.item.price, min)
    })
    return [max, min];
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function getItems() {
    const formdata = new FormData();
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    const response = await sendRequest(
        `https://${location.hostname}/products/inventory/contract/`,
        requestOptions
    );

    const result = await response.json();

    const w = screen.width;
    const h = screen.height;
    let c = 0;

    let rareColor;

    if (result.length) {
        result.forEach((element) => {
            priceMapping.set(element.id, element.item.price)
        })

        const extremiums = getExtremiums(result);

        console.log(extremiums);

        result.forEach((element) => {
            rareColor = getCardColor(extremiums[0], extremiums[1], element.item.price);

            const html = `
                <article class="item-card" style="background: url(/core/static/img/card-bg-${rareColor}.png);background-size:cover;cursor: pointer;" onclick="selectItem(${element.id})" id=${element.id}>
                    <div class="dropped-content">
                        <div class="item-numeric-info">
                            <span class="item-price ${rareColor}"><span>${element.item.price}</span> <img src="/core/static/img/gear.png"></span>
                        </div>

                        <div style="display: grid;grid-template-rows: 1fr;grid-template-columns: 1fr;width: 100%;max-width: 100%;justify-items: center;align-items: center;">
                            <img src="/core/static/img/card-jd-logo.png" style="grid-row: 1;grid-column: 1;width: 100%;">
                            <img src="${element.item.image_path}" class="item-card-img" style="width: 100%;grid-row: 1;grid-column: 1;">
                        </div>

                        <span class="item-title">${element.item.title}</span>
                    </div>
                </article>
            `

            if (w > h) {
                document.getElementById('inventory-items').innerHTML += html;
            } else {
                document.getElementById('inventory-items-mob').innerHTML += html;
            }

            grantedItems.set(element.id, element.item);
            grantedItemsFull.set(element.id, element);
            c++;
        })
    } else {
        if (w > h) {
            document.getElementById('inventory-items').innerHTML = 'Нет предметов для контрактов';
            document.getElementById('inventory-items').style = "display: flex;justify-content: center;align-items: center;backdrop-filter: blur(5px);background: rgba(255, 255, 255, 0.15);text-align: center;padding: 2ch;";
        } else {
            document.getElementById('inventory-items-mob').innerHTML = 'Нет предметов для контрактов';
            document.getElementById('inventory-items-mob').style = "display: flex;justify-content: center;align-items: center;backdrop-filter: blur(5px);background: rgba(255, 255, 255, 0.15);text-align: center;padding: 2ch;";
        }
    }
}

function clearAll() {
    location.href = location.href;
}

function unselectItem(id) {
    if (!selected.has(id)) {
        return false;
    }

    document.getElementById(id).style.cursor = 'pointer';
    document.getElementById(id).style.filter = 'none';

    const current_amount = parseInt(document.getElementById('contract-amount').innerHTML);

    newAmount = Math.max(current_amount - priceMapping.get(id), 0);

    document.getElementById('contract-amount').innerHTML = newAmount.toFixed(0);

    document.getElementById('prst').innerHTML = `${(newAmount/2).toFixed(0)}`;
    document.getElementById('prsp').innerHTML = `${(newAmount*4).toFixed(0)}`;

    selected.delete(id);

    updateBtnBg();
}

async function animateContract() {
    if (gcd() > 1/1) {
        const bias = 10 / (selected.size-1);
        let c = 0;
        console.log(`bias: ${bias}`)

        document.getElementsByTagName('video')[4].defaultPlaybackRate = 2;
        document.getElementsByTagName('video')[4].playbackRate  = 2;
        await document.getElementsByTagName('video')[4].play();

        await declineAmount();

        for (let [key, value] of selected.entries()) {
            document.getElementById(`v${key}`).classList.add("used");
            document.getElementById(`v${key}`).style.marginLeft = `${39+(bias*c)}vw`;
            await sleep(6000 / selected.size)
            c ++;
        }
    } else {
        document.getElementsByTagName('video')[4].defaultPlaybackRate = 3;
        document.getElementsByTagName('video')[4].playbackRate  = 3;
        await document.getElementsByTagName('video')[4].play();

        for (let [key, value] of selected.entries()) {
            document.getElementById(`mv${key}`).style.opacity = `0`;
            await sleep(1000)
        }
    }
}

async function declineAmount() {
    let val = parseInt(document.getElementById('contract-amount').innerHTML);

    while (val>0) {
        document.getElementById('contract-amount').innerHTML = `${val}`;
        val -= 10;
        await sleep(10);
    }

    document.getElementById('contract-amount').innerHTML = `0`;
}

async function makeContract() {
    const myHeaders = new Headers();

    selected.forEach((element, element_id) => {
        document.getElementById(element_id).remove()
    })

    myHeaders.append("X-CSRFToken", document.cookie.split("=")[1].split(";")[0]);
    myHeaders.append("Content-Type", "application/json");

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify({"granted_inventory_items": Array.from(selected.keys())}),
      redirect: "follow"
    };

    const response = await sendRequest(
        `https://${location.hostname}/products/games/contract/`,
        requestOptions
    );

    await animateContract();

    if (!response.ok) {
        makeWarn("Error with operation, try again later");
        location.href = location.href;
    }

    const result = await response.json();

    await printPrizeItem(result.image_path, result.price, result.title);
}

function selectItem(id) {
    const lenBefore = selected.size;

    if (lenBefore+1 == 11 && (!selected.has(id))) {
        makeWarn("Maximum - 10 contract items");
        return;
    }

    console.log("S", selected, id);
//    let empty;
    if (selected.has(id)) {
        dropAnimationCard(id);
        emptyPos.add(selected.get(id).pos);
        return unselectItem(id);
    } else {
        selected.set(id, 1);
        addAnimationCard(id);
    }

    const current_amount = parseInt(document.getElementById('contract-amount').innerHTML);

    newAmount = (current_amount + priceMapping.get(id)).toFixed(0);

    console.log(newAmount, startRange);

    document.getElementById('prst').innerHTML = `${(newAmount/2).toFixed(0)}`;
    document.getElementById('prsp').innerHTML = `${(newAmount*4).toFixed(0)}`;

    document.getElementById('contract-amount').innerHTML = newAmount;

//    document.getElementById(`im${empty}`).style = `
//        background: url("${grantedItems.get(id).image_path}") center center / cover;
//        color: transparent""
//    `;

//    document.getElementById(`id${empty}`).innerHTML = `
//    <img src="${grantedItems.get(id).image_path}"
//        style="height: 15vh;aspect-ratio: 1 / 1;">
//    `;

//    selected.set(id, {pos: empty});

    document.getElementById(id).style.filter = 'grayscale(1)';

    updateBtnBg();
}

function updateBtnBg() {
    if (selected.size < 3) {
        document.getElementById('sign-contract-btn').classList.add('noactive')
    } else {
        document.getElementById('sign-contract-btn').classList.remove('noactive')
    }
}

async function changeBtn() {
    if (!(await getAuthenticated())) {
        let c = false;
        Array.from(document.getElementById('cr-contract').children).forEach((element) => {
            if (c) {
                element.innerHTML = document.getElementById('long-enter-text').innerHTML;
            } else {
                element.classList.remove("noactive");
            }

            c = true;
        })

        document.getElementById('cr-contract').onclick = () => {
            location.href = '/auth/';
        };
    }
}

getItems();
changeBtn();

window.selectItem = selectItem;
window.makeContract = makeContract;
window.unselectItem = unselectItem;
window.clearAll = clearAll;
