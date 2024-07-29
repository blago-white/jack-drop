import { renderItemPrize } from "./prize.js";

const battlesList = document.getElementById('battles');
const battlesHead = document.getElementById('battles-head');
const battlesTable = document.getElementById('battles-table');

const foundingLabel = document.getElementById('founding-label');
const battlesRequest = document.getElementById('battle-request-controls');

const battleSocket = new WebSocket(`ws://${location.hostname}/products/ws/battle/`);
let sendedRequestNow = false;
let connected = false;
let requestCaseId = null;
let itemsPositions = new Map();
let battleCases = new Map();
let activeCase;

let currentCaseImage;

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function gcd () {
    const w = screen.width;
    const h = screen.height;

    return w/h;
}

function animateRoulette(toid, caseItems, dropItemsString) {
    const vw = window.innerWidth / 100;
    const gap = 100 * vw * (40 / 1920);

    let to;
    let c = 0;

    caseItems.forEach((element) => {
        if (element.case_item_id == toid) {
            to = c;
        }

        c++;
    });

    const count = caseItems.length;

    if (gcd() > 1/1) {
        const partWith = 100 * vw * (200 / 1920);

        const biasVal = gap + partWith - count;

        dropItemsString.style.transition = `filter .5s cubic-bezier(0.4, 0, 1, 1), margin 7s cubic-bezier(0.08, 0.22, 0.22, 1)`;

        dropItemsString.style.filter = `blur(.1ch)`;

        setTimeout(() => {
            dropItemsString.style.marginLeft = `-${(biasVal * count) + ((to) * biasVal)}px`;
        })

        setTimeout(() => {dropItemsString.style.transition = `filter 4s cubic-bezier(0.4, 0, 1, 1), margin 7s cubic-bezier(0.08, 0.22, 0.22, 1)`;dropItemsString.style.filter = `blur(0ch)`}, 1000)
    } else {
        const partWith = 100 * vw * (200 / 960) + 7;

        const biasVal = gap + partWith;

        dropItemsString.style.marginTop = `-${((biasVal * count) * 7) + ((to+1) * biasVal)}px`;
    }
}

async function renderDrops(username1, username2, battleImgPath, caseItems, dropped1, dropped2) {
    document.getElementById('battle-sec').innerHTML = `
            <div class="drops-window" id="drops" style="opacity: 0;">
                <div class="battle-info">
                    <span class="user-info">
                        <img src="/core/static/img/account-avatar.png">
                        <span>${username1}</span>
                    </span>

                    <img src="${battleImgPath}" class="battle-case-img">

                    <span class="user-info">
                        <img src="/core/static/img/account-avatar.png">
                        <span>${username2}</span>
                    </span>
                </div>
                <div class="drops-roulette-window">
                    <div class="drop-roulette" id="roulette1">
                        <img class="arrow" src="/core/static/img/case-string-arrow.png">
                        <div class="case-items-string" id="items-string">
                            <ul class="items" id="items1">
                            </ul>
                        </div>
                    </div>
                    <div class="drop-roulette" id="roulette2">
                        <img class="arrow" src="/core/static/img/case-string-arrow.png">
                        <div class="case-items-string" id="items-string">
                            <ul class="items" id="items2">
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
    `;

    for (let i = 0;i<7;i++) {
        caseItems.forEach((element) => {
            document.getElementsByClassName('items')[0].innerHTML += `
                <article class="dropped mono 1-itm-${element.case_item_id}">
                    <div class="w-line"></div>
                    <div class="dropped-content">
                        <span>${element.title}</span>
                        <img src="${element.image_path}">
                    </div>
                </article>
            `;

            document.getElementsByClassName('items')[1].innerHTML += `
                <article class="dropped mono 2-itm-${element.case_item_id}">
                    <div class="w-line"></div>
                    <div class="dropped-content">
                        <span>${element.title}</span>
                        <img src="${element.image_path}">
                    </div>
                </article>
            `;
        })
    };

    const r1 = document.getElementById('items1');
    const r2 = document.getElementById('items2');

    animateRoulette(dropped1.case_item_id, caseItems, r1);
    animateRoulette(dropped2.case_item_id, caseItems, r2);

    Array.from(document.getElementsByClassName(`1-itm-${dropped1.case_item_id}`)).forEach((elem) => {
        elem.style.background = "radial-gradient(50% 50% at 50% 50%, rgba(79, 160, 255, 0.8) 0%, rgba(0, 71, 255, 0.8) 100%)";
    });
    Array.from(document.getElementsByClassName(`2-itm-${dropped2.case_item_id}`)).forEach((elem) => {
        elem.style.background = "radial-gradient(50% 50% at 50% 50%, rgba(79, 160, 255, 0.8) 0%, rgba(0, 71, 255, 0.8) 100%)";
    });

    document.getElementById("battle-sec").style = 'grid-template-columns: 1fr;grid-template-rows: 2fr;';

    setTimeout(() => {
        document.getElementById("drops").style.opacity = 1;
    })
}

battleSocket.onmessage = async function(event) {
    let jsondata = JSON.parse(event.data);

    if (typeof jsondata === 'string') {
        jsondata = JSON.parse(jsondata);
    }

    if (jsondata.response_type == "list") {
        renderActiveRequests(jsondata.result);
        return;
    }

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
        hideRequestWindow();

        const item = jsondata.result.data.dropped_item_winner_id;

        if (gcd() > 1/1) {
            renderDrops(jsondata.result.data.winner_data.username, jsondata.result.data.loser_data.username, jsondata.result.data.battle_case.image_path, jsondata.result.case_items, jsondata.result.data.dropped_item_winner_id, jsondata.result.data.dropped_item_loser_id);
            await sleep(7000);
        }

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
}

function sendConnectRequest(case_id, initiator_id) {
    sendedRequestNow = true;

    battleSocket.send(JSON.stringify({"type": "ctr", "payload": {
        "battle_case_id": case_id,
        "initiator_id": initiator_id
    }}));
}

function onListBattles(case_id) {
    activeCase = battleCases.get(case_id);

    battleSocket.send(JSON.stringify({"type": "lbc", "payload": {
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
    currentCaseImage = document.getElementById(`case-img-${case_id}`).src;

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

    const response = await sendRequest(
        `http://${location.hostname}/products/games/battles/`,
        requestOptions
    );

    const result = await response.json();

    const startButtonText = document.getElementById('create-battle').innerHTML;

    result.forEach((element) => {
        battleCases.set(element.id, element);

        const count = element.battles_count;

        battlesTable.innerHTML += `
            <div class="battle">
                <div class="case-sign">
                    <img class="battle-case" src="${element.image_path}" id="case-img-${element.id}">
                    <span>${element.title}</span>
                </div>
                <span class="count-battles">${element.battles_count}</span>
                <span class="price">${element.price}</span>
                <div style="display: flex;flex-direction: row;">
                    <button onclick="onListBattles(${element.id});"
                            id="create-battle"
                            class="button button-colorized rose create-battle">
                    ПОДКЛ.
                    </button>
                    <button onclick="onCreateBattle(${element.id});"
                            id="create-battle"
                            class="button button-colorized blue create-battle">
                    ${startButtonText}
                    </button>
                </div>
            </div>
        `
    })
}

async function getStats() {
    const requestOptions = {
      method: "GET",
    };

    const response = await sendRequest(
        `http://${location.hostname}/products/games/battle-stats/`,
        requestOptions
    );

    const result = await response.json();

    document.getElementById('wins').innerHTML = result.wins || 0;
    document.getElementById('draw').innerHTML = result.draw || 0;
    document.getElementById('loses').innerHTML = result.loses || 0;
}

function renderActiveRequests(requests) {
    battlesHead.innerHTML = `
        <span style="text-align: start;">Кейс</span>
        <span>Игрок</span>
        <span style="text-align: end;">Действия</span>
    `

    battlesHead.style = 'grid-template-columns: repeat(3, 1fr);';

    battlesTable.innerHTML = '';

    if (requests.length > 0) {
        requests.forEach((element) => {
            battlesTable.innerHTML += `
                <div class="battle" style="grid-template-columns: repeat(3, 1fr);font-size: medium;">
                    <div class="case-sign">
                        <img class="battle-case" src="${activeCase.image_path}">
                        <span>${activeCase.title}<br>[${activeCase.price} р]</span>
                    </div>
                    <span class="case-sign" style="justify-content: start">
                        <img class="battle-case" src="/core/static/img/account-avatar.png">
                        <span>${element.username}</span>
                    </span>
                    <button onclick="sendConnectRequest(${activeCase.id}, ${element.user_id});"
                            id="create-battle"
                            class="button button-colorized rose create-battle">
                    ПОДКЛ.
                    </button>
                </div>
                `
        });
    } else {
        battlesTable.innerHTML = "Запросы на сражения не найдены!"
        battlesTable.style = `display: flex;align-items: center;justify-content: center;font-family: 'Gilroy SemiBold'`;
    }

    document.getElementById('show-btn-text').innerHTML = 'назад';
    document.getElementById('show-btn-bg').style = 'background: gray;box-shadow: none;';
    document.getElementById('show-btn').onclick = () => {location.href = location.href};
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

    const response = await sendRequest(
        `http://${location.hostname}/products/games/battle-history/`,
        requestOptions
    );

    const result = await response.json();

    battlesTable.innerHTML = '';

    result.forEach((element) => {
        if ((!element.dropped_item_winner) || (!element.dropped_item_loser)) {
        } else {
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
        }
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
window.onListBattles = onListBattles;
