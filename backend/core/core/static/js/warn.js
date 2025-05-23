function makeWarn(header, desc) {
    const descHTML = desc ? `<span style="grid-row: 1;grid-column: 1;max-width: 75%;text-align: center;">${desc}</span>` : ''

    document.getElementById('prize-wrappper').innerHTML = `
        <div style="max-width: 90%; display: grid; grid-template-rows: 1fr; grid-template-columns: 1fr; place-items: center; transform: none; transition: 0.2s;" id="warn-content">
            <img src="https://s.iimg.su/s/21/HgBazUEhROqX0TutqYFK0sQWtWSAFjunhOz0E4Kr.png" style="grid-row: 1;grid-column: 1;max-width: 100%;width: 100%;">
            <div class="warn-content" style="grid-row: 1;grid-column: 1;display: flex;flex-direction: column;align-items: center;height: 100%;justify-content: center;">
                <h2 style="font-family: 'Gilroy Bold';font-size: 1.3em;max-width: 75%;text-align: center;">${header}</h2>
                ${descHTML}
                <button class="super-button" onclick="clearWarn()" style="margin-top: calc(0.83* 2em);">
                    <span class="super-button-bg"></span>
                    <span class="super-button-text">Окей</span>
                </button>
            </div>
        </div>
    `;

    document.getElementById("prize-wrappper").style.display = 'flex';
    document.getElementById("prize-wrappper").style.visibility = 'visible';
    document.getElementById("prize-wrappper").style.background = 'rgb(20, 20, 20, .5)';

    setTimeout(() => {
        document.getElementById("warn-content").style.transform = 'none';
    })
}

function clearWarn() {
    document.getElementById("warn-content").style.transform = 'scale(0)';

    setTimeout(() => {
        document.getElementById('prize-wrappper').style.background = 'none';
        document.getElementById("prize-wrappper").style.visibility = 'hidden';
        document.getElementById('prize-wrappper').innerHTML = '';
    }, 200)
}
