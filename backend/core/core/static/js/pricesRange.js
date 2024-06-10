const inputLeft = document.getElementById("pri");
const inputRight = document.getElementById("pri2");
const inputedPrice1 = document.getElementById("range-price-1");
const inputedPrice2 = document.getElementById("range-price-2");

let leftValue = 0;
let rightValue = 5000;

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

    console.log(leftValue, rightValue);
}

inputLeft.addEventListener("input", (e) => {
    changeInputedPrice(e, "l")
})

inputRight.addEventListener("input", (e) => {
    changeInputedPrice(e, "r")
})