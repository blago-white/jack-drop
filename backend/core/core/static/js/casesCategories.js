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

async function getCases() {
    const formdata = new FormData();
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    const response = await fetch("http://localhost/products/cases/api/v1/by-categories/", requestOptions);

    const result = await response.json();

    console.log(result);

    result.forEach((element) => {
        addCases(element.category, element.cases)
    })

    return result
}

async function start() {
    const res = await getCases();

    addCases(res);
}

start();
