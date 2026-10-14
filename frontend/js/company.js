const BASE_URL = `http://127.0.0.1:8000/`

// create the function to post the oand create the company
const create_company = document.getElementById("create_company")
create_company.addEventListener("submit", async function (e) {
    e.preventDefault()

    const company_name = document.getElementById("company_name").value.trim()
    const registration_number = document.getElementById("registration_number").value.trim()
    const email = document.getElementById("email").value.trim()
    const phone_number = document.getElementById("phone_number").value.trim()
    const address = document.getElementById("address").value.trim()

    // creat the post endpoint 
    try {
        const request = await fetch(`${BASE_URL}api/companies/`, {
            method: "POST",
            headers : {
                "Content-Type" : "application/json"
            },
            body : JSON.stringify({
                company_name, registration_number, email, phone_number, address
            }),
            credentials: "include"
        })
        const response = await request.json()
        if (request.ok){
            console.log(response)
            alert("New Company had been added Successfully")
        }else{
            console.log("Error creating new company", response)
        }
    } catch (error) {
        console.error(error)
    }
})