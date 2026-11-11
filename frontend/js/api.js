const BASE_URL = "http://127.0.0.1:8000/"
// create a function to get a new access token from the refresh token
async function refresh_access_token(){
    let refresh = localStorage.getItem("refresh_token")
    if(!refresh){
        return
    }
    // send a request with the access token 
    try{
        const request = await fetch(`${BASE_URL}api/token/refresh/`, {
            method: "POST",
            headers : {
                "Content-Type" : "application/json"
            },
            credentials : "include",
            body: JSON.stringify({ "refresh" : refresh})
        })
        const response = await request.json()
        if (request.ok){
            localStorage.setItem("access_token", response.access)
            if(response.refresh){
                localStorage.setItem("refresh_token", response.refresh)
            }
            return response.access
        }else{
            console.log(`Error Retrieving the access token ${response}`)
        }
    }catch(error){
        console.error(error)
    }
}

// create the a reuseable function for the fetch
async function authenticateFetch(url, options={}) {
    let access_token = localStorage.getItem("access_token")

    if(!access_token){
        return 
    }
    options.headers = {
        ...options.headers || {},
        "Authorization" : `Bearer ${access_token}`,
        "Content-Type" : "application/json"
    }
    let response = await fetch(url, options)
    if(response.status === 401){
        console.log("Access Token expired generating new Token now...")

        const new_access_token = await refresh_access_token()
        if(new_access_token){
            options.headers["Authorization"] = `Bearer ${new_access_token}`
            response = await fetch(url, options)
        }
    }
    return response
}

// check the current user page and lock any access
const publicPages = ['login.html', "register_page.html", 'index.html', 'company.html']
const currentPage = window.location.pathname.split("/").pop()

if(!localStorage.getItem("access_token") && !publicPages.include(currentPage) && currentPage !== ""){
    window.location.href = "login.html"
}


// check the user role
let user_role = localStorage.getItem("user_role")
console.log(user_role)
// define a functio to get all the users information
async function get_user(){
    const request = await authenticateFetch(`${BASE_URL}api/profile/`, {
        method : "GET", 
        credentials : "include"
    })
    const response = await request.json()
    if(request.ok){
        console.log(response)
        localStorage.setItem("user_role", response.role)
    }else{
        console.log("error fetching users profile")
    }
}

// get the saved user role 
get_user()

// create a function for the search input 
let search_input = document.getElementById("search_bar")
if(search_input){
    search_input.addEventListener("input", function(e){
        let search_value = e.target.value.toLowercase()
        let row_content = document.querySelectorAll(".tabel_body")

        row_content.forEach(row => {
            let row_values = row.textContent.toLowerCase()
            if(row_values.includes(search_value)){
                row.style.display = ""
            }else{
                row.style.display = "none";
            }
        })
    })
}

// create the logout functinality 
refresh_token = localStorage.getItem("refresh_token")
async function logout(){
    try {
        const request = await authenticateFetch(`${BASE_URL}api/logout/`, {
            method : "POST",
            credentials : "include",
            body : JSON.stringify({"refresh" : refresh_token })
        })
    } catch (error) {
        console.error(error)
    }

    localStorage.removeItem("refresh_token")
    localStorage.removeItem("access_token")
    localStorage.removeItem("user_role")

    window.location.href = "login.html"
}

document.addEventListener("DOMContentLoaded", () => {
    const logout = document.getElementById("logout_button")
    logout.addEventListener("click", (e) => {
        e.preventDefault()
        logout()
    })
})