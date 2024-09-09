function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const statsWebSocket = new WebSocket(`wss://${location.hostname}/games/ws/stats/`);

statsWebSocket.onmessage = function(event) {
    const jsondata =  JSON.parse(JSON.parse(event.data));

    Object.entries(jsondata).forEach(([key, value]) => {
        if (key != 'id') {
            console.log(`${key}-val`);
            document.getElementById(`${key}-val`).style.opacity = 0;
            document.getElementById(`${key}-val`).innerHTML = value;
            document.getElementById(`${key}-val`).style.opacity = 1;
        }
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

start();
