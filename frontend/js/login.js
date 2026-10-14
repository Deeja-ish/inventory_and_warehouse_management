const BASE_URL = "http://127.0.0.1:8000/"


// creating the login user endpoint
const login_form = document.getElementById("login_form")
// save the username from the register page 
document.addEventListener("DOMContentLoaded", () => {
    let saved_username = sessionStorage.getItem('username')
    const username_input = document.getElementById("username")

    if(saved_username && username_input){
        username_input.value = saved_username
    }
})

// login the user
login_form.addEventListener('submit', async function (e) {
    e.preventDefault()

    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

    if(!username.trim() && !password.trim()){
        alert(`Please fill in the required fields`)
        return 
    }

    try{
        const request = await fetch(`${BASE_URL}api/login/`, {
            method : "POST",
            headers : {
                "Content-Type" : "application/json"
            },
            credentials : "include",
            body: JSON.stringify({
                username, password
            })
        })
        const response = await request.json()
        if(request.ok){
            console.log(response)
            alert("Login Successful")
            window.location.href = "dashboard.html"
            // save the tokens 
            localStorage.setItem("access_token", response.access)
            localStorage.setItem("refresh_token", response.refresh)
        }else{
            alert(`invalid username or password please try again ${response}`)
            console.log(response)
        }
    }catch(error){
        console.error(error)
    }
})