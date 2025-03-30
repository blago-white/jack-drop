const url = new URL(document.location.href);

document.getElementById("price1").addEventListener("click", () => {
    url.searchParams.set("min", 0);
    url.searchParams.set("max", 250);

    location.href = url.href;
})

document.getElementById("price2").addEventListener("click", () => {
    url.searchParams.set("min", 250);
    url.searchParams.set("max", 500);

    location.href = url.href;
})

document.getElementById("price3").addEventListener("click", () => {
    url.searchParams.set("min", 500);
    url.searchParams.set("max", 1000);

    location.href = url.href;
})

document.getElementById("price4").addEventListener("click", () => {
    url.searchParams.set("min", 1000);
    url.searchParams.set("max", 2500);

    location.href = url.href;
})

document.getElementById("price5").addEventListener("click", () => {
    url.searchParams.set("min", 2500);
    url.searchParams.set("max", 10000);

    location.href = url.href;
})

const maxUrlParam = parseInt(url.searchParams.get("max"));

if (maxUrlParam == 250) {
    document.getElementById("price1").style.backgroundColor = "#4a7cff";
} else if (maxUrlParam == 500) {
    document.getElementById("price2").style.backgroundColor = "#4a7cff";
} else if (maxUrlParam == 1000) {
    document.getElementById("price3").style.backgroundColor = "#4a7cff";
} else if (maxUrlParam == 2500) {
    document.getElementById("price4").style.backgroundColor = "#4a7cff";
} else if (maxUrlParam == 10000) {
    document.getElementById("price5").style.backgroundColor = "#4a7cff";
}
