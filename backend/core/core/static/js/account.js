async function renderInfo() {
    const response = await sendRequestJson("/auth/api/v1/public/user/", {mehtod: "GET", headers: new Headers()})

    console.log(response);

    document.getElementById('usr-name').innerHTML = `${response.username}<span class="account-id-val">ID ${response.id}</span>`;
    document.getElementById('balance').innerHTML = `${response.balance}`;
}

renderInfo();
