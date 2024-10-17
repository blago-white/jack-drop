async function renderBonusBuy() {
    const response = await sendRequest("/products/bonus-buy/info/", {method: "GET"});

    if (!response.ok) {return}

    const result = await response.json();

    const percent = (result.points / result.level.target) * 100;

    document.getElementById("bonus").innerHTML = `${result.points}/${result.level.target}  XP`
    document.getElementById("diagram").style.width = `${Math.min((result.points/result.level.target) * 100, 100)}%`
}

async function updateUserTradeLink() {
    const headers = new Headers();

    headers.append("Content-Type", "application/json");

    const link = document.getElementById('trade-link').value;
    const response = await sendRequestJson("/auth/api/v1/public/add-trade/", {method: "POST", headers: headers, body: JSON.stringify({"trade_link": link})})
    if (response.ok) {
        document.getElementById('trade-link').style.color = 'green';
    }
}

async function renderInfo() {
    const response = await sendRequestJson("/auth/api/v1/public/user/", {mehtod: "GET", headers: new Headers()})

    document.getElementById('usr-name').innerHTML = `${response.username}<span class="account-id-val">ID ${response.id}</span>`;
    document.getElementById('balance').innerHTML = `${Math.floor(response.balance)}`;
    document.getElementById('trade-link').value = response.trade_link;
}

renderBonusBuy();
renderInfo();