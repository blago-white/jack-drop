import { getCount } from "./inventoryCount.js";
import { renderItemPrize } from "./prize.js";

const inventoryItemsTable = document.getElementById('inventory-items');

let switchActive = false;

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
};

function getExtremiums(resultList) {
    let max=0;
    let min=99999999999;

    resultList.forEach((element) => {
        console.log(element.item.price, max, min);
        max = Math.max(element.item.price, max)
        min = Math.min(element.item.price, min)
    })

    console.log(max, min);

    return [max, min];
}

function getCardColor(max, min, price) {
    const relativeRate = 1 - (price / max);

    console.log(relativeRate, price, max);

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

async function sellItem(id) {
    const headers = new Headers();

    headers.append("X-CSRFToken", getCookie("csrftoken"));
    headers.append("Content-Type", "application/json");

    const requestOptions = {
      method: "POST",
      body: JSON.stringify({
        "item_id": id
      }),
      headers: headers
    };

    const response = await sendRequest(
        `https://${location.hostname}/products/inventory/sell/`,
        requestOptions
    );

    const result = await response.json();

    if (result.ok) {
        document.getElementById(id).classList.remove('dropped');
        document.getElementById(id).classList.remove('mono');
        document.getElementById(id).classList.add('empty-inventory-item');
        document.getElementById(id).innerHTML = '';
    } else {
        alert("Cannot sell this item")
    }
}

async function withdrawItem(id) {
    const headers = new Headers();

    headers.append("X-CSRFToken", getCookie("csrftoken"));
    headers.append("Content-Type", "application/json");

    const requestOptions = {
      method: "POST",
      body: JSON.stringify({}),
      headers: headers
    };

    const response = await sendRequest(
        `https://${location.hostname}/products/inventory/withdraw/${id}/`,
        requestOptions
    );

    const result = await response.json();

    if (result.ok) {
        document.getElementById(id).classList.remove('dropped');
        document.getElementById(id).classList.remove('mono');
        document.getElementById(id).classList.add('empty-inventory-item');
        document.getElementById(id).innerHTML = '';
    } else {
        alert("Cannot withdraw this item")
    }
}

function renderItems(result) {
    let c = 0;
    let cardColor;

    const extremiums = getExtremiums(result);

    result.forEach((element) => {
        c += 1;
        cardColor = getCardColor(extremiums[0], extremiums[1], element.item.price);

        console.log(cardColor, extremiums);

        inventoryItemsTable.innerHTML += `
            <article class="item-card" style="background: url(/core/static/img/card-bg-${cardColor}.png);background-size:cover;cursor: pointer;" id="${element.id}">
                <div class="dropped-content">
                    <div class="item-numeric-info">
                        <span class="item-price ${cardColor}"><span>${element.item.price}</span> <img src="/core/static/img/gear.png"></span>
                    </div>

                    <div style="display: grid;grid-template-rows: 1fr;grid-template-columns: 1fr;width: 100%;height: 10%;max-width: 100%;justify-items: center;align-items: center;align-content: center;">
                        <img src="/core/static/img/card-jd-logo.png" style="grid-row: 1;grid-column: 1;width: 100%;">
                        <img src="${element.item.image_path}" class="item-card-img" style="width: 70%;grid-row: 1;grid-column: 1;">
                    </div>

                    <span class="item-title">${element.item.title}</span>
                </div>
                <div class="items-controls">
                    <button onclick="sellItem(${element.id})">
                        Продать
                        <img src="/core/static/img/inventory-item-sell-icon.png"
                             style="width: 3ch;aspect-ratio: 1 / 1;position: unset;margin: 0px;">
                    </button>
                    <button onclick="withdrawItem(${element.id})">
                        Вывести
                        <img src="/core/static/img/inventory-item-export-icon.png"
                             style="width: 3ch;aspect-ratio: 1 / 1;position: unset;margin: 0px;">
                    </button>
                </div>
            </article>
        `;
    });

    if (6 - (c % 6)) {
        for (let i = 0; i < (6 - (c % 6)); i++)
        inventoryItemsTable.innerHTML += `
            <div class="empty-inventory-item"></div>
        `;
    };
}

async function getInventoryItems() {
    const requestOptions = {
      method: "GET",
    };

    const response = await sendRequest(
        `https://${location.hostname}/products/inventory/all/`,
        requestOptions
    );

    const result = await response.json();

    renderItems(result);
}

async function getBuyItems() {
    const requestOptions = {
      method: "GET",
    };

    const response = await sendRequest(
        `https://${location.hostname}/products/inventory/unlock/`,
        requestOptions
    );

    const result = await response.json();

    renderItems(result);
}

async function buySwitch() {
    if (!switchActive) {
        if (countItems) {
            document.getElementById('total-inv-items-count').innerHTML = countItems.can_sell;
        }

        document.getElementById('switch-input').style.background = 'linear-gradient(180deg, #FF62CA 0%, #FF007A 100%)';
        document.getElementById('switch-inside-fig').style.marginLeft = '60%';

        document.getElementById('see-all-btn').href = document.getElementById(
            'see-all-btn'
        ) + '?forsell=1';

        switchActive = true;
    } else {
        if (countItems) {
            document.getElementById('total-inv-items-count').innerHTML = countItems.total;
        }

        document.getElementById('switch-input').style= '';
        document.getElementById('switch-inside-fig').style = '';
        document.getElementById('see-all-btn').href = document.getElementById('see-all-btn').href.slice(0, -10);
        switchActive = false;
    }
}

async function sellAll() {
    const data = await sendRequestJson("/products/inventory/sell/all/", {method: "POST", headers: new Headers()})
    if (data.ok && data.received) {
        renderItemPrize(`Receive ${data.received} scrap!`, data.received, "/core/static/img/scrap.png", "Receive!")
    }
}

window.sellItem = sellItem;
window.withdrawItem = withdrawItem;
window.renderItems = renderItems;
window.getInventoryItems = getInventoryItems;
window.getBuyItems = getBuyItems;
window.buySwitch = buySwitch;

if (document.getElementById('sell-all')) {
    document.getElementById('sell-all').addEventListener("click", sellAll);
}

try {
    document.getElementById('switch-input').addEventListener('click', buySwitch);
} catch(error) {}

let countItems;

if (location.pathname.slice(0, 12) == '/inventory/') {
    const searchParams = new URL(location.href).searchParams;

    if (searchParams.get("forsell")) {
        getBuyItems();
    } else {
        getInventoryItems();
    }
} else {
    countItems = await getCount();

    if (!countItems.can_sell) {
        document.getElementById("sell-all").style.display = "none";
    }
}
