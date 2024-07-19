async function renderBonusBuy() {
    const response = await sendRequest("/products/bonus-buy/info/", {method: "GET"});

    if (!response.ok) {
        alert("Error");
        location.href = "/";
        return
    }

    const result = await response.json();

    const percent = (result.points / result.target) * 100;

    document.getElementById("bonus").innerHTML = `${result.points}/${result.target}  XP`
    document.getElementById("diagram").style.width = `${(result.points/result.target) * 100}%`
}

async function renderInfo() {
    const response = await sendRequestJson("/auth/api/v1/public/user/", {mehtod: "GET", headers: new Headers()})

    console.log(response);

    document.getElementById('usr-name').innerHTML = `${response.username}<span class="account-id-val">ID ${response.id}</span>`;
    document.getElementById('balance').innerHTML = `${response.balance}`;
}

//async function getStatus() {
//    document.getElementById('level-digit').innerHTML = result.level;
//    document.getElementById('level-desc').innerHTML = `Оборот ${result.target} металлалома, что бы получить Рудный кейс Дерево`;
//    document.getElementById('upgrade-percent').innerHTML = `${percent}%`;
//    document.getElementById('next-lvl-desc').innerHTML = `Перейти к ${result.level+1} уровню`;
//}

//getStatus();

renderBonusBuy();
renderInfo();
