const battlesList = document.getElementById('battles');
const battlesHead = document.getElementById('battles-head');
const battlesTable = document.getElementById('battles-table');

const foundingLabel = document.getElementById('founding-label');
const battlesRequest = document.getElementById('battle-request-controls');

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function onCreateBattle() {
    battlesHead.style.display = 'none';
    battlesTable.style.display = 'none';

    battlesRequest.style.display = 'flex';

    let c = 0;

    while (true) {
        await sleep(1000);
        c += 1;

        if (c % 4 == 0 && c > 0) {
            foundingLabel.innerHTML = foundingLabel.innerHTML.slice(0, -3);
        } else {
            foundingLabel.innerHTML += ".";
        }
    }
}

function cancelRequest() {
    console.log(123);

    battlesHead.style = '';
    battlesTable.style = '';

    battlesRequest.style.display = 'none';
}
