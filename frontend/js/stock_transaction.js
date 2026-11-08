// display the products warehosue and transaction_type
// get the product name 
// load all filter varaibales 
const filter_warehouse = document.getElementById("filter_warehouse")
const warehouse_name = document.getElementById("warehouse_name")
async function load_warehouse(){
    warehouse_name.innerHTML = ""
    filter_warehouse.innerHTML = "<option value=''>All warehouse</option>"
    try {
        const request = await authenticateFetch(`${BASE_URL}api/warehouses/`, {
            method : "GET",
            credentials : "include"
        })
        const response = await request.json()
        warehouse_name.innerHTML = "<option value=''>Choose a warehouse</option>"
        if(request.ok){
            console.log(response)
            response.forEach(warehouse => {
                const option = document.createElement("option")
                option.value = warehouse.id
                option.textContent = warehouse.warehouse_name

                warehouse_name.appendChild(option)
                const filter_option = option.cloneNode(true)
                filter_warehouse.appendChild(filter_option)
            });
        }else{
            console.log("Error fetching the warehosue name", response)
        }
    } catch (error) {
        console.error(error)
    }
}

// load the products 
const filter_product = document.getElementById("filter_product")
const product_name = document.getElementById("product_name")
async function load_products(){
    product_name.innerHTML = ""
    filter_product.innerHTML = "<option value=''>All Products</option>"
    try {
        const request = await authenticateFetch(`${BASE_URL}api/products/`, {
            method : "GET",
            credentials : "include"
        })
        const response = await request.json()
        product_name.innerHTML = "<option value= ''> Choose the product Name</option>"
        if(request.ok){
            console.log(response)
            response.forEach(product => {
                const option = document.createElement("option")
                option.value = product.id
                option.textContent = product.product_name

                product_name.appendChild(option)
                const filter_option = option.cloneNode(true)
                filter_product.appendChild(filter_option)
            });
        }else{
            console.log("error fetching the warehosue name", response)
        }
    } catch (error) {
        console.error(error)
    }
}

// load the transaction type
const filter_transaction_type = document.getElementById("filter_transaction_type")
const stock_type = document.getElementById("transaction_type")
async function load_stock_type(){
    stock_type.innerHTML = ""
    filter_transaction_type.innerHTML = "<option value=''>All Type</option>"
    try {
        const request = await authenticateFetch(`${BASE_URL}api/stock_type/`, {
            method : "GET",
            credentials : "include"
        })
        const response = await request.json()
        stock_type.innerHTML = "<option value=''> Choose the type of transaction to perform</option>"
        if(request.ok){
            console.log(response)
            response.forEach(type => {
                const option = document.createElement("option")
                option.value = type[0]
                option.textContent = type[1]

                stock_type.appendChild(option)
                const filter_option = option.cloneNode(true)
                filter_transaction_type.appendChild(filter_option)
            });
        }else{
            console.log("error fetching the transaction type", response)
        }
    } catch (error) {
        console.error(error)
    }
}

// fetch the data to diplay in the tables
let stock_table = document.getElementById("stock_table")
async function load_table() {
    stock_table.innerHTML = ""

    // append the given values to params
    let params = new URLSearchParams
    if(filter_warehouse && filter_warehouse.value){
        params.append("warehouse", filter_warehouse.value)
    }
    if(filter_product && filter_product.value){
        params.append("product", filter_product.value)
    }
    if(filter_transaction_type && filter_transaction_type.value){
        params.append("transaction_type", filter_transaction_type.value)
    }
    const query_param = params.toString() ? `?${params.toString()}` : "";
    try {
        const request = await authenticateFetch(`${BASE_URL}api/stock_transactions/${query_param}`, {
            method : "GET",
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            response.forEach(stock => {
                const formated_data = stock.created_at ? new Date(stock.created_at).toLocaleString("en-GB", {
                    year : "numeric",
                    month : "short",
                    day : "2-digit"
                }) : "N/A"

                const tr = document.createElement("tr")
                tr.innerHTML = `
                <td>${stock.warehouse}</td>
                <td>${stock.product}</td>
                <td>${stock.transaction_type}</td>
                <td>${stock.quantity_before}</td>
                <td>${stock.quantity_after}</td>
                <td>${stock.quantity}</td>
                <td>${stock.reason}</td>
                <td>${formated_data}</td>
                <td><button data-id='${stock.id}' class="edit_button">Edit</button></td>
                `
                stock_table.appendChild(tr)
            })
        }else{
            console.log("error fetching the stock details", response)
        }
    } catch (error) {
        console.error(error) 
    }
}

[filter_warehouse, filter_product, filter_transaction_type].forEach(select => {
    if(select){
        select.addEventListener("change", () => load_table())
    }
})
// allow only selected members to create a transaction 
const add_stock_button = document.getElementById("transfer_stock")
let stock_transaction_form = document.getElementById("stock_transaction_form")
let allowed_role = ['Admin', "Super_Admin", "Manager", "Store_keeper"]
add_stock_button.addEventListener("click", () => {
    if(!allowed_role.includes(user_role) || !user_role){
        alert(`Your role of ${user_role} does not allow you to perform this action`)
        return
    }
    stock_transaction_form.style.display = "block"
})

let cancle_button = document.getElementById("cancle_button")
cancle_button.addEventListener("click", () => {
    stock_transaction_form.reset()
    stock_transaction_form.style.display = "none"
})

// update the table for edit
if(stock_transaction_form){
    load_products()
    load_stock_type()
    load_warehouse()
    stock_transaction_form.addEventListener("submit", async function (e) {
        e.preventDefault()

        const product = document.getElementById("product_name").value
        const warehouse = document.getElementById("warehouse_name").value
        const transaction_type = document.getElementById("transaction_type").value
        const quantity = document.getElementById("quantity").value
        const reason = document.getElementById("reason").value

        try{
            if(!product || !warehouse || !transaction_type || !quantity){
                alert("product, warehosue, transaction_type and quantity are required fields")
                return
            }
            const request = await authenticateFetch(`${BASE_URL}api/stock_transactions/`, {
                method : "POST",
                credentials : "include",
                headers : {
                    "Content-Type" : "application/json"
                },
                body : JSON.stringify({product, warehouse, transaction_type, quantity, reason})
            })
            const response = await request.json()
            if(request.ok){
               console.log(response)
               alert("New Stock Transaction has been added successfully") 
               load_table()
            }else{
                console.log("Error creating new stock", response)
            }
        }catch(error){
            console.error(error)
        }

    })
}

document.addEventListener("DOMContentLoaded", () => {
    load_table()
    load_products()
    load_stock_type()
    load_warehouse()
})

