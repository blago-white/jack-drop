async function renderBonusBuy() {
    const response = await sendRequest("/products/bonus-buy/info/", {method: "GET"});

    if (!response.ok) {
        return
    }

    const result = await response.json();

    const percent = (result.points / result.level.target) * 100;

    document.getElementById("bonus").innerHTML = `${result.points}/${result.level.target}  XP`
    document.getElementById("diagram").style.width = `${Math.min((result.points/result.level.target) * 100, 100)}%`
}

async function renderInfo() {
    const response = await sendRequestJson("/auth/api/v1/public/user/", {mehtod: "GET", headers: new Headers()})

    document.getElementById('usr-name').innerHTML = `${response.username}<span class="account-id-val">ID ${response.id}</span>`;
    document.getElementById('balance').innerHTML = `${Math.floor(response.balance)}`;
}

renderBonusBuy();
renderInfo();
