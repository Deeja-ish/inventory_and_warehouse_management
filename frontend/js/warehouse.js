current_id = null
// display the warehosue type options
const warehouse_type = document.getElementById("warehouse_type")
async function load_warehouse_type(){
    warehouse_type.innerHTML = ''
    try{
        const request = await authenticateFetch(`${BASE_URL}api/warehouse_types/`, {
            method : "GET",
            credentials : "include"
        })
        const response = await request.json()
        warehouse_type.innerHTML = `<option value ="">Choose the type of warehouse</option>`
        if(request.ok){
            console.log(response)
            response.forEach(type =>{
                const option = document.createElement("option")
                option.value = type[0]
                option.textContent = type[1]

                warehouse_type.appendChild(option)
            })
        }else{
            console.log(response)
        }
    }catch(error){
        console.error(error)
    }
}

// populate the capacity type value
const capacity_unit = document.getElementById("capacity_unit")
async function load_capacity_unit(){
    capacity_unit.innerHTML = ""
    try{
        const request = await authenticateFetch(`${BASE_URL}api/capacity_types/`, {
            method : "GET",
            credentials : "include"
        })
        const response = await request.json()
        capacity_unit.innerHTML = "<option value=''> Choose a unit </option>"
        if(request.ok){
            response.forEach(capacity =>{
                const option = document.createElement("option")
                option.value = capacity[0]
                option.textContent = capacity[1]

                capacity_unit.appendChild(option)
            })
        }else{
            console.log("Error fetching the capacity details", response)
        }
    }catch(error){
        console.log(error)
    }
}

// display the available managers from the company 
const manager_company = document.getElementById("manager")
async function load_manager(){
    manager_company.innerHTML = ""
    try {
        const request = await authenticateFetch(`${BASE_URL}api/users/get_manager/`, {
            method : "GET",
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            response.forEach(manager => {
                const option = document.createElement("option")
                option.value = manager.id
                option.textContent = `${manager.username} - ${manager.role} - ${manager.company}`
                manager_company.appendChild(option)
            })
        }else{
            console.log(response)
        }
        
    } catch (error) {
        console.error(error)
    }
}


// lets get and display the warehouse table data 
const table_body = document.getElementById("warehouse_table")
async function load_warehouse(){
    table_body.innerHTML = ""
    try{
        const request = await authenticateFetch(`${BASE_URL}api/warehouses/`, {
            method : "GET", 
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            response.forEach(warehouse=> {
                const tr = document.createElement("tr")
                tr.innerHTML = `
                <td>${warehouse.warehouse_name}</td>
                <td>${warehouse.warehouse_code}</td>
                <td>${warehouse.city || "Not Provided"}</td>
                <td>${warehouse.address || "Not Provided"} </td>
                <td>${warehouse.state || "Not Provided"}</td>
                <td>${warehouse.country || "Not Provided"}</td>
                <td>${warehouse.warehouse_type}</td>
                <td>${warehouse.manager}</td>
                <td>${warehouse.capacity}</td>
                <td>${warehouse.capacity_unit}</td>
                <td><button data-id=${warehouse.id} class="edit_button">Edit</button></td>
                `
                table_body.appendChild(tr)
            });
        }else{
            console.log("Error getting the warehouse data", response)
        }
    }catch(error){
        console.error(error)
    }
}

// ensure that someone is allowed to open the form 
let form = document.getElementById("warehouse_form")
let add_warehouse = document.getElementById("add_warehouse")
let allowed_role = ['Manager', "Admin", "Store_keeper"]
add_warehouse.addEventListener("click", (e) => {
    e.preventDefault()
    e.stopPropagation()
    if(!user_role || !allowed_role.includes(user_role)){
        alert(`Your role of ${user_role} does not allow you to perform this action`)
        return
    }
    form.style.display = "block"
    document.getElementById("warehouse_title").textContent = "Add Warehosue"
    document.querySelector("#warehouse_form button[type='submit']").textContent = "Submit"
})

// creat an update filter that fills the form 
if(table_body){
    table_body.addEventListener("click", (e) => {
        if(e.target.classList.contains("edit_button")){
            if(allowed_role.includes(user_role)){
                let warehosue_id = e.target.getAttribute("data-id")
                current_id = warehosue_id
    
                // get the data from the table and display in the form
                let row = e.target.closest("tr")
                let warehosue_name = row.children[0].textContent
                let city = row.children[2].textContent
                let address = row.children[3].textContent
                let state = row.children[4].textContent
                let country = row.children[5].textContent
                let warehouse_type = row.children[6].textContent
                let manager = row.children[7].textContent
                let capacity = row.children[8].textContent
                let capacity_unit = row.children[9].textContent

                document.getElementById("warehouse_name").value = warehosue_name
                document.getElementById("city").value = city
                document.getElementById("address").value =address
                document.getElementById("state").value = state
                document.getElementById("country").value = country 
                document.getElementById("warehouse_type").value = warehouse_type,
                document.getElementById("manager").value = manager
                document.getElementById("capacity").value = capacity 
                document.getElementById("capacity_unit").value = capacity_unit

                // display the form and change the header 
                form.style.display = "block"
                document.getElementById("warehouse_title").textContent = "Update Warehouse"
                document.querySelector("#warehouse_form button[type ='submit']").textContent = "Update"
            }
        }else{
            alert(`Your role of ${user_role} does not allow you to perform this action.`)
            return
        }

    })
}

// create a cancle event 
const cancle_button = document.getElementById("cancle_button")
cancle_button.addEventListener("click", () => {
    form.style.display = "none"
    form.reset()
})

// create the create and update warehouse
if(form){
    load_capacity_unit()
    load_warehouse_type()
    load_manager()
    form.addEventListener("submit", async function (e) {
        e.preventDefault()


        const warehouse_name = document.getElementById("warehouse_name").value
        const city = document.getElementById("city").value
        const address = document.getElementById("address").value
        const warehouse_type = document.getElementById("warehouse_type").value
        const state = document.getElementById("state").value
        const country = document.getElementById("country").value
        const manager = document.getElementById("manager").value
        const capacity = document.getElementById("capacity").value
        const capacity_unit = document.getElementById("capacity_unit").value

        let is_updating = current_id != null
        method = is_updating ? "PATCH" : "POST"
        url = is_updating ? `api/warehouses/${current_id}/` :  `api/warehouses/`

        if(!warehouse_name || !manager ||! warehosue_type){
            alert("Name and manager are required fields")
            return 
        }
        const request = await authenticateFetch(`${BASE_URL}${url}`, {
            method : method,
            headers : {
                "Content-Type" : "application/json"
            },
            body : JSON.stringify({
                warehouse_name, city, address, state, country, manager, warehouse_type, capacity, capacity_unit
            }),
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            alert(is_updating ? `Warehouse deatails updated successfully` : `New warehouse created`)

            form.style.display = "none"
            form.reset()
            current_id = null
            load_warehouse()
        }else{
            console.log(is_updating ? `Error updating warehouse` : `Error creating new warehosue`, response )
        }
    })
}


document.addEventListener("DOMContentLoaded", () => {
    load_capacity_unit()
    load_manager()
    load_warehouse_type()
    load_warehouse()
})