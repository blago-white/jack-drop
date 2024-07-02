const counterClock = document.getElementById('clock');

const dayCount =  document.getElementById('day-count');
const hrsCount =  document.getElementById('hrs-count');
const minCount =  document.getElementById('min-count');
const secCount =  document.getElementById('sec-count');

const timeLimits = [31, 24, 60, 60];

const dateWithoutTimezone = (date) => {
   const tzoffset = date.getTimezoneOffset() * 60000; // Get the timezone offset in milliseconds
   const withoutTimezone = new Date(date.valueOf() - tzoffset)
      .toISOString()
      .slice(0, -1); // Remove the trailing 'Z'
   return withoutTimezone;
};

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function zFill(num, size) {
    num = num.toString();
    while (num.length < size) num = "0" + num;
    return num;
}

function saveTime(times) {
    console.log(times);

    dayCount.innerHTML = times[0];
    hrsCount.innerHTML = times[1];
    minCount.innerHTML = times[2];
    secCount.innerHTML = times[3];
}

function getTime() {
    return [
        parseInt(dayCount.innerHTML),
        parseInt(hrsCount.innerHTML),
        parseInt(minCount.innerHTML),
        parseInt(secCount.innerHTML)
    ]
}

function getNewTime(times) {
    let summary = times[3] + (times[2] * 60) + (times[1] * 60 * 60) + (times[0] * 24 * 60 * 60);

    if (!summary) {
        return false;
    }

    summary -= 1;

    const d = Math.floor(summary/86400);
    const h = Math.floor((summary - d*86400) / (60 * 60));
    const m = Math.floor((summary - (d*86400 + h * (60*60))) / 60);
    const s = (summary - (d*86400 + h * (60*60) + m*60));

    return [
        zFill(d, 2),
        zFill(h, 2),
        zFill(m, 2),
        zFill(s, 2)
    ];
}

function hideCountDown() {
        document.getElementById('c-d-desc').style.display = 'none';
        counterClock.style.display = 'none';
        document.getElementById('start-btn').style.display = 'grid';

        document.getElementsByClassName('wheel-game-title')[0].style.marginTop = '0px';
        document.getElementsByClassName('inner-wheel')[0].style.justifyContent = 'center';

        document.getElementById('code-btn').style.display = 'none';

        return false;
}

function updateClock(time) {
    current = getTime();

    newTime = getNewTime(current);

    if (!newTime) {
        hideCountDown();
    }

    saveTime(newTime);
    return true;
}

async function setWheelTimeout() {
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    const response = await fetch("http://localhost/products/games/fortune-wheel/timeout/", requestOptions);

    const result = await response.json();

    let unix_timestamp = Math.floor(Date.now()/1000 - result.current) + result.timeout;

    if (unix_timestamp < 1 || !unix_timestamp) {
        hideCountDown();
        return false;
    }

    const hours = Math.floor((unix_timestamp % (60 * 60 * 24)) / (60*60));

    const minutes = Math.floor((unix_timestamp % (60 * 60)) / 60);

    const seconds = Math.ceil(unix_timestamp % 60);

    saveTime([
        zFill(Math.floor(unix_timestamp / (60 * 60 * 24)), 2),
        zFill(hours, 2),
        zFill(minutes, 2),
        zFill(seconds, 2)
    ]);

    return true;
}

async function main() {
    if (!await setWheelTimeout()) {
        return
    }

    while (true) {
        await sleep(1000);

        if (!updateClock()) {
            return
        }
    }
}

main();
