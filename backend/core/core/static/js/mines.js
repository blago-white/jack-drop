import { renderItemPrize, renderPrize } from "./prize.js";

const gameFields = document.getElementById('game-fields');

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

        document.getElementById('info-banner').innerHTML = 'Не повезло, попробуйте еще раз!'
        document.getElementById('info-banner-bg').style.background = '#FF007A';


        document.getElementById('action-button').onclick = () => {
            location.href = location.href
        };

        document.getElementById('action-button-text').innerHTML = 'Мне повезет!'

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
        document.getElementById('info-banner').innerHTML = `
            Receive: ${response.win_amount} <img src="/core/static/img/scrap.png" style="width: 3ch">
        `;
    }

    currentStep++;

    if (currentStep == 1) {
        document.getElementById('stop-btn-bg').classList.remove("noactive");
        document.getElementById('controls').style = 'none';
    }
}

async function stopGame() {
    if (currentStep == 0) {
        return false;
    }

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

        gameStarted = true;
        fundsDiff = result.user_funds_diff;

        document.getElementById('mines-game-form').innerHTML = `
            <div class="super-button">
                <span class="super-button-bg noactive" id="info-banner-bg"></span>
                <span class="super-button-text" id="info-banner" style="gap: 0px;" id="receive">Receive: 0.0 <img src="/core/static/img/scrap.png" style="width: 3ch"></span>
            </div>
            <button class="super-button" id="action-button" type="submit" onclick="stopGame();return false;">
                <span class="super-button-bg noactive" id="stop-btn-bg"></span>
                <span class="super-button-text" id="action-button-text">Stop game!</span>
            </button>
        `;

        document.getElementById('controls').style = 'opacity: .2;cursor: default;pointer-events: none;';
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

async function multipleDeposit(factor=-1) {
    const current = document.getElementById('user_deposit');

    if (factor == -1) {
        current.value = (await getAuthenticated()).balance;
    } else {
        current.value = parseFloat(current.value) * parseFloat(factor);
    }

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

async function changeBtn() {
    if (!(await getAuthenticated())) {
        document.getElementById('count-pumpkin').innerHTML = "???";
        document.getElementById('count-seeds').innerHTML = "???";

        renderPrize(
            `
                <img src="/core/static/img/banner-man.png">
                <h3 style="text-transform: none;">${document.getElementById('long-enter-text').innerHTML}</h3>
                <button class="super-button" style="font-family: 'Gilroy SemiBold'" onclick="location.href = '/auth/'">
                    <span class="super-button-bg"></span>
                    <span class="super-button-text" style="font-size: x-large">${document.getElementById('short-enter-text').innerHTML}</span>
                </button>
            `
        );
    }
}

renderFields();
changeBtn();

addEventListener("beforeunload", (event) => {stopGame()});

document.getElementById('count_mines').addEventListener('input', changeGameVals);

window.makeMinesGame = makeMinesGame;
window.sendMakeRequest = sendMakeRequest;
window.changeGameVals = changeGameVals;
window.iterField = iterField;
window.multipleDeposit = multipleDeposit;
window.stopGame = stopGame;
