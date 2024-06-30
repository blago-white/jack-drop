import { renderItemPrize } from "./prize.js";

let selected = new Map();

let grantedItems = new Map();

let priceMapping = new Map();

function gcd (a, b) {
    return (b == 0) ? a : gcd (b, a%b);
}

async function getItems() {
    const formdata = new FormData();
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    const response = await fetch(
        `http://localhost/products/inventory/contract/`,
        requestOptions
    );

    const result = await response.json();

    result.forEach((element) => {
        priceMapping.set(element.id, element.item.price)
    })

    const w = screen.width;
    const h = screen.height;
    const ratio = gcd (w, h);

    if (result.length) {
        result.forEach((element) => {
            const html = `
                <article class="inventory-item dropped regular" style="cursor: pointer;" onclick="selectItem(${element.id})" id=${element.id}>
                    <div class="w-line"></div>
                    <div class="dropped-content">
                        <span>${element.item.title}</span>
                        <img src="${element.item.image_path}">
                    </div>
                </article>
            `

            if (ratio > 1/1) {
                document.getElementById('inventory-items').innerHTML += html;
            } else {
                document.getElementById('inventory-items-mob').innerHTML += html;
            }

            grantedItems.set(element.id, element.item);
        })
    } else {
        if (ratio > 1/1) {
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

    document.getElementById('contract-amount').innerHTML = current_amount - priceMapping.get(id);

    let pos = null;

    console.log(selected.get(id), selected, id);

    document.getElementById(`im${selected.get(id).pos}`).style = '';

    selected.delete(id);
}

async function makeContract() {
    const myHeaders = new Headers();

    selected.forEach((element, element_id) => {
        document.getElementById(element_id).remove()
    })

    document.getElementById('contract-amount').innerHTML = "0";

    myHeaders.append("X-CSRFToken", document.cookie.split("=")[1].split(";")[0]);
    myHeaders.append("Content-Type", "application/json");

    console.log(selected.keys());

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify({"granted_inventory_items": Array.from(selected.keys())}),
      redirect: "follow"
    };

    const response = await fetch(
        `http://localhost/products/games/contract/`,
        requestOptions
    );

    if (!response.ok) {
        alert("Error with operation, try again later");
        location.href = location.href;
    }

    const result = await response.json();

    console.log(result);

    renderItemPrize(
        result.title,
        result.price,
        result.image_path,
        "Amazing!"
    );
}

function selectItem(id) {
    const lenBefore = selected.size;

    if (lenBefore+1 == 10 && (!selected.has(id))) {
        alert("Maximum - 10 contract items");
        return;
    }

    if (selected.has(id)) {
        return unselectItem(id);
    } else {
        selected.set(id, {"pos": lenBefore+1});
    }

    const current_amount = parseInt(document.getElementById('contract-amount').innerHTML);

    document.getElementById('contract-amount').innerHTML = current_amount + priceMapping.get(id);

    document.getElementById(`im${selected.size}`).style = `
        background: url("${grantedItems.get(id).image_path}") center center / cover;
        color: transparent;
    `;

    selected.set(id, {pos: selected.size});

    document.getElementById(id).style.background = 'gray';
}

getItems();

window.selectItem = selectItem;
window.makeContract = makeContract;
window.unselectItem = unselectItem;
window.clearAll = clearAll;
