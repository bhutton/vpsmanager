// Form validation modules for Create User Form

function validateName() {
    if (document.forms["createUser"]["inputName"].value != "") {
        document.getElementById("valName").innerHTML = "";
        return(false)
    }
};

function validateEmail() {
    if (document.forms["createUser"]["inputEmail"].value != "") {
        document.getElementById("valEmail").innerHTML = "";
        return(false)
    }
};

function validatePassword() {
    if (document.forms["createUser"]["inputPassword"].value != "") {
        document.getElementById("valPassword").innerHTML = "";
        return(false)
    }
};

// Form validation modules for Create VPS Form

function validateVPSName() {
    if (document.forms["vps"]["name"].value != "") {
        document.getElementById("valName").innerHTML = "";
        return(false)
    }
}

function validateVPSDescription() {
    if (document.forms["vps"]["description"].value != "") {
        document.getElementById("valDescription").innerHTML = "";
        return(false)
    }
}