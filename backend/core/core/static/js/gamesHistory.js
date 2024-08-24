const table = document.getElementById('game-history-table');
const empty = document.getElementById('empty-hist');

const gamesMapping = {
    "U": "Upgrade",
    "C": "Contract",
    "B": "Battle",
    "M": "Mines"
};

let section;

Array.from(document.getElementById('main-nav').children).forEach((element) => {
    console.log(element.className, element.className.slice(-6));

    if (element.className.slice(-6) == "active") {
        section = element.href.split("=")[1];
        return
    }
});

if (!section) {
    location.href = location.href + '?sec=drop';
}

async function getHistory() {
    const response = await sendRequest("/products/games/history/1/");

    if (!response.ok) {
        alert('Error with history')
        return
    }

    const result = await response.json();

    if (!result.length) {
        empty.style.display = 'flex';
    } else {
        table.style = "";
        let c = 0;

        result.forEach((element) => {
            c++;

            html = `
            <li>
                <span class="game-num">${c}</span>
                <span class="game-name">${gamesMapping[element.game]}</span>
            `;

            if (!element.related_item_first) {
                html += `
                    <span class="is-win true"></span>
                `
            } else if (!(element.related_item_second || element.related_case)) {
                html += `
                    <span class="item-img"><img src="${element.related_item_first.image_path}"></span>
                    <span class="is-win ${element.is_win}"></span>
                `
            } else if (element.related_item_second) {
                html += `
                    <span class="case-drop-items">
                        <span class="case-img"><img src="${element.related_item_first.image_path}"></span>
                        <span class="item-img"><img src="${element.related_item_second.image_path}"></span>
                    </span>
                    <span class="is-win ${element.is_win}"></span>
                `
            } else if (element.related_case) {
                html += `
                    <span class="case-drop-items">
                        <span class="case-img"><img src="${element.related_case.image_path}"></span>
                        <span class="item-img"><img src="${element.related_item_first.image_path}"></span>
                    </span>
                    <span class="is-win ${element.is_win}"></span>
                `
            }

            table.innerHTML += `${html}</li>`;
        });
    }
}

function renderItems(result) {
    let c = 0;

    result.forEach((element) => {
        c += 1;

        table.innerHTML += `
            <article class="dropped mono" style="width: calc(100vw * calc(196 / var(--reference-display-w)));" id="${element.id}">
                <div class="w-line"></div>
                <div class="dropped-content">
                    <span style="margin-left: .5vw;font-size: small;margin-right: 0.5ch;">${element.related_item_first.title}</span>
                    <span style="margin-left: .5vw;" class="item-price rose"><span>${element.related_item_first.price}</span> <img style="left: 0px;" src="/core/static/img/gear.png"></span>
                    <img style="width: 81%;position: relative;left: 2%;margin-top: 4%;" src="${element.related_item_first.image_path}" style="left: 0%;">
                </div>
            </article>
        `;
    });

    table.style = "";
    table.style.display = "grid";
}

function renderBattles(result) {
    let c = 0;

    result.forEach((element) => {
        c += 1;

        table.innerHTML += `
            <article class="battle-result" id="${element.id}">
                <div class="item-left">
                    <img src="${element.related_item_first.image_path}" class="item-battle-img">
                    <span class="extra-info"><img src="/core/static/img/account-avatar.png" class="avatar"><span class="price">${element.related_item_first.price}</span></span>
                </div>
                <img src="${element.related_case.image_path}" class="case-img">
                <div class="item-left">
                    <img src="${element.related_item_second.image_path}" class="item-battle-img">
                    <span class="extra-info"><img src="/core/static/img/account-avatar.png" class="avatar"><span class="price">${element.related_item_second.price}</span></span>
                </div>
            </article>
        `;
    });

    table.style = "";
    table.style.display = "grid";
}


function renderContracts(result) {
    let c = 0;

    result.forEach((element) => {
        c += 1;

        table.innerHTML += `
            <article class="contract-result" id="${element.id}">
                <div class="contract-amount">
                    ${element.related_item_first.price} <img src="/core/static/img/scrap.png" style="width: 3.5ch;">
                </div>
                <div class="contract-info">
                    <span class="contract-result-price">${element.related_item_first.title}</span>
                    <img src="${element.related_item_first.image_path}" style="    height: 110%;margin-top: 12%;margin-left: 0%;" class="contract-result-item">
                </div>
            </article>
        `;
    });

    table.style = "";
    table.style.display = "grid";
}

async function getItems() {
    let _requestSection;

    if (section == "drop") {
        _requestSection = "D"
    } else if (section == "contract") {
        _requestSection = "C"
    } else if (section == "battles") {
        _requestSection = "B"
    } else if (section == "bonuse") {
        _requestSection = "S"
    }

    const requestOptions = {
      method: "GET",
    };

    const response = await sendRequest(
        `http://${location.hostname}/products/games/history/${_requestSection}/`,
        requestOptions
    );

    const result = await response.json();

    if (!result.length) {
        document.getElementById('footer-w').style.marginTop = 'calc(100vw * calc(311 / var(--reference-display-w)))';
        return
    }

    if (_requestSection == "D") {
        renderItems(result)
    } else if (_requestSection == "B") {
        renderBattles(result)
    } else if (_requestSection == "C") {
        renderContracts(result)
    }
}

getItems();
