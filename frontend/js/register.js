const BASE_URL = 'http://127.0.0.1:8000/'

async function load_company() {
    const select_company = document.getElementById("company")
    // create the route to get the 
    try{
        select_company.innerHTML = ""
        const request = await fetch(`${BASE_URL}api/list_company/`, {
            method : 'GET',
            credentials : "include"
        })
        const response = await request.json()
        if (request.ok){
            select_company.innerHTML = "<option value=''> Choose your company </option>"
            console.log(response)
            response.forEach(company => {
                const option = document.createElement('option')
                option.value = company.id
                option.textContent = company.company_name  

                // append the created option to the select dropdown
                select_company.appendChild(option)              
            });
        }else{
            console.log(response)
        }
    }catch(error){
        console.error(error)
    }
}
document.addEventListener('DOMContentLoaded', load_company);

// create the registration endpoint to register a new company staff
const register = document.getElementById("register_form")
register.addEventListener('submit', async function (e) {
    e.preventDefault()

    const username = document.getElementById('username').value 
    const first_name = document.getElementById("first_name").value
    const last_name = document.getElementById("last_name").value
    const email = document.getElementById("email").value
    const company = document.getElementById("company").value
    const role = document.getElementById("role").value
    const password = document.getElementById("password").value
    const confirm_password = document.getElementById("confirm_password").value

    if(password != confirm_password){
        alert("Passwords must match")
        return
    }

    if(!company){
        alert("Please Choose a company")
    }

    try{
        const request = await fetch(`${BASE_URL}api/users/`, {
            method : "POST",
            headers : {
                "Content-Type" : "application/json"
            },
            credentials : "include",
            body : JSON.stringify({
                "username" : username, "first_name" : first_name, "last_name" : last_name, "email" : email, "role" : role, "company" : company, "password" : password, "confirm_password" : confirm_password
            })
        })
        const response = await request.json()
        if (request.ok){
            console.log(response)
            alert(`User has been registered Successfully. Your assgined ID is ${response.employee_ID}`)

            window.location.href = "login.html"
            sessionStorage.setItem('username', username)
        }
    }catch(error){
        console.error(error)
    }
})