const inputLeft = document.getElementById("pri");
const inputRight = document.getElementById("pri2");
const inputedPrice1 = document.getElementById("range-price-1");
const inputedPrice2 = document.getElementById("range-price-2");

const url = new URL(document.location.href);

let leftValue = parseInt(inputLeft.value);
let rightValue = parseInt(inputRight.value);

function changeInputedPrice(event, iid) {
    if (iid == "l") {
        leftValue = Number(inputLeft.value);
        inputedPrice1.innerHTML = `${leftValue} ₽`;

        if (leftValue > rightValue) {
            rightValue = leftValue;
            inputedPrice2.innerHTML = `${leftValue} ₽`;
            inputRight.value = inputLeft.value;
        }
    } else {
        rightValue = Number(inputRight.value);
        inputedPrice2.innerHTML = `${rightValue} ₽`;

        if (leftValue > rightValue) {
            leftValue = rightValue;
            inputedPrice1.innerHTML = `${leftValue} ₽`;
            inputLeft.value = inputRight.value;
        }
    }

    return [leftValue, rightValue];
}

function reload() {
    changed = changeInputedPrice();

    url.searchParams.set("min", changed[0]);
    url.searchParams.set("max", changed[1]);

    location.href = url.href;
}

inputLeft.addEventListener("input", (e) => {
    changeInputedPrice(e, "l")
})

inputRight.addEventListener("input", (e) => {
    changeInputedPrice(e, "r")
})

inputLeft.addEventListener("change", (e) => {
    reload()
})

inputRight.addEventListener("change", (e) => {
    reload()
})
