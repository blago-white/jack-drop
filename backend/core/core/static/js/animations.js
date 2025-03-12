const animationsDurations = {
    "upgrade1": 9000,
    "upgrade2": 9000,
    "otkritie": 4000,
    "unlucky": 4000
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

export async function useAnim(freezeLast=true, animId) {
    startAnim(animId, freezeLast);

    if (!freezeLast) {
        await sleep(animationsDurations[animId] || 9000);
    }
}


function startAnim(animId='unlucky', freeze) {
    document.getElementById("prize-wrappper").style.display = 'flex';
    document.getElementById("prize-wrappper").style.visibility = 'visible';

    document.getElementById("prize-wrappper").innerHTML = `
        <video class="animation ${freeze == true ? 'active-forever' : 'active'}" id="animation" autoplay>
            <source src="/core/static/webm/${animId}.webm">
        </video>
    `;
}

function closeAnimation() {
    document.getElementById('prize-wrappper').style = ''

    setTimeout(() => {
        document.getElementById('prize-wrappper').innerHTML = '';
    }, 200)
}

export async function printPrizeItem(itemImg, itemPrice, itemTitle, redirectUrl='', useAutoPlay=false, notRedirect=false) {
    document.getElementById("prize-wrappper").style.display = 'flex';
    document.getElementById("prize-wrappper").style.visibility = 'visible';
    document.getElementById("prize-wrappper").style.background = 'rgb(20, 20, 20, .5)';
    redirectUrl = redirectUrl || location.href;

    const receiveButtonText = getCookie('lang') == 'ru' ? 'Получить!' : 'Receive Item!';

    document.getElementById("prize-wrappper").innerHTML = `
        <video class="animation" id="animation" style="position: absolute;" autoplay=${useAutoPlay}>
            <source src="/core/static/webm/otkritie.webm">
        </video>
        <img class="anim-item-img" id="animItemImg" src="${itemImg}">
        <button style="position: absolute;top: 78vh;"
        class="super-button pink">
            <span class="super-button-bg" style="background: transparent;box-shadow: 0 0 0 7px #0047FF!important;"></span>
            <span class="super-button-text">
                <span id="user-data-h" style="list-style: none;display: flex;flex-direction: column;align-items: flex-start;padding: 0px;margin: 0px;">
                    <span id="acc-username-header">${itemTitle}</span>
                </span>
            </span>
        </button>
        <button style="position: absolute;top: 86vh;"
        class="super-button pink" onclick="${notRedirect ? "closeAnimation()" : ("location.href = '" + redirectUrl + "'")}">
            <span class="super-button-bg" style="background: #FF007A;"></span>
            <span class="super-button-text">
                <span id="user-data-h" style="list-style: none;display: flex;flex-direction: column;align-items: flex-start;padding: 0px;margin: 0px;">
                    <span id="acc-username-header">${receiveButtonText}</span>
                </span>
            </span>
        </button>
    `;

    await sleep(50);

    document.getElementById("animation").classList.toggle("active-forever");

    if (!useAutoPlay) {
        await document.getElementById('animation').play();
    }

    await sleep(1450);

    document.getElementById("animItemImg").classList.toggle("active");
}

document.getElementById("prize-wrappper").innerHTML = '';

Object.keys(animationsDurations).forEach((key) => {
    document.getElementById("prize-wrappper").innerHTML += `
        <video src="/core/static/webm/${key}.webm">
    `;
})

window.closeAnimation = closeAnimation;
