const caseImg = document.getElementById('case-img');
const caseTitle = document.getElementById('case-title');
const caseItems = document.getElementById('case-items');
let caseId = null;
let USE_BONUS_CASE = false;

let caseDiscount = 0;
let caseFree = false;

function unlockOpen(id) {
    if (caseFree) {
        document.getElementById('open-case-btn').addEventListener("click", () => {
            location.href = `/case/${caseId}/drop/?bonus=1`
        });
    } else if (caseDiscount > 0) {
        document.getElementById('open-case-btn').addEventListener("click", () => {
            location.href = `/case/${caseId}/drop/?discount=1`
        });
    } else {
        document.getElementById('open-case-btn').addEventListener("click", () => {
            location.href = `/case/${caseId}/drop/`
        });
    }

    Array.from(document.getElementById('open-case-btn').children).forEach((child) => {
        child.classList.remove("noactive")
        return;
    });
}

async function checkBonusCaseAvailable(id) {
    const formdata = new FormData();
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    const response = await sendRequest(
        `http://${location.hostname}/products/bonus-buy/bonuse/${id}/`,
        requestOptions
    );

    const result = await response.json();

    return result;
}

async function getCase(id) {
    const formdata = new FormData();
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    caseId = id;

    const response = await sendRequest(
        `http://${location.hostname}/products/cases/api/v1/case/${id}/items/`,
        requestOptions
    );

    const result = await response.json();

    console.log(await getUserData());

    const bonus = await checkBonusCaseAvailable(id);

    if (bonus.free || bonus.discount > 0) {
        USE_BONUS_CASE = true;
        caseDiscount = bonus.discount;
        caseFree = bonus.free;

        console.log(bonus);

        unlockOpen(caseId);
    } else if (result.case.price > 0) {
        if (result.case.price <= (await getUserData()).balance) {
            unlockOpen(caseId);
        }
    }

    caseTitle.innerHTML = result.case.title;
    caseImg.src = result.case.image_path;

    document.getElementById('case-drop-data').style = "display: flex;gap: 1ch;";

    if (USE_BONUS_CASE) {
        document.getElementById('price-label-span').innerHTML = `<del style="color: #aaa;">${result.case.price}</del>&nbsp;${caseFree ? 0 : Math.ceil(result.case.price * (1 - (caseDiscount / 100)))} <img style="height: 2ch;" src="/core/static/img/scrap.png">`
    } else {
        document.getElementById('price-label-span').innerHTML = `${result.case.price} <img style="height: 2ch;" src="/core/static/img/scrap.png">`
    }

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
