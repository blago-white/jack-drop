const casesSec = document.getElementById('cases-sec');

function addCases(category, cases, bonuses) {
    let html = `
        <section class="free-cases-sec">
            <h2 id="cases-category">${category}</h2>
            <ul class="cases-row" id="cases-row">
    `;

    let realPrice;
    let priceLabel;

    cases.forEach((element) => {

        if (bonuses.free.includes(element.id)) {
            realPrice = 0
        } else if (bonuses.discounted.get(element.id)) {
            realPrice = bonuses.discounted.get(element.id)
        }

        if (realPrice != undefined) {
            priceLabel = `${realPrice} <span style="text-decoration: line-through;color: rgb(210, 210, 210);">${element.price}</span>`
        } else {
            priceLabel = `${element.price}`
        }

        html += `
            <li class="case-data" onclick="location.href = 'case/${element.id}/'">
                <img src="${ element.image_path }" class="case-image">
                <h3>${ element.title }</h3>
                <span>${priceLabel} <img src="/core/static/img/gear.png"></span>
            </li>
        `

        realPrice = undefined;
    });

    html += `</ul></section>`;

    casesSec.innerHTML += html;
}


async function addItemSets() {
    const itemSet = await sendRequestJson(`http://${location.hostname}/products/items/sets/`, {method: "GET"})

    console.log(itemSet);

    let html = `
        <section class="free-cases-sec">
            <h2 id="cases-category">НАБОРЫ</h2>
            <ul class="cases-row" id="cases-row">
    `;

    itemSet.forEach((element) => {
        html += `
            <li class="case-data" onclick="location.href = 'set/${element.id}/'">
                <img src="${ element.image_path }" class="case-image">
                <h3>${ element.title }</h3>
                <span>${ element.price } <img src="/core/static/img/gear.png"></span>
            </li>
        `
    });

    html += `</ul></section>`;

    casesSec.innerHTML += html;
}

async function getBonuses() {
    const formdata = new FormData();
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    const response = await sendRequest(`http://${location.hostname}/products/bonus-buy/bonuse/all/`, requestOptions);

    if (!response.ok) {
        return {
            "free": [],
            "discounted": {}
        }
    } else {
        return await response.json();
    }
}

async function getCases() {
    let params = new URL(document.location.toString()).searchParams;

    const formdata = new FormData();
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    const response = await sendRequest(`http://${location.hostname}/products/cases/api/v1/by-categories/?`+params, requestOptions);

    const result = await response.json();

    console.log(result);

    c = false;

    const bonuses = await getBonuses();

    addCases(result[0].category, result[0].cases, bonuses)

    await addItemSets();

    result.slice(1).forEach((element) => {
        addCases(element.category, element.cases)
    })

    return result
}

async function start() {
    console.log(1)

    const res = await getCases();

    console.log(2)

    addCases(res);

    console.log(3);
}

start();
