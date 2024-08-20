function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
};

async function setLang(lang) {
    const data = new FormData();
    const headers = new Headers();

    data.append("language", lang);

    headers.append("X-CSRFToken", getCookie("csrftoken"));

    const requestOptions = {
      method: "POST",
      headers: headers,
      body: data,
      redirect: "follow"
    };

    response = await sendRequest(`https://${location.hostname}/i18n/setlang/`, requestOptions);

    location.href = location.href;
}