const street_number = document.getElementById("id_street_number");
const _name = document.getElementById("id_name");
const city = document.getElementById("id_city");
const street = document.getElementById("id_street");
const img1 = document.getElementById("id_img1");
const img2 = document.getElementById("id_img2");
const description = document.getElementById("id_description");
const img3 = document.getElementById("id_img3");
const submitBtn = document.getElementById("id_submit");
const restaurantExists = document.getElementById("invalid_name");
const invalidAddress = document.getElementById("invalid_address");

const fieldsArray = [_name, city, street_number, street, img1, img2, img3, description];

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

//Checks if restaurant already exists
if(restaurantExists.innerText === "Restaurant already exists." && invalidAddress.innerText === "1"){
    checkInputs();
    setErrorFor(_name, "Restaurant already exists.");
    setErrorFor(street, "Invalid address.");
    setErrorFor(city, "Invalid address.");
    setErrorFor(street_number, "Invalid address.");
    setErrorFor(img1, "You must re-upload the images, please!");
    setErrorFor(img2, "You must re-upload the images, please!");
    setErrorFor(img3, "You must re-upload the images, please!");
}
else if(restaurantExists.innerText === "Restaurant already exists."){
    checkInputs();
    setErrorFor(_name, "Restaurant already exists.");
    setErrorFor(img1, "You must re-upload the images, please!");
    setErrorFor(img2, "You must re-upload the images, please!");
    setErrorFor(img3, "You must re-upload the images, please!");
}
else if(invalidAddress.innerText === "1"){
    checkInputs();
    setErrorFor(street, "Invalid address.");
    setErrorFor(city, "Invalid address.");
    setErrorFor(street_number, "Invalid address.");
    setErrorFor(img1, "You must re-upload the images, please!");
    setErrorFor(img2, "You must re-upload the images, please!");
    setErrorFor(img3, "You must re-upload the images, please!");
}


function checkInputs(){
    //Check if first image has been uploaded
    if(img1.files.length === 0)
        setErrorFor(img1, "You must upload an image!");
    else
        setSuccessFor(img1);

    //Check if first image has been uploaded
    if(img2.files.length === 0)
        setErrorFor(img2, "You must upload an image!");
    else
        setSuccessFor(img2);
    
    //Check if second image has been uploaded
    if(img3.files.length === 0)
        setErrorFor(img3, "You must upload an image!");
    else
        setSuccessFor(img3);

    //Check if third image has been uploaded
    if(img3.files.length === 0)
        setErrorFor(img3, "You must upload an image!");
    else
        setSuccessFor(img3);
    
    //Check if restaurant's name is empty
    if(_name.value === "")
        setErrorFor(_name, "Your restaurant's name cannot be blank.");
    else
        setSuccessFor(_name);
    
    //Check if street's name is empty
    if(street.value === "")
        setErrorFor(street, "Your restaurant's street cannot be blank.");
    else
        setSuccessFor(street);

    //Check if restaurant's street name is empty
    if(city.value === "")
        setErrorFor(city, "Your restaurant's city cannot be blank.");
    else
        setSuccessFor(city);
    
    //Check if restaurant's street number is empty or <0
    if(street_number.value === "")
        setErrorFor(street_number, "Your restaurant's street number cannot be blank.");
    else if(street_number.value < 0)
        setErrorFor(street_number, "Your restaurant's street number must be a positive integer.")
    else
        setSuccessFor(street_number);
    
    //Check if restaurant's description is empty
    if(description.value === "")
        setErrorFor(description, "Your restaurant's description cannot be blank.");
    else
        setSuccessFor(description);

    for(let x in fieldsArray)
        if(fieldsArray[x].classList.contains("error"))
            return false;

    return true;

}

//If inputs are invalid, prevent form from submitting.
submitBtn.addEventListener("click", e => {
    if(checkInputs() === false)
        e.preventDefault();
  });