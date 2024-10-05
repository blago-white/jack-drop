const arrow = document.getElementById("nav-arrow");

let top_direction_scroll = false;

arrow.addEventListener("click", () => {window.scrollTo({
    top: top_direction_scroll ? 0 : document.body.scrollHeight,
    behavior: 'smooth'
})});

function updateArrow(e) {
    if (((document.body.clientHeight - window.innerHeight) - window.pageYOffset) < ((document.body.clientHeight - window.innerHeight) / 2)) {
        if (!arrow.classList.contains("up")) {
            arrow.style.opacity = "0";
            top_direction_scroll = true;

            setTimeout(() => {
                arrow.style.opacity = "1";
                arrow.classList.add("up");
            }, 200)
        }
    } else {
        if (arrow.classList.contains("up")) {
            arrow.style.opacity = "0";
            top_direction_scroll = false;

            setTimeout(() => {
                arrow.style.opacity = "1";
                arrow.classList.remove("up");
            }, 200)
        }
    }
}


if (document.body.clientHeight / window.innerHeight > 1.5) {
    document.addEventListener("scroll", updateArrow)
} else {
    let heightBefore = document.body.clientHeight;
    arrow.style.opacity = "0";

//    while (true) {
//        if ((heightBefore != document.body.clientHeight) && (document.body.clientHeight / window.innerHeight > 1.5)) {
//            arrow.style.opacity = "1";
//            document.addEventListener("scroll", updateArrow)
//            break;
//        }
    setTimeout(() => {
        if ((heightBefore != document.body.clientHeight) && (document.body.clientHeight / window.innerHeight > 1.5)) {
            arrow.style.opacity = "1";
            document.addEventListener("scroll", updateArrow)
        }
    }, 5000)
}
