const casesSec = document.getElementById('cases-sec');

function addCases(category, cases) {
    console.log(typeof cases, cases);

    let html = `
        <section class="free-cases-sec">
            <h2 id="cases-category">${category}</h2>
            <ul class="cases-row" id="cases-row">
    `;

    cases.forEach((element) => {
        html += `
            <li class="case-data" onclick="location.href = 'case/${element.id}/'">
                <img src="${ element.image_path }" class="case-image">
                <h3>${ element.title }</h3>
                <span>${ element.price }р</span>
            </li>
        `
    });

    html += `</ul></section>`;

    casesSec.innerHTML += html;
}


async function addItemSets() {
    const itemSet = await sendRequestJson("http://jackdrop.online/products/items/sets/", {method: "GET"})

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
                <span>${ element.price }р</span>
            </li>
        `
    });

    html += `</ul></section>`;

    casesSec.innerHTML += html;
}

async function getCases() {
    let params = new URL(document.location.toString()).searchParams;

    const formdata = new FormData();
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    const response = await sendRequest("http://jackdrop.online/products/cases/api/v1/by-categories/?"+params, requestOptions);

    const result = await response.json();

    console.log(result);

    c = false;

    addCases(result[0].category, result[0].cases)

    await addItemSets();

    result.slice(1).forEach((element) => {
        addCases(element.category, element.cases)
    })

    return result
}

async function start() {
    const res = await getCases();

    addCases(res);
}

start();
