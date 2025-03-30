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