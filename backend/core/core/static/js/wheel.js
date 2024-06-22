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


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function randomIntFromInterval(min, max) { // min and max included
  return Math.floor(Math.random() * (max - min + 1) + min);
}

async function startRotate() {
    let d = 0;

    document.getElementById('start-btn').style.display = 'none';

    wheel.style.transition = `all 10s cubic-bezier(0.42, 0, 0.18, 0.99) 0s`;

    wheel.style.transform = `rotate(${360*5 + degrees["promoCode"] + randomIntFromInterval(0, 50)}deg)`;

    setTimeout(
        () => {
            document.getElementById(tiles["promoCode"]).classList.add('active');
            document.getElementById('wheel-canvas').src = `/static/img/wheel-${backgrounds["promoCode"]}.png`;
        },
        10000
    )
}
