function renderFullScreenDepositWindow() {
    document.getElementById('prize-wrappper').innerHTML = `
        <div class="offer-window">
            <div class="offer-content">
                <div class="offer-header">
                    <h2 class="offer-content-title">Эксклюзивный промокод от JackDrop!</h2>
                    <button class="offer-cross" onclick="closeOffer()"></span>
                </div>
                <div class="timer">
                    <div class="timer-ring"></div>
                    <div class="timer-data">
                        <span style="font-size: .9em;">осталось:</span>
                        <span style="font-size: 1.4em;font-family: 'Gilroy SemiBold';">03:16:54</span>
                    </div>
                </div>
                <span style="max-width: 62%;text-transform: none;color: #eee;">
                    До конца дня используй код JD25 и получи +25% к своему первому депозиту!
                </span>
                <button class="super-button offer-button" onclick="closeOffer()">
                    <span class="super-button-bg"></span>
                    <span class="super-button-text">ПОПОЛНИТЬ С БОНУСОМ!</span>
                </button>
            </div>
        </div>
    `

    document.getElementById('prize-wrappper').style = "background: #1A1A1AB2;display: flex;visibility: visible;"
}

function closeOffer() {
    document.getElementById('prize-wrappper').style = "";
    document.getElementById('prize-wrappper').innerHTML = "";
}

function renderSmallDepositWindow() {
    document.getElementsByTagName('body')[0].innerHTML += `
    <aside class="small-deposit-window">
        <button class="small-close-cross"></button>
        <img src="https://s.iimg.su/s/28/oToA9ygk2Htnv3mmSRgvIWNylrhlvZgQaCkInOhE.png" class="small-banner-img">
        <span class="small-offer-content">+25% К депозиту</span>
    </aside>
    `;
}

function renderWindow() {
    if (getCookie("has-offer")) {
        if (getCookie("viewed-offer")) {
            renderSmallDepositWindow()
        } else {
            renderFullScreenDepositWindow();
            setCookie("viewed-offer", true)
        }
    }
}

//async function checkOffer() {
//    if ((parseInt(new Date()) - getCookie("offer-checked-date")) < 60*15) {
//        return renderWindow();
//    }
//
//    if ((await getAuthenticated()).balance != 0) {return}
//
//    const response = await sendRequest(
//        "/auth/discount/api/v1/public/get-offer/",
//        {method: "GET", headers: new Headers()}
//    );
//
//    const result = await response.json();
//
//    if (result.available) {
//        setCookie("has-offer", true)
//        setCookie("has-offer-promo-name", result.promocode.code)
//        setCookie("has-offer-promo-discount", result.promocode.discount)
//        setCookie("has-offer-promo-created-at", result.promocode.date_received)
//    } else {
//        setCookie("has-offer", false)
//    }
//
//    setCookie("offer-checked-date", parseInt(new Date()));
//
//    renderWindow();
//}

window.renderFullScreenDepositWindow = renderFullScreenDepositWindow;
