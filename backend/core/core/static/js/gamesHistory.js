const table = document.getElementById('game-history-table');
const empty = document.getElementById('empty-hist');

const gamesMapping = {
    "U": "Upgrade",
    "C": "Contract",
    "B": "Battle",
    "M": "Mines"
};

const bonuseMapping = {
    "CD": "CASE",
    "US": "UPGRADE",
    "CS": "CONTRACT",
    "FR": "FREE",
    "FC": "FREE CASE",
    "PR": "PROMO"
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
        makeWarn('Error with history')
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
    let items = "";

    result.forEach((element) => {
        c += 1;

        items += `
                <article class="item-card" style="background: url(/core/static/img/card-bg-yellow.png);background-size:cover;cursor: pointer;width: calc(100vw * calc(196 / var(--reference-display-w)));" onclick="selectItem(${element.id})" id=${element.id}>
                    <div class="dropped-content">
                        <div class="item-numeric-info">
                            <span class="item-price yellow"><span>${element.related_item_first.price}</span> <img src="/core/static/img/gear.png"></span>
                        </div>

                        <div style="display: grid;grid-template-rows: 1fr;grid-template-columns: 1fr;width: 100%;max-width: 100%;justify-items: center;align-items: center;">
                            <img src="/core/static/img/card-jd-logo.png" style="grid-row: 1;grid-column: 1;width: 100%;">
                            <img src="${element.related_item_first.image_path}" class="item-card-img" style="width: 100%;grid-row: 1;grid-column: 1;">
                        </div>

                        <span class="item-title">${element.related_item_first.title}</span>
                    </div>
                </article>
        `;
    });

    table.innerHTML = items;
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
                    <img src="${element.related_item_first.image_path}" style="height: 110%;margin-top: 12%;margin-left: 0%;" class="contract-result-item">
                </div>
            </article>
        `;
    });

    table.style = "";
    table.style.display = "grid";
}

function renderBonuses(result) {
    let c = 0;
    let path = "";

    result.forEach((element) => {
        c += 1;

    let style1 = "margin-right: -10%;width: 54%;height: auto;";
    let style2 = "margin-right: -10%;width: 54%;height: auto;";

    let style;

    if (element.bonus_type == "CD") {
            style = style1;
    } else {
            style = style2;
    }

        if (element.bonus_type == "US") {
            path = "http://s.iimg.su/s/25/hNQxLOAWR6M9X1SaGB5qpxXDEExmbgA4l7Zaq49B.png"
        } else if (element.bonus_type == "CD") {
            path = "http://s.iimg.su/s/25/khzavJhECphtVsVQLOu31xQefiTejDHJhIrb4BEw.png"
        } else {
            path = "http://s.iimg.su/s/25/X5s3CLf5s7VCngiq6PKVUeO2rqUJR0YZ3S7Pi0zE.png"
        }

        table.innerHTML += `
                <article class="bonuse_" id="${c}">
                    <span class="bonuse-title" style="    margin-left: 10%;
    font-size: 2.3em;
    font-family: 'Gilroy Regular';">
                        ${element.item_title || element.case_title}<span style="color: rgb(200, 200, 200)">.${bonuseMapping[element.bonus_type]}</span>
                    </span>
                    <img style="${style}" src="${path}">
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
    } else {
        _requestSection = "D"
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
        document.getElementById('game-history-table').style = "display: flex;align-items: center;font-size: 1.17em;";
        document.getElementById('game-history-table').innerHTML = "<div>Ничего не найдено</div><div>Nothing found.</div>";

        document.getElementById('footer-w').style.marginTop = 'calc(100vw * calc(311 / var(--reference-display-w)))';
        return
    }

    if (_requestSection == "D") {
        renderItems(result)
    } else if (_requestSection == "B") {
        renderBattles(result)
    } else if (_requestSection == "C") {
        renderContracts(result)
    } else if (_requestSection == "S") {
        renderBonuses(result)
    }
}

getItems();
