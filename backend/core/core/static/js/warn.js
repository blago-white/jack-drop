function makeWarn(header, desc) {
    document.getElementById('prize-wrappper').innerHTML = `
<div style="display: grid;grid-template-rows: 1fr;grid-template-columns: 1fr;justify-items: center;align-items: center;">
<img src="https://s.iimg.su/s/21/HgBazUEhROqX0TutqYFK0sQWtWSAFjunhOz0E4Kr.png" style="grid-row: 1;grid-column: 1;width: 100%;">
<div class="warn-content" style="grid-row: 1;grid-column: 1;display: flex;flex-direction: column;align-items: center;">
    <h2 style="font-family: 'Gilroy Bold';font-size: 2em;">${header}</h2>
<span style="grid-row: 1;grid-column: 1;">${desc}</span>
<button class="super-button" onclick="clearWarn()" style="margin-top: calc(0.83* 2em);">
    <span class="super-button-bg"></span>
    <span class="super-button-text">Окей</span>
</button></div></div>
    `

    document.getElementById("prize-wrappper").style.display = 'flex';
    document.getElementById("prize-wrappper").style.visibility = 'visible';
    document.getElementById("prize-wrappper").style.background = 'rgb(20, 20, 20, .5)';
}

function clearWarn() {
    document.getElementById('prize-wrappper').innerHTML = '';
    document.getElementById('prize-wrappper').style.background = 'none';
    document.getElementById("prize-wrappper").style.visibility = 'hidden';
}
