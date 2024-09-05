function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const statsWebSocket = new WebSocket(`ws://${location.hostname}/games/ws/stats/`);

statsWebSocket.onmessage = function(event) {
    const jsondata =  JSON.parse(JSON.parse(event.data));

    Object.entries(jsondata).forEach(([key, value]) => {
        if (key != 'id') {
            console.log(`${key}-val`);
            document.getElementById(`${key}-val`).innerHTML = value;
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
