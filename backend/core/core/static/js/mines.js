const gameFields = document.getElementById('game-fields');

let lossStep = null;
let gameStarted = false;
let currentStep = 0;
let countMines = 0;


function iterField(id) {
    if (!gameStarted) {
        return false;
    }

    if (currentStep == lossStep) {
        document.getElementById(id).innerHTML += `
            <img src="/core/static/img/seeds.png" style="width: 90%;margin-inline: 5%;">
        `;
        alert("End!");
        gameStarted = false;
    } else {
        document.getElementById(id).innerHTML += `
            <img src="/core/static/img/pumpkin.png" style="width: 90%;margin-inline: 5%;">
        `
    }

    currentStep++;
}


async function sendMakeRequest(formData) {
    const myHeaders = new Headers();

    myHeaders.append("X-CSRFToken", document.cookie.split("=")[1].split(";")[0]);
    myHeaders.append("Content-Type", "application/json");

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify(formData),
      redirect: "follow"
    };

    const response = await fetch(
        `http://localhost/products/games/mines/`,
        requestOptions
    );

    return await response.json();
}

async function makeMinesGame() {
    const formData = new FormData(document.getElementById('mines-game-form'));

    countMines =  parseFloat(formData.get("count_mines")),

    result = await sendMakeRequest({
        "count_mines": parseFloat(formData.get("count_mines")),
        "user_deposit": parseFloat(formData.get("user_deposit"))
    });

    console.log(result);

    lossStep = Math.min(25-countMines, result.loss_step);

    gameStarted = true;

    document.getElementById('controls').style = 'opacity: .2;cursor: default;pointer-events: none;';

    return false;
}

function renderFields() {
    for (i = 0; i < 25; i++) {
        gameFields.innerHTML += `
            <div id="${i}" onclick="iterField(${i})" style="cursor: pointer;"></div>
        `
    }
}

function multipleDeposit(factor) {
    const current = document.getElementById('depo-input');
    current.value = parseFloat(current.value) * parseFloat(factor);
    return false;
}

function changeGameVals() {
    const value = Math.max(1, Math.min(24, parseFloat(document.getElementById('mines-count').value)));

    document.getElementById('mines-count').value = value;

    const countEmpty = 25 - value;

    document.getElementById('count-seeds').innerHTML = value;
    document.getElementById('count-pumpkin').innerHTML = countEmpty;

    return false;
}

renderFields();

document.getElementById('mines-count').addEventListener('input', changeGameVals);
