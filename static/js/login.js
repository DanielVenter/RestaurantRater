username = document.getElementsByName("username");
password = document.getElementsByName("password");
const loginBtn = document.getElementsByName("submit");
const invalidAccount = document.getElementById("invalid_account");

const fieldsArray = [username[0], password[0]];

//If inputs are invalid, prevent form from submitting.
loginBtn[0].addEventListener("click", e => {
    if(checkInputs() === false)
        e.preventDefault();
  });

if (invalidAccount.innerText === "Invalid account"){
    setErrorFor(password[0], "Invalid login credentials, please try again.");
    setErrorFor(username[0], "Invalid login credentials, please try again.");
}

//Function to check the inputs
function checkInputs(){
    if(password[0].value === "")
        setErrorFor(password[0], "Your password cannot be blank.");
    else
        setSuccessFor(password[0]);
    
    if(username[0].value === "")
        setErrorFor(username[0], "Your username cannot be blank.");
    else
        setSuccessFor(username[0]);
    
    for(let x in fieldsArray)
        if(fieldsArray[x].classList.contains("error"))
            return false;
    
    return true;
}

//Sets success for a certain input box
function setSuccessFor(input){
    input.classList.remove("error");
    input.classList.add("success");

    inputDiv = input.parentElement;
    inputSmall = inputDiv.querySelector("small");
    inputSmall.style.display = "none";

    exclamationIcon = input.parentElement.parentElement.childNodes[5].childNodes[3];
    checkIcon = input.parentElement.parentElement.childNodes[5].childNodes[1];
    checkIcon.style.display = "block";
    exclamationIcon.style.display = "none";

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

    exclamationIcon = input.parentElement.parentElement.childNodes[5].childNodes[3];
    checkIcon = input.parentElement.parentElement.childNodes[5].childNodes[1];
    checkIcon.style.display = "none";
    exclamationIcon.style.display = "block";
}