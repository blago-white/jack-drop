const user = await getAuthenticated();

async function copyRefLink() {
    try {
        await navigator.clipboard.writeText(document.getElementById('refLink').innerHTML)
    } catch {}
}

async function renderInfo() {
    if ((screen.width / screen.height) < 1/1) {
        document.getElementsByClassName('main-content')[0].style = 'font-size: 6em;text-align: center;font-family: "Gilroy Bold";';
        document.getElementsByClassName('main-content')[0].innerHTML = 'Зайдите с пк, планшета, или переверните телефон перед заходом в профиль';
        return;
    }

    const response = await sendRequest(
        `https://${location.hostname}/auth/referrals/api/v1/public/status/`,
        {method: "GET"}
    );

    if (!response.ok) {
        makeWarn("Ошибка с получением данных реф. статуса, обратитесь в поддержку!")
        return;
    }

    const result = await response.json();

    document.getElementById('referName').innerHTML = user.username;
    document.getElementById('countActivations').innerHTML = result.count_promocodes_activations;
    document.getElementById('depositsTotalAmount').innerHTML = result.total_deposits;
    document.getElementById('depositsProfit').innerHTML = result.profit;
    document.getElementById('refLink').innerHTML = result.reflink;
    document.getElementById('canWithdrawProfit').innerHTML = result.profit;
    document.getElementById('referAvatar').src = user.avatar;
}

if (!user || (user && (!user.is_blogger))) {
    location.href = '/auth/';
}

renderInfo()

window.copyRefLink = copyRefLink;
