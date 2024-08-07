import { renderItemPrize } from "./prize.js";

const gameFields = document.getElementById('game-fields');

let lossStep = 26;
let gameStarted = false;
let currentStep = 0;
let countMines = 0;
let deposit = 0;
let fundsDiff = 0;
let selected = new Set();


function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
};


async function iterField(id) {
    if (!gameStarted) {
        return false;
    }

    if (selected.has(id)) {return} else {selected.add(id)}

    const myHeaders = new Headers();

    myHeaders.append("X-CSRFToken", getCookie("csrftoken"));
    myHeaders.append("Content-Type", "application/json");

    const requestOptions = {
      method: "PUT",
      headers: myHeaders,
      body: JSON.stringify({}),
      redirect: "follow"
    };

    const response = await sendRequestJson(
        `http://${location.hostname}/products/games/mines/next/`,
        requestOptions
    );

    if (response.game_ended) {
        document.getElementById(id).innerHTML = `
            <img src="/core/static/img/seeds.png" style="width: 90%;margin-inline: 5%;">
        `;
        renderItemPrize("You lose scrap!", -deposit, "/core/static/img/scrap.png", "Ok");

        gameStarted = false;
    } else if (currentStep == (25 - countMines - 1)) {
        const requestOptions = {
          method: "DELETE",
          headers: myHeaders,
          body: JSON.stringify({}),
          redirect: "follow"
        };

        const response = await sendRequest(
            `http://${location.hostname}/products/games/mines/stop/`,
            requestOptions
        );

        renderItemPrize("You win scrap!", fundsDiff, "/core/static/img/scrap.png", "Amazing!");

        document.getElementById(id).innerHTML = `
            <img src="/core/static/img/pumpkin.png" style="width: 90%;margin-inline: 5%;">
        `
    } else if (!response.game_ended) {
        document.getElementById(id).innerHTML = `
            <img src="/core/static/img/pumpkin.png" style="width: 90%;margin-inline: 5%;">
        `;
        document.getElementById('receive').innerHTML = `
            Receive: ${response.win_amount} <img src="/core/static/img/scrap.png" style="width: 3ch">
        `;
    }

    currentStep++;
}

async function stopGame() {
    const myHeaders = new Headers();

    myHeaders.append("X-CSRFToken", getCookie("csrftoken"));
    myHeaders.append("Content-Type", "application/json");

    const requestOptions = {
      method: "DELETE",
      headers: myHeaders,
      body: JSON.stringify({}),
      redirect: "follow"
    };

    const response = await sendRequestJson(
        `http://${location.hostname}/products/games/mines/stop/`,
        requestOptions
    );

    renderItemPrize("You win scrap!", response.win_amount, "/core/static/img/scrap.png", "Ok");

    gameStarted = false;
}

async function sendMakeRequest(formData) {
    const myHeaders = new Headers();

    myHeaders.append("X-CSRFToken", getCookie("csrftoken"));
    myHeaders.append("Content-Type", "application/json");

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify(formData),
      redirect: "follow",
    };

    const response = await sendRequest(
        `http://${location.hostname}/products/games/mines/`,
        requestOptions
    );

    return response;
}

async function makeMinesGame() {
    const formData = new FormData(document.getElementById('mines-game-form'));

    countMines = parseFloat(formData.get("count_mines"));
    deposit = parseFloat(formData.get("user_deposit"));

    let result = await sendMakeRequest({
        "count_mines": parseFloat(formData.get("count_mines")),
        "user_deposit": parseFloat(formData.get("user_deposit"))
    });

    if (result.ok) {
        result = await result.json();

        lossStep = Math.min(25-countMines, result.loss_step);

        gameStarted = true;
        fundsDiff = result.user_funds_diff;

        document.getElementById('mines-game-form').innerHTML = `
            <div class="super-button">
                <span class="super-button-bg noactive"></span>
                <span class="super-button-text" style="gap: 0px;" id="receive">Receive: 0.0 <img src="/core/static/img/scrap.png" style="width: 3ch"></span>
            </div>
            <button class="super-button" type="submit" onclick="stopGame();return false;">
                <span class="super-button-bg"></span>
                <span class="super-button-text">Stop game!</span>
            </button>
        `;

//        document.getElementById('controls').style = 'opacity: .2;cursor: default;pointer-events: none;';
    } else {
        const resultJson = await result.json();

        Object.keys(resultJson).forEach((errorkey) => {
            if (errorkey >= "0" && errorkey <= "9") {
                alert(resultJson[errorkey]);
            } else {
                document.getElementById(errorkey).style.outline = '2px solid red';
                alert(resultJson[errorkey][0]);
            }
        });
    }

    return false;

}

function renderFields() {
    let i = 0;

    for (i = 0; i < 25; i++) {
        gameFields.innerHTML += `
            <div id="${i}" onclick="iterField(${i})" style="cursor: pointer;"></div>
        `
    }
}

function multipleDeposit(factor) {
    const current = document.getElementById('user_deposit');
    current.value = parseFloat(current.value) * parseFloat(factor);
    return false;
}

function changeGameVals() {
    const value = Math.max(1, Math.min(24, parseFloat(document.getElementById('count_mines').value)));

    if (parseFloat(document.getElementById('count_mines').value)) {
        document.getElementById('count_mines').value = value;

        const countEmpty = 25 - value;

        document.getElementById('count-seeds').innerHTML = value;
        document.getElementById('count-pumpkin').innerHTML = countEmpty;
    } else {
        document.getElementById('count-seeds').innerHTML = "-";
        document.getElementById('count-pumpkin').innerHTML = "-";
    }
    return false;
}

renderFields();

addEventListener("beforeunload", (event) => {stopGame()});

document.getElementById('count_mines').addEventListener('input', changeGameVals);

window.makeMinesGame = makeMinesGame;
window.sendMakeRequest = sendMakeRequest;
window.changeGameVals = changeGameVals;
window.iterField = iterField;
window.multipleDeposit = multipleDeposit;
window.stopGame = stopGame;
