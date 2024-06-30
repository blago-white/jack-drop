import { renderItemPrize } from "./prize.js";

const dropItemsString = document.getElementById('items');
const dropItems = new Map();
const dropItemsPositions = new Map();
let caseId = null;


function gcd () {
    const w = screen.width;
    const h = screen.height;

    return w/h;
}


export async function getCase(id) {
    const formdata = new FormData();
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    caseId = id;

    const response = await fetch(
        `http://localhost/products/cases/api/v1/case/${id}/items/`,
        requestOptions
    );

    const result = await response.json();

    console.log(result);

    let line = ``;
    let c = 0;

    result.items.forEach((element) => {
        dropItems.set(element.id, element);
        line += `
            <article class="dropped mono itm-${element.case_item_id}">
                    <div class="w-line"></div>
                    <div class="dropped-content">
                        <span>${element.title}</span>
                        <img src="${element.image_path}">
                    </div>
            </article>
        `;
        c ++;
        dropItemsPositions.set(element.case_item_id, c);
    });

    dropItemsString.innerHTML += line + line + line + line + line + line + line;

    await dropCase();
}


async function dropCase() {
    const headers = new Headers();

    headers.append("Content-Type", "application/json");
    headers.append("X-CSRFToken", document.cookie.split("=")[1].split(";")[0]);

    const requestOptions = {
      method: "POST",
      headers: headers,
      body: JSON.stringify({}),
      redirect: "follow"
    };

    const response = await fetch(
        `http://localhost/products/games/drop/${caseId}/`,
        requestOptions
    );

    if (!response.ok) {
        alert(await response.json());
        window.history.back();
        return false;
    }

    const result = await response.json();

    const dropped = result.dropped_item;

    console.log('---R', result);

    const position = dropItemsPositions.get(dropped.id);

    console.log(position);

    console.log(dropped);

    console.log(dropItemsPositions);

    animateRoulette(position, dropItems.size);

    setTimeout(() => {
        console.log("itm", dropped.id);

        Array.from(document.getElementsByClassName(`itm-${dropped.id}`)).forEach((elem) => {
            elem.style.background = "radial-gradient(50% 50% at 50% 50%, rgba(79, 160, 255, 0.8) 0%, rgba(0, 71, 255, 0.8) 100%)";
        });

        setTimeout(() => {
            renderItemPrize(dropped.title, dropped.price, dropped.image_path, "Amazing!")
        }, 500);
    }, 5000);
}

function animateRoulette(to, count) {
    const vw = window.innerWidth / 100;

    if (gcd() > 1/1) {
        const gap = 100 * vw * (48 / 1920);

        const partWith = 100 * vw * (217 / 1920);

        const biasVal = gap + partWith + 1;

        console.log(count, count*5, to-3, to);

        dropItemsString.style.marginLeft = `-${((biasVal * count) * 5) + ((to-3) * biasVal)}px`;

    }
}

window.getCase = getCase;
window.dropCase = dropCase;
