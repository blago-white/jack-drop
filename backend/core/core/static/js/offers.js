function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function countDown() {
    let time;

    while (true) {
        await sleep(1000);

        time = ((60*60*24) - ((Date.now()/1000) - parseInt(getCookie("has-offer-promo-created-at"))));

        document.getElementById('timerValue').innerHTML = `${parseInt(time / 60 / 60)}:${parseInt((time % (60*60)) / 60)}:${parseInt(time%60)}`
    }
}

async function renderFullScreenDepositWindow(promocode, discount) {
    document.getElementById('prize-wrappper').innerHTML = `
        <div class="offer-window" id="offerWindow">
            <div class="offer-content">
                <div class="offer-header">
                    <h2 class="offer-content-title">Эксклюзивный промокод от JackDrop!</h2>
                    <button class="offer-cross" onclick="closeOffer()"></span>
                </div>
                <div class="timer">
                    <div class="timer-ring" id="timerRing"></div>
                    <div class="timer-data">
                        <span style="font-size: .9em;">осталось:</span>
                        <span style="font-size: 1.4em;font-family: 'Gilroy SemiBold';" id="timerValue">24:00:00</span>
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
    `;

    document.getElementById('timerRing').style.background = `radial-gradient(closest-side, #202020 79%, transparent 80% 100%), conic-gradient(#ffffff 75%, rgb(255, 255, 255, .2) 0)`

    document.getElementById('prize-wrappper').style = "background: #1A1A1AB2;display: flex;visibility: visible;"

    await countDown();
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

async function renderSmallDepositWindow(promocode, discount) {
    document.getElementById('smallDepositWindow').innerHTML += `
        <button class="small-close-cross" onclick="closeOffer(true, true);"></button>
        <img src="https://s.iimg.su/s/28/oToA9ygk2Htnv3mmSRgvIWNylrhlvZgQaCkInOhE.png" onclick="location.href = '/replenish/${promocode}/'" class="small-banner-img">
        <span class="small-offer-content" onclick="location.href = '/replenish/${promocode}/'" id="smallOfferContent">+${discount}% К депозиту</span>
    `;

    document.getElementById('smallDepositWindow').style = "";
}

async function renderWindow() {
    if (getCookie("offer-hidden")) {
        console.log(10);
        return
    }

    if (getCookie("has-offer")) {
        console.log(11);
        if (getCookie("viewed-offer")) {
            console.log(12);

            await renderSmallDepositWindow(getCookie("has-offer-promo-name"), getCookie("has-offer-promo-discount"))
        } else {
            console.log(13);

            await renderFullScreenDepositWindow(getCookie("has-offer-promo-name"), getCookie("has-offer-promo-discount"));
            setCookie("viewed-offer", true)
        }
    }
}

async function checkOffer() {
    if ((Date.now() - parseInt(getCookie("offer-checked-date"))) < 60*15) {
        console.log(1);
        await renderWindow();
    }

    if ((await getAuthenticated()).balance != 0 || getCookie("offer-hidden")) {return}

    console.log(2);

    const response = await sendRequest(
        "/auth/discount/api/v1/public/get-offer/",
        {method: "GET", headers: new Headers()}
    );

    const result = await response.json();

    if (result.available) {

        console.log(result);

        setCookie("has-offer", true)
        setCookie("has-offer-promo-name", result.promocode.code)
        setCookie("has-offer-promo-discount", result.promocode.discount)
        setCookie("has-offer-promo-created-at", result.date_received)
    } else {
        console.log(4);

        setCookie("has-offer", false)
    }

    setCookie("offer-checked-date", Date.now());

    console.log(5);

    await renderWindow();
}

window.renderFullScreenDepositWindow = renderFullScreenDepositWindow;

if (!location.href.includes("replenish")) {
    checkOffer();
}
