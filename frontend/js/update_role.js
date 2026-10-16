// create a function to populate the user dropdown
const select_user = document.getElementById("select_user")
async function load_users() {
    try{
        const request = await authenticateFetch(`${BASE_URL}api/users/`, {
            method : "GET",
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            select_user.innerHTML = "<option> Choose an employee </option>"
            response.forEach(user => {
                const option = document.createElement("option")
                option.value = user.id
                option.textContent = `${user.first_name} ${user.last_name} - ${user.employee_ID}`
    
                select_user.appendChild(option)
            });   
        }else{
            console.log(`Error fetching the list of users ${response}`)
        }
    }catch(error){
        console.error(error)
    }
}

// display the result
async function display_user(event) {
    const selected_user = event.target.value
    const user_details = document.getElementById("user_details")
    if(!selected_user){
        user_details.style.display = "none";
        return
    }
    try{
        const request = await authenticateFetch(`${BASE_URL}api/users/${selected_user}/`, {
            method : "GET",
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){ 
            console.log(response)
            document.getElementById("detail_employee_id").textContent = response.employee_ID
            document.getElementById("detail_username").textContent = response.username
            document.getElementById("detail_first_name").textContent = response.first_name
            document.getElementById("detail_last_name").textContent = response.last_name
            document.getElementById("detail_company").textContent = response.company
            document.getElementById("detail_current_role").textContent = response.role

            // display the form 
            user_details.style.display = "block";
            
        }else{
            console.log(response)
        }
    }catch(error){
        console.error(error)
    }
}

// show the display of role
const get_role = document.getElementById("choose_role")
async function load_role(){
    get_role.innerHTML = ""
    try {
        const request = await authenticateFetch(`${BASE_URL}api/get_roles/`, {
            method : "GET",
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            get_role.innerHTML = "<option value=''> Choose a role </option>"
            response.forEach(role => {
                const option = document.createElement("option")
                option.value = role[0]
                option.textContent = role[1]

                get_role.appendChild(option)
            })
        }else{
            console.log(`Error fetching response dropdown ${response}`)
        }
    } catch (error) {
        console.error(error)
    }
}

// make the user details show when selected
document.addEventListener("DOMContentLoaded", () => {
    load_users()
    load_role()
    select_user.addEventListener("change", display_user) 
})

// create a request to post the new role 
const update_form = document.getElementById("update_form")
update_form.addEventListener("submit", async function (e) {
    e.preventDefault()
    const selected_user = select_user.value
    const new_role = document.getElementById("choose_role").value
    const response_message = document.getElementById("response_message")
    if(!new_role){
        alert("A role must be provided")
        return
    }
    if(!selected_user){
        alert("User must be provided")
        return
    }
    response_message.innerHTML = ""

    try {
        const request = await authenticateFetch(`${BASE_URL}api/users/${selected_user}/update_role/`, {
            method : "PATCH", 
            headers : {
                "Content-Type" : "application/json"
            },
            body : JSON.stringify({"role" : new_role}),
            credentials : "include"
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            response_message.innerHTML = `
            <p class='success_message'> User status has been updated successfully</p>
            `
            document.getElementById("detail_current_role") = new_role
            // set a time out 
            setTimeout(() => {
                window.location.href = "dashboard.html"
            }, 5000)
        }else{
            console.log("Error Updating user role", response)
            alert("error updating role")
        }
    } catch (error) {
        console.error("Network error retrieving user", error)
    }
})

