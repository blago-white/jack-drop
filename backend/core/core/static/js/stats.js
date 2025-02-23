function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const statsWebSocket = new WebSocket(`ws://${location.hostname}/games/ws/stats/`);

statsWebSocket.onmessage = async function(event) {
    const jsondata =  JSON.parse(JSON.parse(event.data));

    let valueRepr;

    Object.entries(jsondata).forEach(([key, value]) => {
        if (key != 'id') {
            document.getElementById(`${key}-val`).style.opacity = 0;
            setTimeout(async function() => {
                document.getElementById(`${key}-val`).style.opacity = 1;

                valueRepr = parseInt(value);

                for (let i = 0; i < valueRepr; i+=2) {
                    document.getElementById(`${key}-val`).innerHTML = i;
                    await sleep(1);
                }
            }
        }, 200)}
    });
};


function get() {
    if (statsWebSocket.readyState == WebSocket.OPEN) {
        statsWebSocket.send(JSON.stringify({
            "type": "get",
            "payload": {},
        }));
    }
}

async function start() {
    while (true) {
        get();
        await sleep(3000);
    }
}

const windowInnerWidth = document.documentElement.clientWidth
const windowInnerHeight = document.documentElement.clientHeight

if (windowInnerWidth / windowInnerHeight < 1) {
    Array.from(document.getElementsByClassName("flex-stat")).forEach((elem) => {elem.remove()})
}


start();
