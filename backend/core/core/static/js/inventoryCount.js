let count = 0;
let countItemsResult;

export async function getCount() {
    if (countItemsResult) {
        return countItemsResult;
    }

    const requestOptions = {
      method: "GET",
    };

    const response = await sendRequest(
        `http://localhost/products/inventory/count/`,
        requestOptions
    );

    if (!response.ok) {
        return '-'
    }

    const result = await response.json();

    countItemsResult = result;

    return result;
}

window.getCount = getCount;
