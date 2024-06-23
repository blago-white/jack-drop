let selected = new Set();

let priceMapping = new Map();

async function getItems() {
    const formdata = new FormData();
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    const response = await fetch(
        `http://localhost/products/inventory/all/`,
        requestOptions
    );

    const result = await response.json();

    result.forEach((element) => {
        priceMapping.set(element.id, element.item.price)
    })

    result.forEach((element) => {
        document.getElementById('inventory-items').innerHTML += `
            <article class="inventory-item dropped regular" style="cursor: pointer;" onclick="selectItem(${element.id})" id=${element.id}>
                <div class="w-line"></div>
                <div class="dropped-content">
                    <span>${element.item.title}</span>
                    <img src="${element.item.image_path}">
                </div>
            </article>
        `
    })
}

function clearAll() {
    selected.forEach((element) => {
        unselectItem(element);
    });

    document.getElementById('contract-amount').innerHTML = "0";
}

function unselectItem(id) {
    const lenBefore = selected.size;

    selected.delete(id);

    if (lenBefore == selected.size) {
        return false;
    }

    document.getElementById(id).style = 'cursor: pointer;';

    const current_amount = parseInt(document.getElementById('contract-amount').innerHTML);

    document.getElementById('contract-amount').innerHTML = current_amount - priceMapping.get(id);
}

async function makeContract() {
    const myHeaders = new Headers();

    selected.forEach((element) => {
        document.getElementById(element).remove()
    })

    document.getElementById('contract-amount').innerHTML = "0";

    myHeaders.append("X-CSRFToken", document.cookie.split("=")[1].split(";")[0]);
    myHeaders.append("Content-Type", "application/json");

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify({"granted_inventory_items": Array.from(selected)}),
      redirect: "follow"
    };

    const response = await fetch(
        `http://localhost/products/games/contract/`,
        requestOptions
    );

    const result = await response.json();

    console.log(result);
}

function selectItem(id) {
    const lenBefore = selected.size;

    selected.add(id);

    console.log(lenBefore, selected.size);

    if (lenBefore === selected.size) {
        return unselectItem(id);
    }

    document.getElementById(id).style.background = 'gray';

    const current_amount = parseInt(document.getElementById('contract-amount').innerHTML);

    document.getElementById('contract-amount').innerHTML = current_amount + priceMapping.get(id);
}

getItems();
