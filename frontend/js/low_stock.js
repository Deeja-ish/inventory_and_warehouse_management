const low_stock = document.getElementById("low_stock_table")

async function load_low_stock(){
    low_stock.innerHTML = ""
    try {
        const request = await authenticateFetch(`${BASE_URL}api/inventories/low_stock/`, {
            method : "GET",
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            response.forEach(stock => {
                const tr = document.createElement("tr")
                tr.innerHTML = `
                <td>${stock.product_name}</td>
                <td>${stock.warehouse_name}</td>
                <td>${stock.available_quantity}</td>
                <td>${stock.reorder_level}</td>
                <td>${stock.stock_status}</td>
                `
                low_stock.appendChild(tr)
            });
        }
    } catch (error) {
        console.error(`Error ${response.error}`)
    }
}

document.addEventListener("DOMContentLoaded", () => {
    load_low_stock()
})