function renderLotteryInfo(renderMainPrize) {
    document.getElementById("prize-wrapper").innerHTML = `
    <div class="lottery-expand-info" style="transform: scale(0);" id="lotteryExpanded">
        <h3 class="lottery-expand-header">РАЗДАЧА<br>СКИНОВ
            <button class="lottery-expand-close-btn">X</button>
        </h3>
        <div class="lottery-prize-info">
            <img src="https://cdn.rust.tm/item/AK+Royale/300.png" class="lottery-prize-img">
            <span class="lottery-prize-name">StatTrak™ MAC-10 | Neon Rider</span>
        </div>
        <div class="lottery-requirement">
            <span>Пополните свой баланс от 30 000₽<br>Ваш баланс: 0₽</span>
            <button class="lottery-requirement-replenish-btn">ПОПОЛНИТЬ</button>
        </div>
        <div class="lottery-stats">
            <div class="timer lottery-timer" style="">
            <div class="timer-ring lottery-expand-ring" id="timerRing"></div>
                <div class="timer-data">
                    <span style="font-size: .9em;">осталось:</span>
                    <span style="font-size: 1.4em;font-family: 'Gilroy SemiBold';" id="timerValue">24:00:00</span>
                </div>
            </div>
            <span class="lottery-expand-partipicant-count">УЧАСТНИКОВ: 24</span>
        </div>
        <button class="lottery-make-part-btn">УЧАСТВОВАТЬ</button>
    </div>
    `;

    document.getElementById("prize-wrapper").style = "transition: all .2s ease;";

    document.getElementById("prize-wrapper").style.visibility = "visible";
    document.getElementById("prize-wrapper").style.display = "flex";
    document.getElementById("prize-wrapper").style.backgroundColor = "rgb(20, 20, 20, .9)";

    setTimeout(() => {
        document.getElementById("lotteryExpanded").style = "";
    }, 200);
}

const user = getAuthenticated();

if (!user || (user.id != 57)) {
    document.getElementById("lotteryBanner").style.display = 'none';
}

window.renderLotteryInfo = renderLotteryInfo;
