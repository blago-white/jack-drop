function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function renderFullScreenDepositWindow(promocode, discount) {
    document.getElementById('prize-wrappper').innerHTML = `
        <div class="offer-window" id="offerWindow">
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
                    До конца дня используй код ${promocode} и получи +${discount}% к своему первому депозиту!
                </span>
                <button class="super-button offer-button" onclick="location.href = '/replenish/${promocode}/'">
                    <span class="super-button-bg"></span>
                    <span class="super-button-text">ПОПОЛНИТЬ С БОНУСОМ!</span>
                </button>
            </div>
        </div>
    `

    document.getElementById('prize-wrappper').style = "background: #1A1A1AB2;display: flex;visibility: visible;"
}


async function closeOffer(small=false, block=false) {
    alert(`${small}, ${block}`)

    if (small) {
        document.getElementById('smallOfferContent').style.transform = "scale(0)";
        await sleep(200);
        document.getElementById('smallDepositWindow').style.transform = "scale(0)";
    } else {
        document.getElementById('prize-wrappper').style.transition = "all .2s ease";
        document.getElementById('offerWindow').style.transform = "scale(0)";
        document.getElementById('prize-wrappper').style.background = "transparent";
    }

    if (block) {
        setCookie("offer-hidden", true)
    }

    document.getElementById('prize-wrappper').style = "";
    document.getElementById('prize-wrappper').innerHTML = "";
}

async function renderSmallDepositWindow(promocode) {
    await sleep(2000);

    document.getElementsByTagName('body')[0].innerHTML += `
    <aside class="small-deposit-window" id="smallDepositWindow">
        <button class="small-close-cross" onclick="closeOffer(true, true);"></button>
        <img src="https://s.iimg.su/s/28/oToA9ygk2Htnv3mmSRgvIWNylrhlvZgQaCkInOhE.png" onclick="location.href = '/replenish/${promocode}/'" class="small-banner-img">
        <span class="small-offer-content" onclick="location.href = '/replenish/${promocode}/'" id="smallOfferContent">+25% К депозиту</span>
    </aside>
    `;
}

async function renderWindow() {
    if (getCookie("offer-hidden")) {
        return
    }

    if (getCookie("has-offer")) {
        if (getCookie("viewed-offer")) {
            await renderSmallDepositWindow(getCookie("has-offer-promo-name"))
        } else {
            renderFullScreenDepositWindow(getCookie("has-offer-promo-name"), getCookie("has-offer-promo-discount"));
            setCookie("viewed-offer", true)
        }
    }
}

async function checkOffer() {
    if ((parseInt(new Date()) - getCookie("offer-checked-date")) < 60*15) {
        return await renderWindow();
    }

    if ((await getAuthenticated()).balance != 0 || getCookie("offer-hidden")) {return}

    const response = await sendRequest(
        "/auth/discount/api/v1/public/get-offer/",
        {method: "GET", headers: new Headers()}
    );

    const result = await response.json();

    if (result.available) {
        setCookie("has-offer", true)
        setCookie("has-offer-promo-name", result.promocode.code)
        setCookie("has-offer-promo-discount", result.promocode.discount)
        setCookie("has-offer-promo-created-at", result.promocode.date_received)
    } else {
        setCookie("has-offer", false)
    }

    setCookie("offer-checked-date", parseInt(new Date()));

    await renderWindow();
}

window.renderFullScreenDepositWindow = renderFullScreenDepositWindow;

if (!location.href.includes("replenish")) {
    checkOffer();
}
