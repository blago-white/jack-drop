import { renderItemPrize } from "./prize.js";

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


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function randomIntFromInterval(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

async function startRotate() {
    let d = 0;

    document.getElementById('start-btn').style.display = 'none';

    wheel.style.transition = `all 10s cubic-bezier(0.42, 0, 0.18, 0.99) 0s`;

    const result = await getResult();

    console.log(result);

    const result_till = responseTypes[result.prize_type];

    wheel.style.transform = `rotate(${360*5 + degrees[result_till] + randomIntFromInterval(0, 50)}deg)`;

    setTimeout(
        () => {
            document.getElementById(tiles[result_till]).classList.add('active');
            document.getElementById('wheel-canvas').src = `/core/static/img/wheel-${backgrounds[result_till]}.png`;
            renderItemPrize(result.prize.title, result.prize.price, result.prize.image_path, "Amazing!");
        },
        10000
    )
}


async function getResult() {
    const myHeaders = new Headers();
    const formdata = new FormData();

    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("X-CSRFToken", document.cookie.split("=")[1].split(";")[0]);

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify({}),
      redirect: "follow"

    };

    const response = await fetch("http://localhost/products/games/fortune-wheel/", requestOptions);

    return await response.json();
}

window.startRotate = startRotate;
