// create a function to show the inventory table
const inventory_table = document.getElementById("inventory_table")
async function display_table() {

    inventory_table.innerHTML = ""
    try{
        const request = await authenticateFetch(`${BASE_URL}api/inventories/`, {
            method : "GET",
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            response.forEach(inventory => {
                const tr = document.createElement('tr')
                tr.innerHTML = `
                <td>${inventory.product_name}</td>
                <td>${inventory.warehouse_name}</td>
                <td>${inventory.available_quantity}</td>
                <td>${inventory.reserved_quantity}</td>
                <td>${inventory.reorder_level}</td>
                <td>${inventory.stock_status}</td>
                `
                inventory_table.appendChild(tr)
            });
    
        }
    }catch(error){
        console.error(`Error ${error}}`)
    }
}

document.addEventListener("DOMContentLoaded", () => {
    display_table()
})