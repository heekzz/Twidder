var webSocket = new WebSocket("ws://localhost:5000/socket");
webSocket.onmessage = function (event) {
    if (event.data == "logout") {
        sessionStorage.removeItem("token");
        displayView();
    }
};


displayView = function(){
    // the code required to display a view
    var callback = function (response) {
        var view = null;
        if (getToken() != null && response.success == true) {
            view = document.getElementById("profileview");
            document.getElementById("placeholder").innerHTML = view.innerHTML;

            getUserData();
            // Get the element with id="defaultOpen" and click on it
            document.getElementById("defaultOpen").click();
        }
        else {
            view = document.getElementById("welcomeview");
            document.getElementById("placeholder").innerHTML = view.innerHTML;
        }
    };
    httpRequest("GET", "/getUserData?token="+getToken(),null ,callback);
    return false;
};
window.onload = function(){
    displayView();
};


function validateSignUp() {
    const PASSWORD_LENGTH = 8;
    var form = document.forms["signUp-form"];
    var email = form["email"].value;
    var password = form["password"].value;
    var password_repeat = form["password_repeat"].value;
    var alertText = document.getElementById("signUp-alert");

    if (password.length < PASSWORD_LENGTH || password_repeat.length < PASSWORD_LENGTH) {
        alertText.innerHTML = "Password too short!";
    } else {
        if (password != password_repeat) {
            alertText.innerHTML = "Password doesn't match!";
        } else {
            var signUpData = {
                email: email,
                password: password,
                firstname: form["firstname"].value,
                familyname: form["familyname"].value,
                gender: form["gender"].value,
                city: form["city"].value,
                country: form["country"].value
            };
            var data = new FormData(form);
            for (var key in signUpData) {
                data.append(key, signUpData[key]);
            }

            var callback = function (response) {
                if (response.success == true) {
                    sessionStorage.setItem("token", response.data.token);
                    displayView();
                } else {
                    if (response.message == "Not authenticated")
                        displayView();
                    alertText.innerHTML = response.message;
                }
            };
            httpRequest("POST", "/signup", data, callback);
        }
    }
    return false;
}

function login() {
    var form = document.forms["login-form"];
    var alertText = document.getElementById("login-alert");
    var token = "";
    var data = new FormData();
    data.append("email", form["email"].value);
    data.append("password", form["password"].value);

    var callback = function (response) {
        if(response.success == true) {
            token = response.data.token;
            console.log("Token: " + token);
            sessionStorage.setItem("token", token);
            var socketMessage = {"message": "login", "token": token};
            webSocket.send(JSON.stringify(socketMessage));
            displayView();
        } else {
            sessionStorage.removeItem("token");
            console.log("Failed: " + response.message);
            alertText.innerHTML = response.message;
        }
    };
    httpRequest("POST", "/login", data, callback);

    return false;
}

function logout() {
    var callback = function (response) {
        if (response.success == true) {
            sessionStorage.removeItem("token");
            displayView();
        } else {
            if (response.message == "Not authenticated")
                displayView();
            console.log(response.message);
        }
    };
    httpRequest("POST", "/logout?token="+getToken(), null, callback);
    return false;
}

function getToken() {
    return sessionStorage.getItem("token");
}


function changePassword() {
    var form = document.forms["changePasswordForm"];
    var old_password = form["old"].value;
    var new_password_1 = form["new1"].value;
    var new_password_2 = form["new2"].value;
    var alertText = document.getElementById("changeAlert");

    if (new_password_1.length < 8 || new_password_2.length < 8) {
        alertText.innerHTML = "Invalid length of password!"
    } else {
        if (new_password_1 == new_password_2) {
            var data = new FormData();
            data.append("old", old_password);
            data.append("new1", new_password_1);

            var callback = function (response) {
                alertText.innerHTML = response.message;
            };
            httpRequest("POST", "/changePassword?token="+getToken(), data, callback);
        } else {
            alertText.innerHTML = "Password doesn't match!";
        }
    }
    return false;
}

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}


function getUserData() {
    var callback = function (response) {
        var user = response.data;
        document.getElementById("nameField").innerHTML = user.firstname;
        document.getElementById("familyField").innerHTML = user.familyname;
        document.getElementById("home-emailField").innerHTML = user.email;
        document.getElementById("genderField").innerHTML = user.gender;
        document.getElementById("cityField").innerHTML = user.city;
        document.getElementById("countryField").innerHTML = user.country;
        updateComments('home');
    };
    httpRequest("GET", "/getUserData?token="+getToken(), null, callback);
    return false;
}

function postComment(page) {
    var message = document.getElementById(page + "-comment-input").value;
    var email = document.getElementById(page + "-emailField").innerHTML;
    var data = new FormData();
    data.append("user", email);
    data.append("message", message);
    var callback = function(response) {
        if (response.success == true) {
            updateComments(page, email);
        } else {
            if (response.message == "Not authenticated")
                displayView();
            console.log(response.message);
        }
    };
    httpRequest("POST", "/postMessage?token="+getToken(), data, callback);
    return false;
}

function updateComments(page, email) {
    if (typeof email === "undefined") {
        email = document.getElementById(page + "-emailField").innerHTML;
    }

    var callback = function (response) {
        if (response.success) {

            var comments = response.data;
            var commentHolder =  document.getElementById(page + "-comment-holder");
            var content = "";
            for (var i = 0; i < comments.length; i++) {
                content += "<h4 class='comment-header'>" + comments[i].author + ":</h4>";
                content += "<p class='comment-body'>" + comments[i].message + "</p>";
                content += "<hr>"
            }

            commentHolder.innerHTML = content;
        } else {
            if (response.message = "Not authenticated")
                displayView()
        }
    };
    httpRequest("GET", "/getUserMessages/"+email+"?token="+getToken(), null, callback);
    return false;
}

function browseUser() {
    var alertText = document.getElementById("browseAlert");
    var input = document.getElementById("searchUserText").value;
    var callback = function(response) {
        if (response.success == true) {
            alertText.innerHTML = "";
            var user = response.data;
            document.getElementById("browse-nameField").innerHTML = user.firstname;
            document.getElementById("browse-familyField").innerHTML = user.familyname;
            document.getElementById("browse-emailField").innerHTML = user.email;
            document.getElementById("browse-genderField").innerHTML = user.gender;
            document.getElementById("browse-cityField").innerHTML = user.city;
            document.getElementById("browse-countryField").innerHTML = user.country;
            document.getElementById("browseInfo").style.display = "inline";
            updateComments('browse');
        } else {
            if (response.message == "Not authenticated")
                displayView();
            document.getElementById("browseInfo").style.display = "none";
            alertText.innerHTML = response.message;
        }
    };
    httpRequest("GET", "/getUserData/"+input+"?token="+getToken(), null, callback);
    return false;
}

function httpRequest(method, url, data, callback) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            callback(response);
        }
    };
    xhttp.open(method, "http://localhost:5000" + url, true);
    if (data != null)
        xhttp.send(data);
    else
        xhttp.send();
}

