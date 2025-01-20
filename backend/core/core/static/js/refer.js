const user = await getAuthenticated();

function copyRefLink() {
    window.prompt("Copy to clipboard: Ctrl+C, Enter", document.getElementById('refLink').innerHTML);
}

async function renderInfo() {
    const response = await sendRequest(
        `https://${location.hostname}/auth/referrals/api/v1/public/status/`,
        {method: "GET"}
    );

    if (!response.ok) {
        alert("Ошибка с получением данных реф. статуса, обратитесь в поддержку!")
        return;
    }

    const result = await response.json();

    document.getElementById('referName').innerHTML = user.username;
    document.getElementById('countActivations').innerHTML = 'чуть позже:)';
    document.getElementById('depositsTotalAmount').innerHTML = result.total_deposits;
    document.getElementById('depositsProfit').innerHTML = result.profit;
    document.getElementById('refLink').innerHTML = result.reflink;
    document.getElementById('canWithdrawProfit').innerHTML = result.profit;
    document.getElementById('referAvatar').innerHTML = user.avatar;
}

if (!user || (user && (!user.is_blogger))) {
    location.href = '/auth/';
}

renderInfo()

window.copyRefLink = copyRefLink;
