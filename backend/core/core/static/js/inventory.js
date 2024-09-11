import { getCount } from "./inventoryCount.js";

const inventoryItemsTable = document.getElementById('inventory-items');

let switchActive = false;

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
};

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

    result.forEach((element) => {
        c += 1;

        inventoryItemsTable.innerHTML += `
            <article class="dropped mono" id="${element.id}">
                <div class="w-line"></div>
                <div class="dropped-content">
                    <span>${element.item.title}</span>
                    <span class="item-price rose"><span>${element.item.price}</span> <img src="/core/static/img/gear.png"></span>
                    <img src="${element.item.image_path}" style="left: 0%;">
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
    const countItemsResult = await getCount();

    if (!switchActive) {
        if (countItemsResult) {
            document.getElementById('total-inv-items-count').innerHTML = countItemsResult.can_sell;
        }

        document.getElementById('switch-input').style.background = 'linear-gradient(180deg, #FF62CA 0%, #FF007A 100%)';
        document.getElementById('switch-inside-fig').style.marginLeft = '60%';

        document.getElementById('see-all-btn').href = document.getElementById(
            'see-all-btn'
        ) + '?forsell=1';

        switchActive = true;
    } else {
        if (countItemsResult) {
            document.getElementById('total-inv-items-count').innerHTML = countItemsResult.total;
        }

        document.getElementById('switch-input').style= '';
        document.getElementById('switch-inside-fig').style = '';
        document.getElementById('see-all-btn').href = document.getElementById('see-all-btn').href.slice(0, -10);
        switchActive = false;
    }
}

async function sellAll() {
    const response = await sendRequestJson("/products/inventory/sell/all/", {method: "POST", headers: new Headers()})
    if (response.ok) {
        const data = await response.json();

        if (data.ok) {
            renderItemPrize(`Receive ${data.receive} scrap!`, data.receive, "/core/static/img/scrap.png", "Receive!")
        }
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


if (location.pathname.slice(0, 12) == '/inventory/') {
    const searchParams = new URL(location.href).searchParams;

    if (searchParams.get("forsell")) {
        getBuyItems();
    } else {
        getInventoryItems();
    }
}
