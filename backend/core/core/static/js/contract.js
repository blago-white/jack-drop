import { renderItemPrize } from "./prize.js";

const startRange = document.getElementById('prst');
const stopRange = document.getElementById('prsp');
let newAmount;

let emptyPos = new Set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
let selected = new Map();

let grantedItems = new Map();

let priceMapping = new Map();

function gcd () {
    const w = screen.width;
    const h = screen.height;

    return w/h;
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
        `http://${location.hostname}/products/inventory/contract/`,
        requestOptions
    );

    const result = await response.json();

    result.forEach((element) => {
        priceMapping.set(element.id, element.item.price)
    })

    const w = screen.width;
    const h = screen.height;

    if (result.length) {
        result.forEach((element) => {
            const html = `
                <article class="inventory-item dropped regular" style="cursor: pointer;" onclick="selectItem(${element.id})" id=${element.id}>
                    <div class="w-line"></div>
                    <div class="dropped-content">
                        <span>${element.item.title}</span>
                        <span class="item-price rose"><span>${element.item.price}</span> <img src="/core/static/img/gear.png"></span>
                        <img src="${element.item.image_path}">
                    </div>
                </article>
            `

            if (w > h) {
                document.getElementById('inventory-items').innerHTML += html;
            } else {
                document.getElementById('inventory-items-mob').innerHTML += html;
            }

            grantedItems.set(element.id, element.item);
        })
    } else {
        if (w > h) {
            document.getElementById('inventory-items').innerHTML = 'Items for upgrade not found';
            document.getElementById('inventory-items').style = "display: flex;background: #0E0E0E;padding: 3ch;text-align: center";
        } else {
            document.getElementById('inventory-items-mob').innerHTML = 'Items for upgrade not found';
            document.getElementById('inventory-items-mob').style = "display: flex;background: #0E0E0E;padding: 3ch;text-align: center";
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

    document.getElementById(id).style = 'cursor: pointer;';

    const current_amount = parseInt(document.getElementById('contract-amount').innerHTML);

    newAmount = current_amount - priceMapping.get(id);

    document.getElementById('contract-amount').innerHTML = newAmount;

    startRange.innerHTML = `${Math.ceil(newAmount/2)}`;
    stopRange.innerHTML = `${Math.ceil(newAmount*4)}`;

    let pos = null;

    document.getElementById(`im${selected.get(id).pos}`).style = '';
    document.getElementById(`id${selected.get(id).pos}`).innerHTML = '';

    selected.delete(id);
}

async function animateContract() {
    if (gcd() > 1/1) {

        document.getElementById('cells-row-1').style = 'transform: translateY(31vh);gap: 0px;';

        document.getElementById('cells-row-2').style = 'transform: translateY(16vh);gap: 0px;';

        document.getElementById('cells-row-3').style = 'gap: 0px;';

        document.getElementById('cells-row-4').style = 'transform: translateY(-21vh);gap: 0px;';

        document.getElementById('cells-row-5').style = 'transform: translateY(-31vh);gap: 0px;';


        document.getElementById('contract-glow').style.transform = 'scale(1.5)';

        setTimeout(() => {
            document.getElementById('contract-glow').style.transform = 'scale(1)';
        }, 1000)

        setTimeout(() => {
            document.getElementById('contract-glow').style.animation = 'infinite ease-in-out 0s glow-flickering, infinite ease-in-out 0s glow-rotate, infinite ease-in-out 1.5s glow-sizing';
        }, 2000)

        await declineAmount();
        await sleep(5000);
    }
}

async function declineAmount() {
    let val = parseInt(document.getElementById('contract-amount').innerHTML);

    while (val>0) {
        document.getElementById('contract-amount').innerHTML = `${val}`;
        val -= 10;
        await sleep(1);
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
        `http://${location.hostname}/products/games/contract/`,
        requestOptions
    );

    await animateContract();

    if (!response.ok) {
        alert("Error with operation, try again later");
        location.href = location.href;
    }

    const result = await response.json();

    renderItemPrize(
        result.title,
        result.price,
        result.image_path,
        "Amazing!"
    );
}

function selectItem(id) {
    const lenBefore = selected.size;

    if (lenBefore+1 == 11 && (!selected.has(id))) {
        alert("Maximum - 10 contract items");
        return;
    }

    let empty;

    if (selected.has(id)) {
        emptyPos.add(selected.get(id).pos);
        return unselectItem(id);
    } else {
        empty = Math.min(...Array.from(emptyPos.keys()));
        selected.set(id, {pos: empty});
        emptyPos.delete(empty);
    }

    const current_amount = parseInt(document.getElementById('contract-amount').innerHTML);

    newAmount = current_amount + priceMapping.get(id);

    startRange.innerHTML = `${Math.ceil(newAmount/2)}`;
    stopRange.innerHTML = `${Math.ceil(newAmount*4)}`;

    document.getElementById('contract-amount').innerHTML = newAmount;

    document.getElementById(`im${empty}`).style = `
        background: url("${grantedItems.get(id).image_path}") center center / cover;
        color: transparent;
    `;

    document.getElementById(`id${empty}`).innerHTML = `
    <img src="${grantedItems.get(id).image_path}"
        style="height: 15vh;aspect-ratio: 1 / 1;">
    `;

    selected.set(id, {pos: empty});

    document.getElementById(id).style.background = 'radial-gradient(50% 50% at 50% 50%, rgba(93, 93, 93, 0.8) 0%, rgba(35, 35, 35, 0.8) 100%)';
}

getItems();

window.selectItem = selectItem;
window.makeContract = makeContract;
window.unselectItem = unselectItem;
window.clearAll = clearAll;
