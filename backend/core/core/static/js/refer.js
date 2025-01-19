const user = await getAuthenticated();

async function renderInfo() {
    const response = await sendRequest('https://{location.hostname}/auth/referrals/api/v1/public/status/');

    if (!response.ok) {
        alert("Ошибка с получением данных реф. статуса, обратитесь в поддержку!")
        return;
    }

    const result = await response.json();

    document.getElementById('referName').innerHTML = user.username;
    document.getElementById('countActivations').innetHTML = 'чуть позже:)';
    document.getElementById('depositsTotalAmount').innetHTML = result.total_deposits;
    document.getElementById('depositsProfit').innetHTML = result.profit;
    document.getElementById('refLink').innetHTML = result.reflink;
}

if (!user || (user && (!user.is_blogger))) {
    location.href = '/auth/';
}

renderInfo()
