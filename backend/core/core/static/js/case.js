const caseImg = document.getElementById('case-img');
const caseTitle = document.getElementById('case-title');
const caseItems = document.getElementById('case-items');
let caseId = null;


async function getCase(id) {
    const formdata = new FormData();
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    caseId = id;

    const response = await fetch(
        `http://localhost/products/cases/api/v1/case/${id}/items/`,
        requestOptions
    );

    const result = await response.json();

    console.log(result);

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

document.getElementById('open-case-btn').addEventListener("click", () => {location.href = `/case/${caseId}/drop/`});
