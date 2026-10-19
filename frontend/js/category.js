// create a null id
let current_id = null

// display the form data 
const category_table = document.getElementById("table_body")
async function load_category_data() {
    category_table.innerHTML = ""
    try {
        const request = await authenticateFetch(`${BASE_URL}api/categories/`, {
            methodS : "GET",
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            response.forEach(category => {
                const tr = document.createElement("tr")
                tr.innerHTML = `
                <td>${category.category_name}</td>
                <td>${category.category_description}</td>
                <td><button data-id="${category.id}" class="edit_button">Edit</button></td>
                `

                category_table.append(tr)
            });
        }else{
            console.log(`Error Ftching the data from the backend ${error}`)
        }
    } catch (error) {
        console.error(error)
    }
}

// check if the user is a manager or admin
let check_rows = ['Manager', "Admin", "Super_Admin"]
const category_form = document.getElementById("category_form")
const add_category = document.getElementById("add_category")
add_category.addEventListener("click", (e) => {
    e.preventDefault()
    e.stopPropagation()
    if(!check_rows.includes(user_role)){
        alert(`You role of ${user_role} does not have permission to perform this action`)
        return
    }
    category_form.style.display = "block"
    document.querySelector(".form_title").textContent = "Add Catgory"
    document.querySelector("#create_category").textContent = "Create Category"
})

// lets enable a cancle event 
const cancle_button = document.getElementById("cancle_category")
cancle_button.addEventListener("click",() => {
    category_form.style.display = "none"
    category_form.reset()

})

// to update a category capture the information form the table
if(category_table){
    category_table.addEventListener("click", async function (e) {
        if(e.target.classList.contains('edit_button')){
            if(!check_rows.includes(user_role)){
                alert(`Your role of ${user_role} does not allow you to perfrom this action`)
            }
            let category_id = e.target.getAttribute("data-id")
            current_id = category_id
            // populate the form again 
            let row = e.target.closest("tr")
            let category_name = row.children[0].textContent
            let category_decription = row.children[1].textContent

            document.getElementById("category_name").value = category_name
            document.getElementById("category_description").value = category_decription

            category_form.style.display = "block"
            document.querySelector(".form_title").textContent = "Edit Catgory"
            document.querySelector("#create_category").textContent = "Edit"

        }
    })
}


// now create a post and get request
if(category_form){
    category_form.addEventListener("submit", async function (e) {
        e.preventDefault()
        const category_name = document.getElementById("category_name").value
        const category_description = document.getElementById("category_description").value
    
        if(!category_name){
            alert("Category name is required")
            return
        }
    
        let is_updating = current_id != null
        method = is_updating ? "PATCH" : "POST"
        url = is_updating ? `api/categories/${current_id}` : "api/categories/"
    
        try{
            const request = await authenticateFetch(`${BASE_URL}${url}`, {
                methods : method,
                headers : {
                    "Content-Type" : "application/json"
                },
                credentials : "include",
                body : JSON.stringify({ category_name, category_description})
            })
            const response = await request.json()
            if(request.ok){
                console.log(response)
                alert(is_updating ? `Category updated successfully` : `New Category has been added successfully`)
                category_form.style.display = "none"
                category_form.reset()
                current_id = null 
    
                document.querySelector(".form_title").textContent = "Add Catgegory"
                document.querySelector("#create_category").textContent = "Create Category"
    
                load_category_data()
            }else{
                console.log(is_updating ? `Error updating category ${response}` : `Error creating category ${response}`)
            }
        }catch(error){
            console.error(error)
        }
    })
}

document.addEventListener("DOMContentLoaded", () =>{
    load_category_data()
})