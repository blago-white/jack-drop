import { printPrizeItem } from "./animations.js";

const wheel = document.getElementById('wheel-canvas');

const degrees = {
    "freeSkin": 360,
    "freeSkinContract": (360/5),
    "caseDiscount": 2*(360/5),
    "freeSkinUpgrade": 3*(360/5),
    "promoCode": 4*(360/5),
};

const tiles = {
    "freeSkin": "t_e",
    "freeSkinContract": "s_d",
    "caseDiscount": "f_r",
    "freeSkinUpgrade": "f_v",
    "promoCode": "f_t",
}

const backgrounds = {
    "freeSkin": "1",
    "freeSkinContract": "5",
    "caseDiscount": "4",
    "freeSkinUpgrade": "3",
    "promoCode": "2",
}

const responseTypes = {
    "F": "freeSkin",
    "C": "freeSkinContract",
    "D": "caseDiscount",
    "U": "freeSkinUpgrade",
    "P": "promoCode",
}

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
          "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
        ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
};

let prizeTitlePrefixes;

if (getCookie('lang') == 'ru') {
    prizeTitlePrefixes = {
        "F": "Получите",
        "C": "Предмет для контракта",
        "D": "Скидка на кейс",
        "U": "Предмет для апгрейда",
        "P": "Промокод получен"
    }
} else {
    prizeTitlePrefixes = {
        "F": "You win",
        "C": "You win for contract",
        "D": "You win discount",
        "U": "You win for upgrade",
        "P": "You win promocode"
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function randomIntFromInterval(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

async function startRotate(promocode) {
    document.getElementById('start-btn').style.display = 'none';
    document.getElementById('clock').style.display = 'none';
    document.getElementById('code-btn').style.display = 'none';
    document.getElementById('cancel-code-btn').style.display = 'none';
    document.getElementById('inn-wheel').style.justifyContent = 'center';
    document.getElementById('game-title').style.margin = '0px';

    wheel.style.transition = `all 10s cubic-bezier(0.42, 0, 0.18, 0.99) 0s`;

    const result = await getResult(promocode);

    if (!result) {
        location.href = location.href;
    }

    const result_till = responseTypes[result.prize_type];

    wheel.style.transform = `rotate(${360*5 + degrees[result_till] + randomIntFromInterval(0, 50)}deg)`;

    setTimeout(
        () => {
            document.getElementById(tiles[result_till]).classList.add('active');
//            document.getElementById('wheel-canvas').src = `/core/static/img/wheel-${backgrounds[result_till]}.png`;

            if (result.prize_type == "D") {
                printPrizeItem(
                    result.prize.case.image_path,
                    `${result.prize.discount}%`,
                    `-${result.prize.discount}% -> ${result.prize.case.title}`,
                )
            } else {
                printPrizeItem(
                    result.prize.image_path,
                    result.prize.price,
                    `${prizeTitlePrefixes[result.prize_type]} "${result.prize.title}"`,
                )
            }
        },
        10000
    )
}


async function getResult(promocode) {
    const myHeaders = new Headers();
    const formdata = new FormData();

    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("X-CSRFToken", document.cookie.split("=")[1].split(";")[0]);

    let body = {};

    if (promocode) {
        body = {"promocode": promocode}
    }

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify(body),
      redirect: "follow"

    };

    const response = await sendRequest(`https://${location.hostname}/products/games/fortune-wheel/`, requestOptions);

    if (!response.ok) {
        makeWarn(await response.json());
        return {};
    }

    return await response.json();
}


async function startRotatePromo() {
    const input = document.getElementById('code-inp');

    const promocode = input.value.toUpperCase();

    if (!true) {
        input.value = '';
        input.style.outline = '3px solid red';
        makeWarn("Only 8 symbols");
    } else {
        await startRotate(promocode)
    }
}


function enterPromo() {
    document.getElementById('c-d-desc').remove();
    document.getElementById('clock').innerHTML = `
        <input type="text"
               maxlength="8"
               class="button"
               id="code-inp"
               style="padding-block: 1ch;text-align: center;"
               oninput="this.style.outline = 'none';"
               placeholder="Promocode">
    `;

    document.getElementById('code-btn').style.marginTop = 'calc(100vw * calc(24.1 / var(--reference-display-w)))';
    document.getElementById('cancel-code-btn').style = 'display: grid;margin-top: calc(100vw * calc(24.1 / var(--reference-display-w)));';

    document.getElementById('code-btn').onclick = startRotatePromo;
}

async function addLoginRequire() {
    if (!(await getAuthenticated())) {
        let c = false;

        document.getElementById('game-title').innerHTML = document.getElementById('long-enter-text').innerHTML;
        document.getElementById('game-title').style = 'padding: 0px';

        Array.from(document.getElementById('start-btn').children).forEach((element) => {
            if (c) {
                element.innerHTML = document.getElementById('short-enter-text').innerHTML;
            } else {
                element.style = '';
            }

            c = true;
        })

        document.getElementById('start-btn').onclick = () => {
            location.href = '/auth/';
        };
    }
}

window.startRotate = startRotate;
window.enterPromo = enterPromo;

addLoginRequire();
