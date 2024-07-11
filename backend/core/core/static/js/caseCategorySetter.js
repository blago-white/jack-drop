function setCaseCategory() {
    const url = new URL(document.location.href);

    let category = document.getElementById('cat-name').value;

    category = category[0].toUpperCase() + category.substring(1);

    url.searchParams.set("cat", category);

    location.href = url.href;

    return false;
}