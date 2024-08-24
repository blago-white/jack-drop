let USERDATA;

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
};

function getAccess() {
    return getCookie("access");
}

function setCookie(name, value, options = {}) {
    options = {
        path: '/',
        ...options
    };

    if (options.expires instanceof Date) {
        options.expires = options.expires.toUTCString();
    }

    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

    for (let optionKey in options) {
        updatedCookie += "; " + optionKey;
        let optionValue = options[optionKey];
        if (optionValue !== true) {
            updatedCookie += "=" + optionValue;
        }
    }

    document.cookie = updatedCookie;
}

function getRefresh() {
    return getCookie("refresh");
}

async function refreshJWT() {
    const data = new FormData();

    data.append('refresh', getRefresh());

    const response = await fetch('/auth/api/token/refresh/', {
        headers: new Headers(),
        method: "POST",
        body: data,
    });

    if (!response.ok) {
        return false;
    } else {
        const result = await response.json();

        setCookie("access", result.access);

        return result.access;
    }
}

async function sendRequestJson(url, requestOptions) {
    let result = await sendRequest(url, requestOptions);

    result = await result.json();

    return result;
}

async function sendRequest(url, requestOptions, __req = false) {
    if (!requestOptions.headers) {
        requestOptions.headers = new Headers();
    }

    if (getAccess()) {
        if (requestOptions.headers.has("Authorization")) {
            requestOptions.headers.delete("Authorization");
        }

        requestOptions.headers.append("Authorization", "Bearer "+getAccess());
    }

    console.log(getCookie("csrftoken"));

    requestOptions.headers.delete("X-CSRFToken");
    requestOptions.headers.append("X-CSRFToken", getCookie("csrftoken"));

    const response = await fetch(url, requestOptions);

    if (response.status == 401 || response.status == 403) {
        const resultRefresh = await refreshJWT();

        if (resultRefresh && (!__req)) {
            return await sendRequest(url, requestOptions, __req=true);
        }
    }

    return response;
}

async function getUserData() {
    if (USERDATA) {
        return USERDATA;
    }

    const response = await sendRequest("/auth/api/v1/public/user/", {method: "GET", headers: new Headers()});

    if (!response.ok) {
        return false;
    } else {
        USERDATA = await response.json();
        return USERDATA;
    }
}

async function getAuthenticated() {
    if (getRefresh()) {
        return await getUserData();
    } else {
        return false;
    }
}

async function processUserAuthStatus() {
    const authenticated = await getAuthenticated();

    if (authenticated) {
        Array.from(document.getElementsByClassName('user-avatar')).forEach((elem) => {elem.src = authenticated.avatar});

        document.getElementById('acc-username-header').innerHTML = authenticated.username;
        document.getElementById('acc-balance-header').innerHTML = `${Math.floor(authenticated.balance)} <img src="/core/static/img/gear.png">`;
        document.getElementById('account-info-btn').style = "";
        document.getElementById('auth-required-btn').style.display = "none";
    } else {
        document.getElementById('auth-required-btn').style = "";
    }
}

processUserAuthStatus();
