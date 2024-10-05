const caseImg = document.getElementById('case-img');
const caseTitle = document.getElementById('case-title');
const caseItems = document.getElementById('case-items');
const caseDescription = document.getElementById('case-desc');

let caseId = null;
let USE_BONUS_CASE = false;

let caseDiscount = 0;
let caseFree = false;

function getCardColor(itemsCount, indexCurrent) {
    if (indexCurrent <= itemsCount/10) {
        return "red"
    } else if (indexCurrent <= itemsCount * 0.25) {
        return "pink"
    } else if (indexCurrent <= itemsCount * 0.45) {
        return "purple"
    } else if (indexCurrent <= indexCurrent * 0.7) {
        return "blue"
    } else {
        return "yellow"
    }
}

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
        `https://${location.hostname}/products/bonus-buy/bonuse/${id}/`,
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
        `https://${location.hostname}/products/cases/api/v1/case/${id}/items/`,
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
    caseDescription.innerHTML = result.case.description;
    caseImg.src = result.case.image_path;

    document.getElementById('case-drop-data').style = "display: flex;gap: 1ch;";

    if (USE_BONUS_CASE) {
        document.getElementById('price-label-span').innerHTML = `<del style="color: #aaa;">${result.case.price}</del>&nbsp;${caseFree ? 0 : Math.ceil(result.case.price * (1 - (caseDiscount / 100)))} <img style="height: 2ch;" src="/core/static/img/scrap.png">`
    } else {
        document.getElementById('price-label-span').innerHTML = `${result.case.price} <img style="height: 2ch;" src="/core/static/img/scrap.png">`
    }

    let c = 0;
    let rareColor;

    result.items.forEach((element) => {
        rareColor = getCardColor(result.items.count, c);

        caseItems.innerHTML += `
            <article class="item-card" style="background: url(/core/static/img/card-bg-${rareColor}.png);background-size: cover;">
                <div class="dropped-content">
                    <div class="item-numeric-info">
                        <span class="item-price ${rareColor}"><span>${element.price}</span></span>
                        <span class="item-price ${rareColor}"><span>${(element.rate*100).toFixed(2)}%</span></span>
                    </div>

                    <div style="display: grid;grid-template-rows: 1fr;grid-template-columns: 1fr;width: 100%;max-width: 100%;justify-items: center;align-items: center;">
                        <img src="/core/static/img/card-jd-logo.png" style="grid-row: 1;grid-column: 1;width: 100%;">
                        <img src="${element.image_path}" style="width: 100%;grid-row: 1;grid-column: 1;">
                    </div>

                    <span class="item-title">${element.title}</span>
                </div>
            </article>
        `;

        c++;
    });
}


async function changeBtn() {
    if (!(await getAuthenticated())) {
        let c = false;

        Array.from(document.getElementById('open-case-btn').children).forEach((element) => {
            if (c) {
                element.innerHTML = document.getElementById('long-enter-text').innerHTML;
            } else {
                element.classList.remove("noactive");
            }

            c = true;
        })

        document.getElementById('open-case-btn').onclick = () => {
            location.href = '/auth/';
        };
    }
}


changeBtn();
