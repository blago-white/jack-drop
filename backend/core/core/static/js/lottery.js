let lottery;

function renderLotteryInfo(renderMainPrize) {
    document.getElementById("prize-wrappper").innerHTML = `
    <div class="lottery-expand-info" style="transform: scale(0);" id="lotteryExpanded">
        <h3 class="lottery-expand-header">РАЗДАЧА<br>СКИНОВ
            <button class="lottery-expand-close-btn offer-cross" onclick="return reduceLotteryInfo();"></button>
        </h3>
        <div class="lottery-prize-info lotterty-info-row">
            <img src="https://cdn.rust.tm/item/AK+Royale/300.png" class="lottery-prize-img">
            <span class="lottery-prize-name">StatTrak™ MAC-10 | Neon Rider</span>
        </div>
        <div class="lottery-requirement lotterty-info-row">
            <span>Пополните свой баланс от 30 000₽<br>Ваш баланс: 0₽</span>
            <button class="lottery-requirement-replenish-btn">ПОПОЛНИТЬ</button>
        </div>
        <div class="lottery-stats lotterty-info-row">
            <div class="timer lottery-timer" style="">
            <div class="timer-ring lottery-expand-ring" id="lotteryExpandTimerRing"></div>
                <div class="timer-data">
                    <span style="font-size: .9em;">осталось:</span>
                    <span style="font-size: 1.4em;font-family: 'Gilroy SemiBold';" id="lotteryExpandTimerValue">24:00:00</span>
                </div>
            </div>
            <span class="lottery-expand-partipicant-count">УЧАСТНИКОВ: 24</span>
        </div>
        <button class="lottery-make-part-btn lotterty-info-row">УЧАСТВОВАТЬ</button>
    </div>
    `;

    document.getElementById("prize-wrappper").style = "transition: all .2s ease;";

    document.getElementById("prize-wrappper").style.visibility = "visible";
    document.getElementById("prize-wrappper").style.display = "flex";
    document.getElementById("prize-wrappper").style.backgroundColor = "rgb(20, 20, 20, .9)";

    setTimeout(() => {
        document.getElementById("lotteryExpanded").style = "";
    }, 200);
}

function reduceLotteryInfo() {
    document.getElementById("lotteryExpanded").style = "";
    document.getElementById("prize-wrappper").style.backgroundColor = "rgb(20, 20, 20, .9)";

    setTimeout(() => {
        document.getElementById("prize-wrappper").innerHTML = "";
        document.getElementById("prize-wrappper").style.visibility = "hidden";
        document.getElementById("prize-wrappper").style.display = "none";
    }, 200);
}

async function countDown(small=false) {
    let time;

    while (true) {
        await sleep(1000);

        time = ((60*60*24) - ((Date.now()/1000) - parseInt(getCookie("lottery-started-at"))));

        if (time < 0) {
            try {document.getElementById("lotteryBanner").remove()} catch(error) {}
            try {reduceLotteryInfo()} catch(error) {}
            return;
        }

        const sec = parseInt(time%60);

        document.getElementById('lotteryTimerValue').innerHTML = `${zeroPad(parseInt(time / 60 / 60), 2)}:${zeroPad(parseInt((time % (60*60)) / 60), 2)}:${zeroPad(parseInt(time%60), 2)}`
        document.getElementById('lotteryTimerRing').style.background = `radial-gradient(closest-side, rgb(255 0 122) 79%, transparent 80%, transparent 100%), conic-gradient(rgb(255, 255, 255) ${sec / 60 * 100}%, rgba(255, 255, 255, 0.2) 0deg)`;

        try {
            document.getElementById('lotteryExpandTimerValue').innerHTML = `${zeroPad(parseInt(time / 60 / 60), 2)}:${zeroPad(parseInt((time % (60*60)) / 60), 2)}:${zeroPad(parseInt(time%60), 2)}`
            document.getElementById('lotteryExpandTimerRing').style.background = `radial-gradient(closest-side, rgb(255 0 122) 79%, transparent 80%, transparent 100%), conic-gradient(rgb(255, 255, 255) ${sec / 60 * 100}%, rgba(255, 255, 255, 0.2) 0deg)`;
        } catch {}
    }
}

async function renderData(lottery_) {
    if (!lottery_) {
        return
    }

    if ((Date.now() - (lottery_.created_at + lottery_.start_after)) >= 0) {
        document.getElementById("first-gun-name").innerHTML = lottery_.prize_main.title;
        document.getElementById("second-gun-name").innerHTML = lottery_.prize_secondary.title;

        document.getElementById("first-gun-img").innerHTML = lottery_.prize_main.image_path;
        document.getElementById("secondary-gun-img").innerHTML = lottery_.prize_secondary.image_path;

        document.getElementById("lotteryBanner").style.display = 'flex';

        await countDown();
    }
}

async function getCurrentLottery() {
    const response = await sendRequest(
        "/products/lottery/current/",
        {method: "GET"}
    );

    if (!response.ok) {
        return
    }

    const result = await response.json();

    if (!result.is_active || ((Date.now() - (result.created_at + result.start_after + result.duration)) < 0)) {
        setCookie("lottery-inactive", true);
        return
    }

    setCookie("lottery-inactive", false);

    setCookie("lottery-started-at", result.created_at + result.start_after);
    setCookie("lottery-ended-at", result.created_at + result.start_after + result.duration);

    lottery = result;

    return result;
}

async function main() {
    const user = await getAuthenticated();

    if (!user || (user.id != 57)) {} else {
        await renderData(await getCurrentLottery());
    }
}

window.renderLotteryInfo = renderLotteryInfo;
window.reduceLotteryInfo = reduceLotteryInfo;

main();
