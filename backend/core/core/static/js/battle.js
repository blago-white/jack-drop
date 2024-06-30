import { renderItemPrize } from "./prize.js";

const battlesList = document.getElementById('battles');
const battlesHead = document.getElementById('battles-head');
const battlesTable = document.getElementById('battles-table');

const foundingLabel = document.getElementById('founding-label');
const battlesRequest = document.getElementById('battle-request-controls');

const battleSocket = new WebSocket("ws://localhost/products/ws/battle/");
let sendedRequestNow = false;
let connected = false;
let requestCaseId = null;

battleSocket.onmessage = function(event) {
    let jsondata = JSON.parse(event.data);

    if (typeof jsondata === 'string') {
        jsondata = JSON.parse(jsondata);
    }

    console.log(jsondata);

    if (!(jsondata["result"]["result"] && jsondata["result"]["result"]["success"])) {
        if (jsondata["result"]["error"]) {
            alert(jsondata["result"]["error"]);
        }

        if (jsondata["result"]["fatal"]) {
            hideRequestWindow();
            return
        }
    }

    if (!jsondata["result"]["success"] && sendedRequestNow && connected) {
        if (jsondata["result"]["error"]) {
            alert(jsondata["result"]["error"]);
        } else {
            alert("Erorr with connect");
        }

        hideRequestWindow();
        return
    }

    if (jsondata["result"]["success"] && jsondata["response_type"] == "result") {
        alert("Battle finished!");
        console.log(jsondata);

        hideRequestWindow();

        const item = jsondata["result"]["data"]["dropped_item_winner_id"];

        renderItemPrize(`You win ${item.title}!`, item.price, item.image_path, "Amazing!");

        return
    }

    if (jsondata["response_type"] == "result" && !jsondata["result"]["success"]) {
        alert(jsondata["result"]["error"]);

        hideRequestWindow();
        return
    }

    if (jsondata["result"]["success"] && jsondata["response_type"] == "create") {
        return
    }

    if (!jsondata["result"]["ok"] && sendedRequestNow && !connected) {
        sendConnectRequest(requestCaseId);
        console.log("SEND");
        connected = true;
    }
}


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function sendConnectRequest(case_id) {
    sendedRequestNow = true;

    battleSocket.send(JSON.stringify({"type": "ctr", "payload": {
        "battle_case_id": case_id
    }}));
}

function sendCreateRequest(case_id) {
    sendedRequestNow = true;

    battleSocket.send(JSON.stringify({"type": "cbr", "payload": {
        "battle_case_id": case_id
    }}));
}

async function onCreateBattle(case_id) {
    battlesHead.style.display = 'none';
    battlesTable.style.display = 'none';

    battlesRequest.style.display = 'flex';

    let c = 0;
    requestCaseId = case_id;

    sendCreateRequest(case_id);

    while (true) {
        await sleep(1000);
        c += 1;

        if (c % 4 == 0 && c > 0) {
            foundingLabel.innerHTML = foundingLabel.innerHTML.slice(0, -3);
        } else {
            foundingLabel.innerHTML += ".";
        }
    }
}

function hideRequestWindow() {
    battlesHead.style = '';
    battlesTable.style = '';

    battlesRequest.style.display = 'none';
    sendedRequestNow = false;
    requestCaseId = null;
}

function cancelRequest() {
    hideRequestWindow();

    battleSocket.send(JSON.stringify({"type": "crb", "payload": {}}));
}

async function getCases() {
    const requestOptions = {
      method: "GET",
    };

    const response = await fetch(
        `http://localhost/products/cases/api/v1/paid-cases/`,
        requestOptions
    );

    const result = await response.json();

    const startButtonText = document.getElementById('create-battle').innerHTML;

    result.forEach((element) => {
        battlesTable.innerHTML += `
            <div class="battle">
                <div class="case-sign">
                    <img class="battle-case" src="${element.image_path}">
                    <span>${element.title}</span>
                </div>
                <span class="count-battles">0</span>
                <span class="price">${element.price}</span>
                <button onclick="onCreateBattle(${element.id});" id="create-battle"
                        class="button button-colorized blue create-battle">
                    ${startButtonText}
                </button>
            </div>
        `
    })
}

async function getStats() {
    const requestOptions = {
      method: "GET",
    };

    const response = await fetch(
        `http://localhost/products/games/battle-stats/`,
        requestOptions
    );

    const result = await response.json();

    document.getElementById('wins').innerHTML = result.wins;
    document.getElementById('draw').innerHTML = result.draw;
    document.getElementById('loses').innerHTML = result.loses;
}

async function showHistory() {
    battlesHead.innerHTML = `
        <span style="text-align: start;">Кейс</span>
        <span>Предмет победителя</span>
        <span style="text-align: end;">Предмет проигравшего</span>
    `

    battlesHead.style = 'grid-template-columns: repeat(3, 1fr);';

    const requestOptions = {
      method: "GET",
    };

    const response = await fetch(
        `http://localhost/products/games/battle-history/`,
        requestOptions
    );

    const result = await response.json();

    battlesTable.innerHTML = '';

    result.forEach((element) => {
        battlesTable.innerHTML += `
            <div class="battle" style="grid-template-columns: repeat(3, 1fr);font-size: medium;">
                <div class="case-sign">
                    <img class="battle-case" src="${element.battle_case.image_path}">
                    <span>${element.battle_case.title}<br>[${element.battle_case.price} р]</span>
                </div>
                <span class="case-sign" style="justify-content: start">
                    <img class="battle-case" src=${element.dropped_item_winner.image_path}>
                    ${element.dropped_item_winner.title} <br>
                    [${element.dropped_item_winner.price} р]
                </span>
                <span class="case-sign" style="text-align: end;justify-content: end;">
                    <img class="battle-case" src=${element.dropped_item_loser.image_path}>
                    ${element.dropped_item_loser.title} <br>
                    [${element.dropped_item_loser.price} р]
                </span>
            </div>
        `
    });

    document.getElementById('show-btn-text').innerHTML = 'скрыть';
    document.getElementById('show-btn-bg').style = 'background: gray;box-shadow: none;';
    document.getElementById('show-btn').onclick = () => {location.href = location.href};
}

getCases();
getStats();

window.showHistory = showHistory;
window.cancelRequest = cancelRequest;
window.hideRequestWindow = hideRequestWindow;
window.onCreateBattle = onCreateBattle;
window.sendCreateRequest = sendCreateRequest;
window.sendConnectRequest = sendConnectRequest;
