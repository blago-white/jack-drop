const inventoryItemsTable = document.getElementById('inventory-items');

async function sellItem(id) {
    const headers = new Headers();

    headers.append("X-CSRFToken", document.cookie.split("=")[1].split(";")[0]);
    headers.append("Content-Type", "application/json");

    const requestOptions = {
      method: "POST",
      body: JSON.stringify({
        "item_id": id
      }),
      headers: headers
    };

    const response = await fetch(
        `http://localhost/products/inventory/sell/`,
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

    headers.append("X-CSRFToken", document.cookie.split("=")[1].split(";")[0]);
    headers.append("Content-Type", "application/json");

    const requestOptions = {
      method: "POST",
      body: JSON.stringify({
        "item_id": id
      }),
      headers: headers
    };

    const response = await fetch(
        `http://localhost/products/inventory/withdraw/`,
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

async function getInventoryItems() {
    const requestOptions = {
      method: "GET",
    };

    const response = await fetch(
        `http://localhost/products/inventory/all/`,
        requestOptions
    );

    const result = await response.json();
    let c = 0;

    result.forEach((element) => {
        c += 1;

        inventoryItemsTable.innerHTML += `
            <article class="dropped mono" id="${element.id}">
                <div class="w-line"></div>
                <div class="dropped-content">
                    <span>${element.item.title}</span>
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


getInventoryItems();
