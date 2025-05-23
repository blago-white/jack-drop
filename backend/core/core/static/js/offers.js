function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const zeroPad = (num, places) => String(num).padStart(places, '0')

async function countDown(small=false) {
    let time;

    while (true) {
        await sleep(1000);

        time = ((60*60*24) - ((Date.now()/1000) - parseInt(getCookie("has-offer-promo-created-at"))));

        if (time < 0) {
            setCookie("viewed-offer", undefined);
            setCookie("offer-hidden", undefined)

            try {await closeOffer()} catch(error) {}
            try {await closeOffer(small=True)} catch(error) {}
            return;
        }

        const sec = parseInt(time%60);

        if (!small) {
            document.getElementById('timerValue').innerHTML = `${zeroPad(parseInt(time / 60 / 60), 2)}:${zeroPad(parseInt((time % (60*60)) / 60), 2)}:${zeroPad(parseInt(time%60), 2)}`
        }

        document.getElementById('timerRing').style.background = `radial-gradient(closest-side, rgb(32, 32, 32) 79%, transparent 80%, transparent 100%), conic-gradient(rgb(255, 255, 255) ${sec / 60 * 100}%, rgba(255, 255, 255, 0.2) 0deg)`;
    }
}

async function renderFullScreenDepositWindow(promocode, discount) {
    const time = ((60*60*24) - ((Date.now()/1000) - parseInt(getCookie("has-offer-promo-created-at"))));

    if (time < 0) {
        return await closeOffer(promocode, discount, block=true);
    }

    const sec = parseInt(time%60);

    document.getElementById('prize-wrappper').innerHTML = `
        <div class="offer-window" id="offerWindow">
            <div class="offer-content">
                <div class="offer-header">
                    <h2 class="offer-content-title">Эксклюзивный промокод от JackDrop!</h2>
                    <button class="offer-cross" onclick="closeOffer('${promocode}', '${discount}')"></span>
                </div>
                <div class="timer">
                    <div class="timer-ring" id="timerRing"></div>
                    <div class="timer-data">
                        <span style="font-size: .9em;">осталось:</span>
                        <span style="font-size: 1.4em;font-family: 'Gilroy SemiBold';" id="timerValue">24:00:00</span>
                    </div>
                </div>
                <span style="max-width: 62%;text-transform: none;color: #eee;">
                    До конца дня используй код <b style="background: #0047FF;padding: .3ch;border-radius: 0.5ch;">${promocode}</b> и получи +${discount}% к своему первому депозиту!
                </span>
                <button class="super-button offer-button" onclick="location.href = '/replenish/${promocode}/'">
                    <span class="super-button-bg"></span>
                    <span class="super-button-text">ПОПОЛНИТЬ С БОНУСОМ!</span>
                </button>
            </div>
        </div>
    `;

    document.getElementById('timerRing').style.background = `radial-gradient(closest-side, #202020 79%, transparent 80% 100%), conic-gradient(#ffffff ${sec / 60 * 100}%, rgb(255, 255, 255, .2) 0)`

    document.getElementById('prize-wrappper').style = "background: #1A1A1AB2;display: flex;visibility: visible;"

    await countDown();
}


async function closeOffer(promocode, discount, small=false, block=false) {
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

    if (!small) {
        await renderSmallDepositWindow(promocode, discount);
    }
}

async function renderSmallDepositWindow(promocode, discount) {
    const time = ((60*60*24) - ((Date.now()/1000) - parseInt(getCookie("has-offer-promo-created-at"))));

    if (time < 0) {
        return await closeOffer(promocode, discount, block=true);
    }

    const sec = parseInt(time%60);

    document.getElementById('smallDepositWindow').innerHTML = `
        <button class="small-close-cross" onclick="closeOffer('${promocode}', '${discount}', true, true);"></button>
        <img src="https://s.iimg.su/s/28/oToA9ygk2Htnv3mmSRgvIWNylrhlvZgQaCkInOhE.png" onclick="location.href = '/replenish/${promocode}/'" class="small-banner-img">
        <span class="small-offer-content" onclick="location.href = '/replenish/${promocode}/'" style="display: flex;align-items: center;" id="smallOfferContent">
        <div class="timer" style="height: 2.5ch;padding: 0px;background: transparent;justify-content: center;">
            <div class="timer-ring" id="timerRing" style="height: 100%;background: radial-gradient(closest-side, #202020 79%, transparent 80% 100%), conic-gradient(#ffffff ${sec / 60 * 100}%, rgb(255, 255, 255, .2) 0);"></div>
        </div>
        +${discount}% К депозиту
        </span>
    `;

    document.getElementById('smallDepositWindow').style = "";

    await countDown(true);
}

async function renderWindow() {
    if (getCookie("offer-hidden")) {
        return
    }

    if (getCookie("has-offer") == 'true') {
        if (getCookie("viewed-offer")) {
            await renderSmallDepositWindow(getCookie("has-offer-promo-name"), getCookie("has-offer-promo-discount"))
        } else {
            setCookie("viewed-offer", true)
            await renderFullScreenDepositWindow(getCookie("has-offer-promo-name"), getCookie("has-offer-promo-discount"));
        }
    }
}

async function checkOffer() {
    if (getCookie("offer-checked-date") && ((Date.now() - parseInt(getCookie("offer-checked-date"))) < 60*10) && getCookie("has-offer-promo-created-at") && ((Date.now()/1000) - getCookie("has-offer-promo-created-at") <= 60*60*24)) {
        await renderWindow();
    }

    if (getCookie("offer-hidden")) {return}

    const response = await sendRequest(
        "/auth/discount/api/v1/public/get-offer/",
        {method: "GET", headers: new Headers()}
    );

    const result = await response.json();

    if (result.available) {
        setCookie("has-offer", true)
        setCookie("has-offer-promo-name", result.promocode.code)
        setCookie("has-offer-promo-discount", result.promocode.discount)
        setCookie("has-offer-promo-created-at", result.date_received)
    } else {
        setCookie("has-offer", false)
    }

    setCookie("offer-checked-date", Date.now());

    await renderWindow();
}

window.renderFullScreenDepositWindow = renderFullScreenDepositWindow;

if (!location.href.includes("replenish")) {
    checkOffer();
}
