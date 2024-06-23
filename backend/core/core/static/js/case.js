const caseImg = document.getElementById('case-img');
const caseTitle = document.getElementById('case-title');
const caseItems = document.getElementById('case-items');


async function getCase(id) {
    const formdata = new FormData();
    const requestOptions = {
      method: "GET",
      redirect: "follow"
    };

    const response = await fetch(
        `http://localhost/products/cases/api/v1/case/${id}/items/`,
        requestOptions
    );

    const result = await response.json();

    console.log(result);

    caseTitle.innerHTML = result.case.title;
    caseImg.src = result.case.image_path;

    result.items.forEach((element) => {
        caseItems.innerHTML += `
            <article class="dropped rare">
                    <div class="w-line"></div>
                    <div class="dropped-content">
                        <span>${element.title}</span>
                        <img src="${element.image_path}">
                    </div>
            </article>
        `;
    });
}
