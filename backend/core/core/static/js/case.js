const caseImg = document.getElementById('case-img');
const caseTitle = document.getElementById('case-title');
const caseItems = document.getElementById('case-items');
let caseId = null;

function unlockOpen(id) {
    document.getElementById('open-case-btn').addEventListener("click", () => {location.href = `/case/${caseId}/drop/`});

    Array.from(document.getElementById('open-case-btn').children).forEach((child) => {
        child.classList.remove("noactive")
        return;
    });
}

async function checkFreeCaseAvailable(id) {
    const formdata = new FormData();
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    const response = await sendRequest(
        `http://localhost/products/bonus-buy/has-case/${id}/`,
        requestOptions
    );

    const result = await response.json();

    return result.ok;
}

async function getCase(id) {
    const formdata = new FormData();
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    caseId = id;

    const response = await sendRequest(
        `http://localhost/products/cases/api/v1/case/${id}/items/`,
        requestOptions
    );

    const result = await response.json();

    console.log(await getUserData());

    if ((result.case.price) == 0) {
        if (await checkFreeCaseAvailable(id)) {
            unlockOpen(caseId);
        }
    } else {
        if (result.case.price <= (await getUserData()).balance) {
            unlockOpen(caseId);
        }
    }

    caseTitle.innerHTML = result.case.title;
    caseImg.src = result.case.image_path;

    document.getElementById('case-drop-data').style = "display: flex;gap: 1ch;"
    document.getElementById('price-label-span').innerHTML = `${result.case.price} <img style="height: 2ch;" src="/core/static/img/scrap.png">`

    result.items.forEach((element) => {
        caseItems.innerHTML += `
            <article style="display: flex;flex-direction: column;align-items: center; gap: 1ch;">
                <div class="dropped rare">
                        <div class="w-line"></div>
                        <div class="dropped-content">
                            <span>${element.title}</span>
                            <div style="display: flex;flex-direction: row;gap: 1ch;">
                                <span class="item-price blue"><span>${element.price}</span></span>
                                <span class="item-price blue"><span>${(element.rate*100).toFixed(2)}%</span></span>
                            </div>
                            <img src="${element.image_path}">
                        </div>
                </div>
            </article>
        `;
    });
}
