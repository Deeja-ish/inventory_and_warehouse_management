// create a null varaible for an id
let currentId = null

// create afunction to display the catgeory values 
const category = document.getElementById("category")
async function load_category() {
    category.innerHTML = ""
    category.innerHTML = "<option value=''> Choose Catgeory </option>"
    try {
        const request = await authenticateFetch(`${BASE_URL}api/categories/`, {
            method : "GET",
            credentials : "include"
    
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            response.forEach(cat => {
                const option = document.createElement("option")
                option.value = cat.id 
                option.textContent = cat.category_name

                category.appendChild(option)
            });
        }else{
            console.log('Error fetching the category', response)
        }
    } catch (error) {
        console.error(error)
    }
}

// create a function to display the product type 
const product_type = document.getElementById("product_type")
async function load_product_type() {
    product_type.innerHTML = ""
    product_type.innerHTML = "<option value=''> Choose Product Type </option>"

    try {
        const request = await authenticateFetch(`${BASE_URL}api/product_type/`, {
            method : "GET",
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            response.forEach(product => {
                const option = document.createElement("option")
                option.value = product[0]
                option.textContent = product[1]

                product_type.appendChild(option)
            })
        }else{
            console.log("Error fetching the product type", response)
        }
    } catch (error) {
        console.error(error)
    }
}

// create a function to display the unit measurement
const unit_type = document.getElementById("unit_of_measure")
async function load_unit_measurment() {
    unit_type.innerHTML = ""
    unit_type.innerHTML = "<option value=''> Choose a unit measurment</option>"

    try {
        const request = await authenticateFetch(`${BASE_URL}api/unit_type/`, {
            method : "GET",
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            response.forEach(unit => {
                const option = document.createElement("option")
                option.value = unit[0]
                option.textContent = unit[1]

                unit_type.appendChild(option)
            })
        }else{
            console.log("Error fetching the unit measurment", response)
        }
    } catch (error) {
        console.error(error)   
    }
}


// show the form when the button is clicked 
// display the form base on user's role
const add_product_form = document.getElementById("add_product_form")
const cancle_button = document.getElementById("cancle_button")
let product_create_roles = ['Manager', "Super_Admin", "Store_Keeper", "Admin"]
document.getElementById("add_product").addEventListener("click", async function (e) {
    e.preventDefault()
    e.stopPropagation()
    
    if(!product_create_roles.includes(user_role)){
        alert("Your role of " + user_role + " does not allow you to perform this action")
        return
    }
    add_product_form.style.display = "block"
    cancle_button.style.display = "block"
})

cancle_button.addEventListener("click", async function () {
    add_product_form.style.display = "none"
    add_product_form.reset()
    currentId = null

    document.querySelector(".product_header").textContent = "Add Product"
    document.querySelector("#create_button").textContent = "Create Product"
})

// create a function to show the products in a table
const products_table = document.getElementById("product_type_body")
async function load_products_table() {
    products_table.innerHTML = ""
    try {
        const request = await authenticateFetch(`${BASE_URL}api/products/`, {
            method : "GET",
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            response.forEach(product => {
                const tr = document.createElement("tr")
                tr.innerHTML = `
                <td>${product.product_name}</td>
                <td>${product.category}</td>
                <td>${product.sku}</td>
                <td>${product.product_type}</td>
                <td>${product.unit_of_measure}</td>
                <td>${product.product_description || "Not Provided"}</td>
                <td>${product.reorder_level || "Not Provided"}</td>


                <td><button class="edit_button" data-id=${product.id} data-category=${product.category}>Edit</button></td>
                `
                products_table.appendChild(tr)
            })
        }else{
            console.log(`Error fetching the companies products`)
        }
    } catch (error) {
        console.error(error)
    }
}

// create a function that will populate the table for an update request 
if(products_table){
    products_table.addEventListener("click", async function (e) {
        if(e.target.classList.contains("edit_button")){
            if(!product_create_roles.includes(user_role)){
                alert("Your Role of " + user_role + " does not have permission to perform this action")
                return
            }
            let product_id = e.target.getAttribute("data-id")
            currentId = product_id
            // get the old values from the product
            let row = e.target.closest("tr")
            let product_name = row.children[0].textContent
            let product_category = row.children[1].textContent
            let product_type = row.children[3].textContent
            let unit_of_measure = row.children[4].textContent
            let product_description = row.children[5].textContent
            let reorder_level = row.children[6].textContent

            // put these values back in the form 
            document.getElementById("product_name").value = product_name
            document.getElementById("category").value = product_category
            document.getElementById("product_type").value = product_type
            document.getElementById("unit_of_measure").value = unit_of_measure
            document.getElementById("product_description").value = product_description
            document.getElementById("reorder_level").value = reorder_level

            document.querySelector(".product_header").textContent = "Update Product"
            document.querySelector("#create_button").textContent = "update"

            // diplay the form 
            document.getElementById("add_product_form").style.display = "block"
            document.getElementById("cancle_button").style.display = "block"

        }
    })
}

// load all fields when the page loads 
document.addEventListener("DOMContentLoaded", () => {
    load_category(), load_product_type(), load_unit_measurment(), load_products_table()
})

// create a function to create and edit proudcts
if(add_product_form){
    load_category()
    load_product_type()
    load_unit_measurment()
    add_product_form.addEventListener("submit", async function (e) {
        e.preventDefault()
        const product_name = document.getElementById("product_name").value
        const category = document.getElementById("category").value
        const product_type = document.getElementById("product_type").value
        const unit_of_measure = document.getElementById("unit_of_measure").value
        const product_description = document.getElementById("product_description").value
        const reorder_level = document.getElementById("reorder_level").value

    
        if(!category){
            alert("Please insert a category")
            return
        }
        if(!product_name){
            alert("Product name is required")
            return 
        }
         // create and update form 
        let isUpdating = currentId != null
        let method = isUpdating ? "PATCH" : "POST"
        let url = isUpdating ? `api/products/${currentId}/` : "api/products/"

        try {
            const request = await authenticateFetch(`${BASE_URL}${url}`, {
                method : method,
                headers : {
                    "Content-Type" : "application/json"
                },
                body : JSON.stringify({
                    product_name, category, product_type, unit_of_measure, product_description, reorder_level
                }),
                credentials : "include"
            })
            const response = await request.json()
            if(request.ok){
                console.log(response)
                alert(isUpdating ? "Product has been update succesfully" : "New Product has been added")

                // hide the form 
                add_product_form.style.display = "none"
                add_product_form.reset()

                // clear the current_id 
                currentId = null
                document.querySelector(".product_header").textContent = "Add New Product"
                document.querySelector("#create_button").textContent = "Create Product"

                load_products_table()
            }else{
                console.log(isUpdating ? `Error editing product with id ${currentId}: ${response}` : "Error Creating new product", response)
            }
        } catch (error) {
            console.error(error)
        }
    })
}

// make the search bar respond
const search_content = document.getElementById("search_product")
if(search_product) {
    search_product.addEventListener("input", function(e){
        const search_value = e.target.value.toLowerCase().trim()
        const row_values = products_table.querySelectorAll()

        if(row_values){
            row_values.forEach(row =>{
                const row_text = row.textContent.toLowerCase()

                if(row_text.includes(search_value)){
                    row.style.display = ""
                }else{
                    row.style.display = "none";
                }
            })
        }
    })
}