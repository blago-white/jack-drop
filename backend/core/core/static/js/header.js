const headerButton = document.getElementById('menu-btn');
const header = document.getElementById('header');
let toggled = false;

function toggleMenu(event) {
    header.style.minHeight = toggled ? "9.25vh" : "calc(100vw*calc(450/960))";

    setTimeout(() => {
        if (toggled) {
            document.getElementById('header').appendChild(document.getElementById('navbar'));
            document.getElementById('navbar').style.maxHeight = "100%";
            document.getElementById('navbar').style.maxWidth = "100%";
            document.getElementById('navbar').style.display = "flex";
            document.getElementById('menu-btn').classList.toggle('sandwich-menu-tggled');
        } else {
            document.getElementById('navbar').style.maxHeight = "0%";
            document.getElementById('navbar').style.maxWidth = "0%";
            document.getElementById('navbar').style.display = "none";

            document.getElementById('menu-btn').classList.toggle('sandwich-menu-tggled');
        }
    }, 0.2)

    toggled = !toggled;
}

headerButton.addEventListener("click", toggleMenu);
