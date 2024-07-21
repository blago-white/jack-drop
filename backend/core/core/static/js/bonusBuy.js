import { renderItemPrize } from "./prize.js";


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
        location.href = "/";
        return
    }

    const result = await response.json();

    const percent = Math.min(Math.ceil((result.points / result.level.target) * 100), 100);

    document.getElementById('level-digit').innerHTML = result.level.level;
    document.getElementById('level-desc').innerHTML = `Оборот ${result.level.target} металлалома, что бы получить Рудный кейс Дерево`;
    document.getElementById('upgrade-percent').innerHTML = `${percent}%`;
    document.getElementById('next-lvl-desc').innerHTML = `Перейти к ${result.level.level+1} уровню`;

    if (percent < 100) {
        document.getElementById('next-level-btn').classList.add('disabled');
        document.getElementById('get-prize-btn').classList.add('disabled');
    } else {
        canUpgradeLevel = true;
        document.getElementById('next-level-btn').onclick = () => {
            nextLevel()
        };

        if (!result.withdraw_current) {
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

    renderItemPrize(result.title, result.price, result.image_path, "Receive!")

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
