let count = 0;

async function getCount() {

    const requestOptions = {
      method: "GET",
    };

    const response = await fetch(
        `http://localhost/products/inventory/count/`,
        requestOptions
    );

    if (!response.ok) {
        return '-'
    }

    const result = await response.json();

    console.log(result);

    return result.count;
}
