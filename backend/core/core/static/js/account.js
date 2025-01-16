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

async function renderReferralStatus() {
    const response = await sendRequest("/auth/referrals/api/v1/public/status/", {method: "GET"});

    if (!response.ok) {
        return
    }

    const result = await response.json();

    const isMobile = ((screen.width / screen.height) < 1/1);

    const additionalStyle = isMobile ? 'position: relative;top: -87%;margin-top: 1em;right: -52%;max-width: max-content;font-size: 1em;text-align: right;' : ''

    document.getElementsByClassName('account-empty')[0].innerHTML += `
        <span style="display: block;margin-top: 1ch;${additionalStyle}"><b style=${isMobile ? "font-size: 1.45ch" : "font-size: calc(100vw * calc(22 / 1920))"}>Статус реферальной системы -</b><span style="
            font-size: 1.45ch;
            color: rgb(240, 240, 240);
        "><br>Реффералов: ${result.count_referrals}<br>Получено: ${result.profit}</span></span>
    `
}

async function renderInfo() {
    const response = await getAuthenticated();

    document.getElementById('usr-name').innerHTML = `${response.username}<span class="account-id-val">ID ${response.id}</span>`;
    document.getElementById('balance').innerHTML = `${Math.floor(response.balance)}`;
    document.getElementById('trade-link').value = response.trade_link;


    renderReferralStatus()
}


renderBonusBuy();
renderInfo();