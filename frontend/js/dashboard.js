// create the summary endpoint to show products aggregrates 
let products_display = document.getElementById("product_total")
async function show_products() {
    products_display.innerHTML = ""
    try{
        const request = await authenticateFetch(`${BASE_URL}api/products/summary/`, {
            method : 'GET',
            headers : {
                'Content-Type' : "application/json"
            },
            credentials : "include",
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            response.total_products !== 0 ? products_display.innerHTML = response.total_products : products_display.innerHTML = '0' 
        }else{
            console.log("Error fetching total products count", response)
        }
    }catch(error){
        console.error(error)
    }

}

// create the inventory_display
let inventory_display = document.getElementById("inventory_total")
async function show_inventory() {
    inventory_display.textContent = ""
    try{
        const request = await authenticateFetch(`${BASE_URL}api/inventories/summary/`, {
            method : "GET",
            headers : {
                "Content-Type" : "application/json"
            },
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            response.total_inventory !== 0 ? inventory_display.textContent = response.total_inventory : inventory_display.textContent = 0
        }else{
            console.log(`Error fetching the total inventory Counts`, response)
        }
    }catch(error){
        console.error(error)
    }
}

// create the warehouse count
let warehouse_display = document.getElementById("warehouse_total")
async function show_warehouse() {
    warehouse_display.textContent = ""
    try {
        const request = await authenticateFetch(`${BASE_URL}api/warehouses/summary/`, {
            method: "GET",
            headers : {
                "Content-Type" : "application/json"
            },
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            response.total_warehouse !== 0 ? warehouse_display.textContent = response.total_warehouse : warehouse_display.textContent = 0 
        }else{
            console.log("Error fetching the warehouse count")
        }
    } catch (error) {
        console.error(error)
    }
}

// create the lowstock count 
let lowstock_display = document.getElementById("low_stock_summary")
async function show_lowstock(){
    lowstock_display.textContent = ""
    try {
        const request = await authenticateFetch(`${BASE_URL}api/inventories/low_stock/`, {
            method : "GET",
            headers : {
                "Content-Type" : "application/json"
            },
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            const count = response.length ? response.length : 0
            lowstock_display.textContent = count
        }else{
            console.log("Error fetching the low stock count", response)
        }
    } catch (error) {
        console.error(error)
    }
}

// show the recent transaction history 
let transaction_details = document.getElementById("transaction_body")
async function show_transaction_history(){
    transaction_details.innerHTML = ""
    try {
        const request = await authenticateFetch(`${BASE_URL}api/stock_transactions/`, {
            method : "GET",
            headers :{
                "Content-Type" : "application/json"
            },
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            let top_warehouse = response.slice(0, 3)
            console.log(top_warehouse)
            top_warehouse.forEach(transaction => {
                const tr = document.createElement("tr")

                tr.innerHTML = `
                <td>${transaction.product}</td>
                <td>${transaction.warehouse}</td>
                <td>${transaction.transaction_type}</td>
                <td>${transaction.quantity}</td>
                <td>${transaction.created_at}</td>
                `
                transaction_details.appendChild(tr)
            });
    
        }else{
            console.log("Error fetching response", response)
        }
    } catch (error) {
        console.error(error)
    }
}

document.addEventListener("DOMContentLoaded", ()=> {
    show_products(), show_inventory(), show_warehouse(), show_lowstock(), show_transaction_history()
})

// get the update role to change on checking ths user status 
const update_role_form = document.getElementById("update_role_form")

update_role_form.addEventListener("click", async function (e) {
    let allowed_role = ['Manager', 'Admin', "Super_Admin"]

    if(!allowed_role.includes(user_role)){
        e.preventDefault()
        e.stopPropagation()
        alert("Your role of " + user_role + " Does not allow you to perform this action.")
        return
    }
    window.location.href = "update_role.html"
})