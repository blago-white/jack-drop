const feedSocket = new WebSocket("ws://localhost/products/ws/feed/");
const feed = document.getElementById('live-string');

feedSocket.onmessage = function(event) {
    const jsondata =  JSON.parse(JSON.parse(event.data));

    console.log(jsondata, jsondata.title, jsondata.image, feed.children);

    if (feed.children.length) {
        console.log(feed.children[0]);

        const node = `
            <article class="dropped rare">
                <div class="w-line"></div>
                <div class="dropped-content">
                    <span>${jsondata.title}</span>
                    <span style="margin-left: .5vw;" class="item-price rose"><span>${jsondata.price}</span> <img style="left: 0px;" src="/core/static/img/gear.png"></span>
                    <img src="${jsondata.image}">
                </div>
            </article>
        `

        feed.innerHTML = node + feed.innerHTML;
    } else {
        feed.innerHTML += `
            <article class="dropped rare">
                <div class="w-line"></div>
                <div class="dropped-content">
                    <span>${jsondata.title}</span>
                    <span style="margin-left: .5vw;" class="item-price rose"><span>${jsondata.price}</span> <img style="left: 0px;" src="/core/static/img/gear.png"></span>
                    <img src="${jsondata.image}">
                </div>
            </article>
        `
    }
};

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function randomIntFromInterval(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

function get() {
    feedSocket.send(JSON.stringify({
        "type": "get",
        "payload": {},
    }));
}

async function start() {
    while (true) {
        await sleep(randomIntFromInterval(500, 2000));
        get();
    }
}

start();
