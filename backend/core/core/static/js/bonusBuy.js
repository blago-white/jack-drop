import { printPrizeItem } from "./animations.js";

let canUpgradeLevel = false;


function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
};

async function getStatus() {
    const response = await sendRequest("/products/bonus-buy/info/", {method: "GET"});

    if (!response.ok) {
        document.getElementById('next-level-btn').innerHTML = "Зайдите через Steam";
        document.getElementById('get-prize-btn').innerHTML = "Можно получить бесплатный кейс";

        if (screen.width / screen.height < 1/1) {
            document.getElementById('next-level-btn').style = "font-size: 3em;";
            document.getElementById('get-prize-btn').style = "font-size: 3em;";
        }

        return
    }

    const result = await response.json();

    const percent = Math.min(Math.ceil((result.points / result.level.target) * 100), 100);

    document.getElementById('level-digit').innerHTML = result.level.level;

    if (getCookie('lang') == 'ru') {
        document.getElementById('level-desc').innerHTML = `
            Оборот ${result.level.target} металлалома, что бы получить кейс "${result.level.free_case.title}"
        `;
        document.getElementById('next-lvl-desc').innerHTML = `Перейти к ${result.level.level+1} уровню`;
    } else {
        document.getElementById('level-desc').innerHTML = `
            Turnover ${result.level.target} of scrap, to receive case "${result.level.free_case.title}"
        `;
        document.getElementById('next-lvl-desc').innerHTML = `Go to ${result.level.level+1} level`;
    }

    document.getElementById('upgrade-percent').innerHTML = `${percent}%`;
    document.getElementById('benefit-case').src = result.level.free_case.image_path;


    if (percent < 100) {
        document.getElementById('next-level-btn').classList.add('disabled');
        document.getElementById('get-prize-btn').classList.add('disabled');
    } else {
        canUpgradeLevel = true;
        document.getElementById('next-level-btn').onclick = () => {
            nextLevel()
        };

        if (result.can_withdraw_case) {
            document.getElementById('get-prize-btn').onclick = () => {
                getCase()
            }
        } else {
            document.getElementById('get-prize-btn').classList.add('disabled');
        }
    }
}

async function getCase() {
    const headers = new Headers();

    headers.append("X-CSRFToken", getCookie("csrftoken"));

    const response = await sendRequest("/products/bonus-buy/get-case/", {method: "POST", headers: headers});

    if (!response.ok) {
        location.reload();

        return
    }

    const result = await response.json();

    printPrizeItem(result.image_path, result.price, result.title)

    return {};
}

async function nextLevel() {
    if (!canUpgradeLevel) {
        return
    }

    const headers = new Headers();

    headers.append("X-CSRFToken", getCookie("csrftoken"));

    const response = await sendRequest("/products/bonus-buy/next/", {method: "POST", headers: headers});

    location.reload();
}

getStatus();
