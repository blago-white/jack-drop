const table = document.getElementById('game-history-table');
const empty = document.getElementById('empty-hist');

const gamesMapping = {
    "U": "Upgrade",
    "C": "Contract",
    "B": "Battle",
    "M": "Mines"
};

async function getHistory() {
    const response = await fetch("/products/games/history/1/");

    if (!response.ok) {
        alert('Error with history')
        return
    }

    const result = await response.json();

    if (!result.length) {
        empty.style.display = 'flex';
    } else {
        table.style = "";
        let c = 0;

        result.forEach((element) => {
            c++;

            html = `
            <li>
                <span class="game-num">${c}</span>
                <span class="game-name">${gamesMapping[element.game]}</span>
            `;

            if (!element.related_item_first) {
                html += `
                    <span class="is-win true"></span>
                `
            } else if (!(element.related_item_second || element.related_case)) {
                html += `
                    <span class="item-img"><img src="${element.related_item_first.image_path}"></span>
                    <span class="is-win ${element.is_win}"></span>
                `
            } else if (element.related_item_second) {
                html += `
                    <span class="case-drop-items">
                        <span class="case-img"><img src="${element.related_item_first.image_path}"></span>
                        <span class="item-img"><img src="${element.related_item_second.image_path}"></span>
                    </span>
                    <span class="is-win ${element.is_win}"></span>
                `
            } else if (element.related_case) {
                html += `
                    <span class="case-drop-items">
                        <span class="case-img"><img src="${element.related_case.image_path}"></span>
                        <span class="item-img"><img src="${element.related_item_first.image_path}"></span>
                    </span>
                    <span class="is-win ${element.is_win}"></span>
                `
            }

            table.innerHTML += `${html}</li>`;
        });
    }
}

getHistory();
