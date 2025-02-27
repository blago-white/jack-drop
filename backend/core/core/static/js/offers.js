function renderFullScreenDepositWindow() {
    document.getElementById('prize-wrappper').innerHTML = `
        <div style="/* width: 60%; */max-width: calc(95% - 2em);/* padding: 2em; */background: linear-gradient(90deg, rgb(13 13 13) 0%, rgba(20, 20, 20, 1) 100%);border-radius: 1em;font-size: 3em;display: grid;grid-template-columns: 1fr;grid-template-rows: 1fr;overflow: hidden;">

            <div class="" style="">
                <h2 style="font-family: 'Gilroy Bold';font-size: 3ch;max-width: 50%;text-align: left;margin: 0px;max-width: 60%;">Эксклюзивный промокод
от JackDrop!</h2>
                <div style="
    padding: 1em;
    gap: 1ch;
    display: flex;
    flex-direction: row;
    align-items: center;
    background: #202020;
    border-radius: calc(100vw * calc(10 / 1920));
    border-radius: calc(100vw * calc(30 / 1920))!important;
"><div class="timer-ring" style="
    background: radial-gradient(closest-side, #202020 79%, transparent 80% 100%), conic-gradient(#ffffff 75%, rgb(255, 255, 255, .2) 0);
    aspect-ratio: 1/1;
    position: relative;
    display: flex;
    height: 5ch;
    border-radius: 50%;
"></div><div class="timer-data" style="
    display: flex;
    flex-direction: column;
">
    <span style="
    font-size: .9em;
">осталось:</span>
    <span style="
    font-size: 1.4em;
    font-family: 'Gilroy SemiBold';
">03:16:54</span>
</div></div>
    <span style="
    max-width: 62%;
    text-transform: none;
    color: #eee;
">До конца дня используй код JD25 и получи +25% к своему первому депозиту!</span>
                <button class="super-button" onclick="clearWarn()" style="
    width: 50%;
    min-height: 4ch;
    font-size: 1.2em;
">
                    <span class="super-button-bg" style="
    transform: none;
"></span>
                    <span class="super-button-text">ПОПОЛНИТЬ С БОНУСОМ!</span>
                </button>
            </div>
        <div class="dep-img-container" style="
    grid-row: 1;
    grid-column: 1;
    width: inherit;
    height: auto;)%;)%;);
    padding-left: 36%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: flex-end;
    z-index: 1;
"><img src="https://s.iimg.su/s/27/MuLvJlbl7Fsub92WKMhkyrTmFuAeTKx500LylQDU.png" style="
    width: 100%;
    left: 22%;
    position: relative;
"></div></div>
    `
}

function renderSmallDepositWindow() {
    ...
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
