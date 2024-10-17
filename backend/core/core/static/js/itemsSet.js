import { renderItemPrize } from "./prize.js";


let setId;
let set;

async function buySet() {
    const result = await sendRequest(
        `https://${location.hostname}/products/items/set/${setId}/buy/`,
        {method: "POST"}
    );

    if (!result.ok) {
        alert("Error");
        location.reload();
    }

    renderItemPrize(set.title, set.price, set.image_path, "Receive");
}


export async function getSet(id) {
    const setImg = document.getElementById('case-img');
    const setTitle = document.getElementById('case-title');
    const setItems = document.getElementById('case-items');

    setId = id;

    const result = await sendRequestJson(
        `https://${location.hostname}/products/items/set/${id}/`,
        {method: "GET"}
    );

    set = result;

    setTitle.innerHTML = result.title;
    setImg.src = result.image_path;

    document.getElementById('case-drop-data').style = "display: flex;gap: 1ch;"
    document.getElementById('price-label-span').innerHTML = `${result.price} <img style="height: 2ch;" src="/core/static/img/scrap.png">`
    document.getElementById('case-desc').innerHTML = result.description;

    result.items.forEach((element) => {
        setItems.innerHTML += `
            <article class="item-card" style="background: url(/core/static/img/card-bg-yellow.png);background-size: cover;">
                <div class="dropped-content">
                    <div class="item-numeric-info">
                        <span class="item-price yellow" style="width: 100%;"><span>${element.price}</span></span>
                    </div>

                    <div style="display: grid;grid-template-rows: 1fr;grid-template-columns: 1fr;width: 100%;max-width: 100%;justify-items: center;align-items: center;">
                        <img src="/core/static/img/card-jd-logo.png" style="grid-row: 1;grid-column: 1;width: 100%;">
                        <img src="${element.image_path}" style="width: 100%;grid-row: 1;grid-column: 1;">
                    </div>

                    <span class="item-title">${element.title}</span>
                </div>
            </article>
        `;
    });

    if ((await getUserData()).balance > result.price) {
        Array.from(document.getElementById('open-case-btn').children).forEach((element) => {
            element.classList.remove('noactive');
            return
        })
        document.getElementById('open-case-btn').onclick = () => {
            buySet()
        };
    }
}


window.buySet = buySet;
window.getSet = getSet;
