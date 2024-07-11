const headerButton = document.getElementById('menu-btn');
const header = document.getElementById('header');
let toggled = false;

function toggleMenu(event) {
    header.style.minHeight = toggled ? "9.25vh" : "46.875vw";

    document.getElementById('menu-btn').classList.toggle('sandwich-menu-tggled');

    if (!toggled) {
        document.getElementById('header').appendChild(document.getElementById('navbar'));
        document.getElementById('header').appendChild(document.getElementById('lang-switch'));
        document.getElementById('header').style.paddingBottom = '7ch';
        document.getElementById('navbar').style.display = "none";
        document.getElementById('navbar').style.maxHeight = "100%";
        document.getElementById('navbar').style.maxWidth = "100%";
    } else {
        console.log("switch");
        document.getElementById('navbar').style.maxHeight = "0vh";
        document.getElementById('navbar').style.maxWidth = "0%";
        document.getElementById('lang-switch').style.display = "none";
    }

    setTimeout(() => {
        if (toggled) {
            document.getElementById('navbar').style.display = "flex";
            document.getElementById('lang-switch').style.display = "flex";
        } else {
            console.log("tim");
            document.getElementById('navbar').style.display = "none";
            document.getElementById('main-part-h').appendChild(document.getElementById('navbar'));
            document.getElementById('main-part-h').appendChild(document.getElementById('lang-switch'));
            document.getElementById('header').style.paddingBottom = '0ch';
        }
    }, 200)

    toggled = !toggled;
}

headerButton.addEventListener("click", toggleMenu);
