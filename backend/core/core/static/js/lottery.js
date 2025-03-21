import { printPrizeItem } from "./animations.js";

let lottery;

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function gcd () {
    const w = screen.width;
    const h = screen.height;

    return w/h;
}

async function takePart(toMain) {
    const headers = new Headers();

    headers.append("Content-Type", "application/json");

    const response = await sendRequest(
        "/products/lottery/participate/",
        {
            method: "POST",
            headers: headers,
            body: JSON.stringify({
                "to_main": toMain
            })
        }
    );

    if (!response.ok) {
        await makeWarn("Не удалось участвовать", "Проверьте соответствие требований!")
        return;
    }

    location.href = location.href;
}

async function renderLotteryInfo(renderMainPrize) {
    let item;

    if (renderMainPrize) {
        item = lottery.prize_main
    } else {
        item = lottery.prize_secondary
    }

    const user = await getAuthenticated();

//    if (!user) {
//        await makeWarn("Войдите в аккаунт!", "Для принятия участия в розыгрыше, нужно быть зарегистрированным!")
//        return;
//    }

    const isAuthenticated = user ? true : false;

    let requirementText;

    if (!isAuthenticated) {
        requirementText = `Сначала пройдите быструю регистрацию!`
    } else if (renderMainPrize) {
        requirementText = `Пополните свой баланс от ${lottery.deposit_amount_require}₽<br>Ваш баланс: ${user.balance}₽`;
    } else if (!requirementText) {
        requirementText = `При балансе > ${lottery.deposit_amount_require} вы можете так же участвовать в главном розыгрыше`;
    }

    let replenishButtonCode = "";

    if (isAuthenticated) {
        replenishButtonCode = `<button class="lottery-requirement-replenish-btn" onclick="location.href = '/replenish/'">ПОПОЛНИТЬ</button>`
    }

    const alreadyTakesPart = renderMainPrize ? lottery.take_part_main : lottery.take_part_second;

    const conversionButtonOnclickCode = isAuthenticated ? (alreadyTakesPart ? "return false;" : "takePart(" + renderMainPrize + ");return false;") : "location.href = '/auth/';";

    document.getElementById("prize-wrappper").innerHTML = `
    <div class="lottery-expand-info" style="transform: scale(0);" id="lotteryExpanded">
        <h3 class="lottery-expand-header">РАЗДАЧА<br>СКИНОВ
            <button class="lottery-expand-close-btn offer-cross" onclick="return reduceLotteryInfo();"></button>
        </h3>
        <div class="lottery-prize-info lotterty-info-row">
            <img src="${item.image_path}" class="lottery-prize-img">
            <span class="lottery-prize-name">${item.title}<br><span style="color: #FF007A;">${item.price} <img src="/core/static/img/gear.png"></span></span>
        </div>
        <div class="lottery-requirement lotterty-info-row">
            <span>${requirementText}</span>
            ${replenishButtonCode}
        </div>
        <div class="lottery-stats lotterty-info-row">
            <div class="timer lottery-timer" style="">
            <div class="timer-ring lottery-expand-ring" id="lotteryExpandTimerRing"></div>
                <div class="timer-data">
                    <span style="font-size: .9em;">осталось:</span>
                    <span style="font-size: 1.4em;font-family: 'Gilroy SemiBold';" id="lotteryExpandTimerValue">24:00:00</span>
                </div>
            </div>
            <span class="lottery-expand-partipicant-count">УЧАСТНИКОВ: ${lottery.display_participants_count+1}</span>
        </div>
        <button class="lottery-make-part-btn lotterty-info-row" type="button" onclick="${conversionButtonOnclickCode}">${isAuthenticated ? (alreadyTakesPart ? "ВЫ УЖЕ УЧАСТВУЕТЕ!" : "УЧАСТВОВАТЬ") : "РЕГИСТРАЦИЯ"}</button>
    </div>
    `;

    document.getElementById("prize-wrappper").onclick = reduceLotteryInfo;
    document.getElementById("prize-wrappper").style = "transition: all .2s ease;";

    document.getElementById("prize-wrappper").style.visibility = "visible";
    document.getElementById("prize-wrappper").style.display = "flex";
    document.getElementById("prize-wrappper").style.backgroundColor = "rgb(20, 20, 20, .9)";

    setTimeout(() => {
        document.getElementById("lotteryExpanded").style = "";
    }, 200);
}

function reduceLotteryInfo() {
    document.getElementById("lotteryExpanded").style = "transform: scale(0);opacity: 0;";
    document.getElementById("prize-wrappper").onclick = () => {};
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
//        time = ((60*60*24) - ((Date.now()/1000) - parseInt(getCookie("lottery-started-at"))));
//        time = (parseInt(getCookie("lottery-ended-at")) - ((Date.now()/1000) - parseInt(getCookie("lottery-started-at"))));

//        durationElapsedTime = (Date.now()/1000) - parseInt(getCookie("lottery-started-at"));
        time = parseInt(getCookie("lottery-ended-at") - Date.now()/1000);;

        if (time < 0) {
            try {document.getElementById("lotteryBanner").remove()} catch(error) {}
            try {reduceLotteryInfo()} catch(error) {}
            return;
        }

        const sec = parseInt(time%60);

        document.getElementById('lotteryTimerValue').innerHTML = `${zeroPad(parseInt(time / 60 / 60), 2)}:${zeroPad(parseInt((time % (60*60)) / 60), 2)}:${zeroPad(parseInt(time%60), 2)}`

        if (gcd() > 1/1) {
            document.getElementById('lotteryTimerRing').style.background = `radial-gradient(closest-side, rgb(255 0 122) 79%, transparent 80%, transparent 100%), conic-gradient(rgb(255, 255, 255) ${sec / 60 * 100}%, rgba(255, 255, 255, 0.2) 0deg)`;
        } else {
            document.getElementById('lotteryTimerRing').style.background = `radial-gradient(closest-side, rgb(34 34 34) 79%, transparent 80%, transparent 100%), conic-gradient(rgb(255, 255, 255) 30%, rgba(255, 255, 255, 0.2) 0deg) !important`;
        }

        try {
            document.getElementById('lotteryExpandTimerValue').innerHTML = `${zeroPad(parseInt(time / 60 / 60), 2)}:${zeroPad(parseInt((time % (60*60)) / 60), 2)}:${zeroPad(parseInt(time%60), 2)}`

            if (gcd() > 1/1) {
                document.getElementById('lotteryTimerRing').style.background = `radial-gradient(closest-side, rgb(255 0 122) 79%, transparent 80%, transparent 100%), conic-gradient(rgb(255, 255, 255) ${sec / 60 * 100}%, rgba(255, 255, 255, 0.2) 0deg)`;
            } else {
                document.getElementById('lotteryTimerRing').style.background = `radial-gradient(closest-side, rgb(34 34 34) 79%, transparent 80%, transparent 100%), conic-gradient(rgb(255, 255, 255) 30%, rgba(255, 255, 255, 0.2) 0deg) !important`;
            }
        } catch {}

        await sleep(1000);
    }
}

async function renderData(lottery_) {
    if (!lottery_) {
        return
    }

    if (((Date.now()/1000) - parseInt(getCookie("lottery-started-at")) >= 0) && ((Date.now()/1000) < parseInt(getCookie("lottery-ended-at")))) {
        document.getElementById("first-gun-name").innerHTML = lottery_.prize_main.title;
        document.getElementById("second-gun-name").innerHTML = lottery_.prize_secondary.title;

        if (lottery_.take_part_main) {
            document.getElementById("prizeGunFirst").style.filter = "opacity(.25)";
        }

        if (lottery_.take_part_second) {
            document.getElementById("prizeGunSecond").style.filter = "opacity(.25)";
        }

        document.getElementById("first-gun-img").src = lottery_.prize_main.image_path;
        document.getElementById("secondary-gun-img").src = lottery_.prize_secondary.image_path;

        document.getElementById("lotteryBanner").style.display = 'flex';

        await countDown();
    } else {
        document.getElementById("lotteryBanner").style.display = "none";
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

//    const lottery_wins_list = [137, 307];
//
//    if (user.lottery_wins_list) {
//        var itemResponses = [];
//
//        lottery_wins_list.forEach(async function(win) {
//            const response = await sendRequest(`/products/items/${win}/`, {method: "GET"});
//            console.log(response.ok);
//            if (response.ok) {
//                itemResponses.push(await response.json());
//            }
//        });
//
//        console.log(itemResponses);
//
//        if (itemResponses.length == 1) {
//            const result = itemResponses[0];
//            await printPrizeItem(result.image_path, result.price, `Победа: ${result.title}`, '', true);
//        } else if (itemResponses.length == 2) {
//            console.log(1);
//            const resultFirst = itemResponses[0];
//            const resultSecond = itemResponses[1];
//
//            printPrizeItem(
//                resultFirst.image_path,
//                resultFirst.price,
//                `Победа: ${resultFirst.title}`,
//                '',
//                true,
//                true,
//                `printPrizeItem("${resultSecond.image_path}", ${resultSecond.price}, "Победа #2: ${resultSecond.title}", "https://jackdrop.online/", true})`
//            )
//        }
//    }
//
//    console.log(user);

    await renderData(await getCurrentLottery());
}

window.renderLotteryInfo = renderLotteryInfo;
window.reduceLotteryInfo = reduceLotteryInfo;
window.takePart = takePart;

main();
