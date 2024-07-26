import { renderItemPrize } from "./prize.js";


let setId;
let set;

async function buySet() {
    const result = await sendRequest(
        `http://${location.hostname}/products/items/set/${setId}/buy/`,
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
        `http://${location.hostname}/products/items/set/${id}/`,
        {method: "GET"}
    );

    set = result;

    setTitle.innerHTML = result.title;
    setImg.src = result.image_path;

    document.getElementById('case-drop-data').style = "display: flex;gap: 1ch;"
    document.getElementById('price-label-span').innerHTML = `${result.price} <img style="height: 2ch;" src="/core/static/img/scrap.png">`

    result.items.forEach((element) => {
        setItems.innerHTML += `
            <article style="display: flex;flex-direction: column;align-items: center; gap: 1ch;">
                <div class="dropped rare">
                        <div class="w-line"></div>
                        <div class="dropped-content">
                            <span>${element.title}</span>
                            <div style="display: flex;flex-direction: row;gap: 1ch;">
                                <span class="item-price blue"><span>${element.price}</span></span>
                            </div>
                            <img src="${element.image_path}">
                        </div>
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
