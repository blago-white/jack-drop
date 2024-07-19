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
        alert("Error");
        location.href = "/";
        return
    }

    const result = await response.json();

    const percent = Math.min(Math.ceil((result.points / result.target) * 100), 100);

    document.getElementById('level-digit').innerHTML = result.level;
    document.getElementById('level-desc').innerHTML = `Оборот ${result.target} металлалома, что бы получить Рудный кейс Дерево`;
    document.getElementById('upgrade-percent').innerHTML = `${percent}%`;
    document.getElementById('next-lvl-desc').innerHTML = `Перейти к ${result.level+1} уровню`;

    if (percent < 100) {
        document.getElementById('next-level-btn').classList.add('disabled');
        document.getElementById('get-prize-btn').classList.add('disabled');
    } else {
        canUpgradeLevel = true;
        document.getElementById('next-level-btn').onclick = () => {
            nextLevel()
        };
    }
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
