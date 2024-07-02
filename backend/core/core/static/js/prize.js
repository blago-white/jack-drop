let expanded = false;


export function renderItemPrize(title, price, image_path, acceptText) {
    if (expanded) {
        return
    }

    document.getElementById('prize-wrappper').style.display = "flex";
    document.getElementById('prize-wrappper').style.visibility = "visible";
    expanded = true;
    setTimeout(() => {
        document.getElementById('prize-wrappper').style.opacity = "1";
        document.getElementById('prize-body').innerHTML += `
            <img src="${image_path}">
            <h3 style="text-transform: none;">${title}</h3>
            <span style="font-size: xx-large;">${price}<img src="/core/static/img/scrap.png" style="width: 3ch"></span>
            <button class="super-button" style="font-family: 'Gilroy SemiBold'" onclick="closePrizeWindow()">
                <span class="super-button-bg"></span>
                <span class="super-button-text" style="font-size: x-large">${acceptText}</span>
            </button>
        `;
        document.getElementById('prize-body').style.transform = "translateY(0vh)";
    }, 300)
}


export function renderPrize(html) {
    if (expanded) {
        return
    }

    document.getElementById('prize-wrappper').style.display = "flex";
    document.getElementById('prize-wrappper').style.visibility = "visible";
    expanded = true;

    console.log(html);

    setTimeout(() => {
        document.getElementById('prize-wrappper').style.opacity = "1";
        document.getElementById('prize-body').innerHTML += `
            ${html}
        `;
        document.getElementById('prize-body').style.transform = "translateY(0vh)";
    }, 300)
}

function closePrizeWindow(redir) {
    closeWindow();

    const elem = document.getElementById(
        'DESTIGATION_ON_CLOSE_WINDOW'
    );

    setTimeout(() => {
        location.href = redir ? redir : (elem ? elem.innerHTML : location.href);
    }, 300)
}

function closeWindow() {
    document.getElementById('prize-body').style.transform = "translateY(-90vh)";
}

window.closePrizeWindow = closePrizeWindow;
