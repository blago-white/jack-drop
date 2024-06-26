const dropItemsString = document.getElementById('items');

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

    let line = ``;

    result.items.forEach((element) => {
        line += `
            <article class="dropped mono">
                    <div class="w-line"></div>
                    <div class="dropped-content">
                        <span>${element.title}</span>
                        <img src="${element.image_path}">
                    </div>
            </article>
        `;
    });

    dropItemsString.innerHTML += line + line + line + line + line + line + line + line + line + line + line + line + line + line + line;

    await dropCase();
}
//    caseTitle.innerHTML = result.case.title;
//    caseImg.src = result.case.image_path;

//    result.items.forEach((element) => {
//        caseItems.innerHTML += `
//            <article class="dropped rare">
//                    <div class="w-line"></div>
//                    <div class="dropped-content">
//                        <span>${element.title}</span>
//                        <img src="${element.image_path}">
//                    </div>
//            </article>
//        `;
//    });

async function dropCase() {
    const headers = new Headers();

    headers.append("Content-Type", "application/json");
    headers.append("X-CSRFToken", document.cookie.split("=")[1].split(";")[0]);

    const requestOptions = {
      method: "POST",
      headers: headers,
      body: JSON.stringify({}),
      redirect: "follow"
    };

    const response = await fetch(
        `http://localhost/products/games/drop/${caseId}/`,
        requestOptions
    );

    const result = await response.json();

    console.log(result);
}
