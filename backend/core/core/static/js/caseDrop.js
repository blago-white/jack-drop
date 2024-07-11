import { renderItemPrize, renderPrize } from "./prize.js";

const dropItemsString = document.getElementById('items');
const dropItems = new Map();
const dropItemsPositions = new Map();
let caseId = null;


function gcd () {
    const w = screen.width;
    const h = screen.height;

    return w/h;
}

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
};

function setCookie(name, value, options = {}) {

    options = {
        path: '/',
        ...options
    };

    if (options.expires instanceof Date) {
        options.expires = options.expires.toUTCString();
    }

    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

    for (let optionKey in options) {
        updatedCookie += "; " + optionKey;
        let optionValue = options[optionKey];
        if (optionValue !== true) {
            updatedCookie += "=" + optionValue;
        }
    }

    document.cookie = updatedCookie;
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


function showAgreement() {
    renderPrize(`
        <div style="margin-inline: 4vw;display: grid;grid-template-rows: 1fr;grid-template-columns: 1fr;display: grid;grid-template-rows: 1fr;grid-template-columns: 1fr;justify-items: center;align-items: end;">
            <img src="/core/static/img/banner-man-agree.png" style="grid-row: 1;grid-column: 1;max-height: 45vh;">
            <h3 style="margin: 0px;grid-row: 1;grid-column: 1;font-size: calc(100vw* calc(54 / var(--reference-display-w)));text-align: center;">
                ПОДТВЕРДИТЕ<br>СОГЛАСИЕ
            </h3>
            <div style="gap: calc(100vw * calc(16 / var(--reference-display-w)));margin-top: calc(100vw * calc(43 / var(--reference-display-w)));display: flex;justify-content: flex-start;width: 100%;">
                <input type="checkbox" id="agreement-1" style="height: 3ch;width: 3ch;">
                <label class="agreement-label" style="color: #979797;font-size: calc(100vw * calc(24 / var(--reference-display-w)))" for="agreement">Я ЧТО МНЕ БОЛЬШЕ 18 ЛЕТ</label>
            </div>
            <div style="gap: calc(100vw * calc(16 / var(--reference-display-w)));margin-block: calc(100vw * calc(43 / var(--reference-display-w)));display: flex;justify-content: flex-start;width: 100%;">
                <input type="checkbox" id="agreement-2" style="height: 3ch;width: 3ch;">
                <label class="agreement-label" style="color: #979797;font-size: calc(100vw * calc(24 / var(--reference-display-w)))" for="agreement">Я ПРИНИМАЮ УСЛОВИЯ <a style="color: #0047FF;" href="/agreement/">ПОЛЬЗОВАТЕЛЬСКОГО СОГЛАШЕНИЯ</a></label>
            </div>
        </div>
        <div style="display: flex;flex-direction: row;gap: 2ch;">
            <button class="super-button" style="font-family: 'Gilroy SemiBold';" onclick="agree();">
                <span class="super-button-bg" style="background: radial-gradient(50% 50% at 50% 50%, rgba(79, 160, 255, 0.8) 0%, rgba(0, 71, 255, 0.8) 100%);"></span>
                <span class="super-button-text" style="font-size: x-large">Agree</span>
            </button>
            <button class="super-button" style="font-family: 'Gilroy SemiBold'" onclick="closePrizeWindow();">
                <span class="super-button-bg" style="background: #979797;box-shadow: none;"></span>
                <span class="super-button-text" style="font-size: x-large">Cancel</span>
            </button>
        </div>
    `);
}

function agree() {
    if (!(document.getElementById('agreement-1').checked && document.getElementById('agreement-2').checked)) {
        alert("Fill all fields");
        return false;
    }

    setCookie('agree-cases', 1);
    closePrizeWindow(location.href);
}

async function dropCase() {
    if (!getCookie('agree-cases')) {
        showAgreement();
        return;
    }

    const headers = new Headers();

    headers.append("Content-Type", "application/json");
    headers.append("X-CSRFToken", getCookie("csrftoken"));

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
    const gap = 100 * vw * (48 / 1920);

    if (gcd() > 1/1) {
        const partWith = 100 * vw * (217 / 1920);

        const biasVal = gap + partWith + 1;

        dropItemsString.style.marginLeft = `-${((biasVal * count) * 5) + ((to-3) * biasVal)}px`;
    } else {
        const partWith = 100 * vw * (331 / 960) + 5;

        const biasVal = gap + partWith;

        dropItemsString.style.marginTop = `-${((biasVal * count) * 5) + ((to) * biasVal)}px`;
    }
}

window.getCase = getCase;
window.dropCase = dropCase;
window.setCookie = setCookie;
window.agree = agree;
