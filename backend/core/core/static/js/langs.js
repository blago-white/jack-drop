async function setLang(lang) {
    const data = new FormData();
    const headers = new Headers();

    data.append("language", lang);
    data.append("csrfmiddlewaretoken", document.cookie.split("=")[1].split(";")[0]);

    headers.append("X-CSRFToken", document.cookie.split("=")[1].split(";")[0]);

    const requestOptions = {
      method: "POST",
      headers: headers,
      body: data,
      redirect: "follow"
    };

    response = await fetch("http://localhost/i18n/setlang/", requestOptions);

    location.href = location.href;
}