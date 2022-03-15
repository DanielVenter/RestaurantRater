const registerBtn = document.getElementById("id_submit");

const username = document.getElementById("id_username");
const password = document.getElementById("id_password");
const email = document.getElementById("id_email");
const street_number = document.getElementById("id_street_number");
const _name = document.getElementById("id_name");
const surname = document.getElementById("id_surname");
const city = document.getElementById("id_city");
const street = document.getElementById("id_street");

const passChecker = new RegExp('(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{6,})')

const fieldsArray = [username, password, email, street_number, _name, surname, city, street];

function checkInputs(){
    //Email checking
    if(email.value === "")
        setErrorFor(email, "Your email address cannot be blank.")
    else if(!checkEmailIsValid(email.value))
        setErrorFor(email, "Your email address is invalid.");
    else
        setSuccessFor(email);

    //Username checking
    if(username.value.length < 5 || username.value.length > 25)
        setErrorFor(username, "Username must be 5 to 25 characters long.");
    else
        setSuccessFor(username);

    //Password checking
    if(!checkPasswordStrong(password.value))
        setErrorFor(password, "Password must be at least 6 characters long and include a lowercase letter, uppercase letter and number.");
    else
        setSuccessFor(password);
    
    //Name checking
    if(_name.value === "")
        setErrorFor(_name, "Your name cannot be blank.");
    else
        setSuccessFor(_name);
    
    //Surname checking
    if(surname.value === "")
        setErrorFor(surname, "Your surname cannot be blank.");
    else
        setSuccessFor(surname);
    
    //City checking
    if(city.value === "")
        setErrorFor(city, "Your city cannot be blank.");
    else
        setSuccessFor(city);
    
    //Street checking
    if(street.value === "")
        setErrorFor(street, "Your street cannot be blank.");
    else
        setSuccessFor(street);

    //Street number checking
    if(street_number.value === "")
        setErrorFor(street_number, "Your street number cannot be blank.")
    else if(street_number.value < 0)
        setErrorFor(street_number, "The street number must be a positive integer.");
    else
        setSuccessFor(street_number);
    
    for(let x in fieldsArray)
        if(fieldsArray[x].classList.contains("error"))
            return false;
    
    return true;
    
}

registerBtn.addEventListener("click", e => {
    if(checkInputs() === false)
        e.preventDefault();
  });




//Sets success for a certain input box
function setSuccessFor(input){
    input.classList.remove("error");
    input.classList.add("success");

    inputDiv = input.parentElement;
    inputSmall = inputDiv.querySelector("small");
    inputSmall.style.display = "none";
}

//Sets error for a certain input box
function setErrorFor(input, message){
    input.classList.remove("success");
    input.classList.add("error");

    inputDiv = input.parentElement;
    inputSmall = inputDiv.querySelector("small");

    inputSmall.innerText = message;
    inputSmall.style.color = "red";
    inputSmall.style.display = "block";
}

//Checks if email is valid
function checkEmailIsValid(email){

    return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email);
}

function checkPasswordStrong(password){
    return passChecker.test(password);
}