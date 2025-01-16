import { printPrizeItem } from "./animations.js";

const dropItemsString = document.getElementById('items');
const dropItems = new Map();
const dropItemsPositions = new Map();
let caseId = null;


function gcd () {
    const w = screen.width;
    const h = screen.height;

    return w/h;
}

function getCardColor(itemsCount, indexCurrent) {
    if (indexCurrent <= itemsCount/10) {
        return "yellow"
    } else if (indexCurrent <= itemsCount * 0.25) {
        return "red"
    } else if (indexCurrent <= itemsCount * 0.45) {
        return "pink"
    } else if (indexCurrent <= itemsCount * 0.7) {
        return "purple"
    } else {
        return "blue"
    }
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

    const response = await sendRequest(
        `https://${location.hostname}/products/cases/api/v1/case/${id}/items/`,
        requestOptions
    );

    const result = await response.json();

    console.log(result);

    let line = [];
    let c = 0;
    let rareColor;

    result.items.forEach((element) => {
        dropItems.set(element.id, element);

        rareColor = getCardColor(result.items.length, c);

        line.push(`
            <article class="item-card itm-${element.case_item_id}" style="background: url(/core/static/img/card-bg-${rareColor}.png);background-size:cover;">
                <div class="dropped-content">
                        <div class="item-numeric-info">
                            <span class="item-price ${rareColor}"><span>${element.price}</span> <img src="/core/static/img/gear.png"></span>
                        </div>

                        <div style="display: grid;grid-template-rows: 1fr;grid-template-columns: 1fr;width: 100%;max-width: 100%;justify-items: center;align-items: center;">
                            <img src="/core/static/img/card-jd-logo.png" style="grid-row: 1;grid-column: 1;width: 100%;">
                            <img src="${element.image_path}" class="item-card-img" style="width: 66%;grid-row: 1;
                            grid-column: 1;">
                        </div>

                        <span class="item-title">${element.title}</span>
                </div>
            </article>
        `);
        c ++;
        dropItemsPositions.set(element.case_item_id, c);
    });

    let lineDrops = [];
    c = 0;

    result.items.forEach((element) => {
        dropItems.set(element.id, element);

        rareColor = getCardColor(result.items.length, c);

        lineDrops.push(`
            <article class="item-card itm-${element.case_item_id}" style="background: url(/core/static/img/card-bg-${rareColor}.png);background-size:cover;" id="drop-${element.case_item_id}">
                <div class="dropped-content">
                        <div class="item-numeric-info">
                            <span class="item-price ${rareColor}"><span>${element.price}</span> <img src="/core/static/img/gear.png"></span>
                        </div>

                        <div style="display: grid;grid-template-rows: 1fr;grid-template-columns: 1fr;width: 100%;max-width: 100%;justify-items: center;align-items: center;">
                            <img src="/core/static/img/card-jd-logo.png" style="grid-row: 1;grid-column: 1;width: 100%;">
                            <img src="${element.image_path}" class="item-card-img" style="width: 66%;grid-row: 1;
                            grid-column: 1;">
                        </div>

                        <span class="item-title">${element.title}</span>
                </div>
            </article>
        `);
        c ++;
        dropItemsPositions.set(element.case_item_id, c);
    });

    line = (line.sort(() => Math.random() - 0.5)).join("");
    lineDrops = (lineDrops.sort(() => Math.random() - 0.5)).join("");

    dropItemsString.innerHTML += line + line + line + line + line + line + lineDrops + line + line;

    await dropCase();
}

async function dropCase() {
    const urlParams = new URLSearchParams(window.location.search);
    const bonusCase = urlParams.get('bonus');

    const headers = new Headers();

    headers.append("Content-Type", "application/json");
    headers.append("X-CSRFToken", getCookie("csrftoken"));

    const requestOptions = {
      method: "POST",
      headers: headers,
      body: JSON.stringify({}),
      redirect: "follow"
    };

    const response = await sendRequest(
        `https://${location.hostname}/products/games/drop/${caseId}/${bonusCase ? '?bonus=1' : ''}`,
        requestOptions
    );

    if (!response.ok) {
        window.history.back();
        return false;
    }

    const result = await response.json();

    const dropped = result.dropped_item;

    const position = dropItemsPositions.get(dropped.id);

    animateRoulette(document.getElementById(`drop-${dropped.id}`).getBoundingClientRect());

    setTimeout(() => {
        console.log("itm", dropped.id);

        Array.from(document.getElementsByClassName(`itm-${dropped.id}`)).forEach((elem) => {
            elem.style.background = "radial-gradient(50% 50% at 50% 50%, rgba(79, 160, 255, 0.8) 0%, rgba(0, 71, 255, 0.8) 100%)";
        });

        setTimeout(() => {
            printPrizeItem(dropped.image_path, dropped.price, dropped.title, `/case/${caseId}`);
        }, 500);
    }, 7000);
}

function animateRoulette(to) {
    const vw = window.innerWidth / 100;

    console.log(gcd());

    new Audio(location.protocol + '//' + location.host + '/core/static/mp3/case.mp3').play();

    if (gcd() > 1/1) {
        dropItemsString.style.marginLeft = `-${to.right - (((100 * vw * (326 / 1920)) + (100 * vw * (48 / 1920)))*3)}px`;

        console.log(`${to}`);

        dropItemsString.style.transition = `filter .5s cubic-bezier(0.4, 0, 1, 1), margin 7s cubic-bezier(0.08, 0.22, 0.22, 1)`;
        dropItemsString.style.filter = `blur(.1ch)`;

        setTimeout(() => {dropItemsString.style.transition = `filter 4s cubic-bezier(0.4, 0, 1, 1), margin 7s cubic-bezier(0.08, 0.22, 0.22, 1)`;dropItemsString.style.filter = `blur(0ch)`}, 1000)
    } else {
        dropItemsString.style.marginTop = `-${to.bottom - (3*((100 * vw * (331 / 960) + 3.5) + (100 * vw * (48 / 1920))))}px`;
        dropItemsString.style.transition = `filter .5s cubic-bezier(0.4, 0, 1, 1), margin 7s cubic-bezier(0.08, 0.22, 0.22, 1)`;
        dropItemsString.style.filter = `blur(.1ch)`;

        setTimeout(() => {dropItemsString.style.transition = `filter 4s cubic-bezier(0.4, 0, 1, 1), margin 7s cubic-bezier(0.08, 0.22, 0.22, 1)`;dropItemsString.style.filter = `blur(0ch)`}, 1000)
    }
}

window.getCase = getCase;
window.dropCase = dropCase;
