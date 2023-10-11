// Function to get a cookie by name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Check if the cookie starts with the desired name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to set a cookie
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; SameSite = Strict; path=/";
}

// Function to send a POST request
async function sendPost(url, data) {
    const csrftoken = getCookie('csrftoken');
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('ERROR');
        }

        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            const responseData = await response.json();
            // Do something with responseData here
            return responseData;
        } else {
            const responseText = await response.text();
            // Do something with responseText here
            return responseText;
        }
    } catch (error) {
        // Handle errors here
        console.error('Error:', error);
    }
}

const createUser = document.getElementById('create-user');
const loginUser = document.getElementById('login-user');
const nickInput = document.getElementById('nick');
const passwdInput = document.getElementById('passwd');

// Function to get user data from input fields
function getUserData() {
    let userName = nickInput.value;
    let userPwd = passwdInput.value;
    // Replace special characters to prevent issues (temporary)
    userName = userName.replaceAll(';', 'SEMICOLON5WNKVjhLxT');
    userName = userName.replaceAll('=', 'EQUALS02vqGHimqN');
    userName = userName.replaceAll('\\', 'BACKSLASHhTwudhrjLN');
    userPwd = userPwd.replaceAll(';', 'SEMICOLON7IYWaNsj2M');
    userPwd = userPwd.replaceAll('=', 'EQUALS1O8OXS2Ka8');
    userPwd = userPwd.replaceAll('\\', 'BACKSLASHeWvl59Sq1c');

    return [userName, userPwd];
}

// Event listener for creating a user
createUser.addEventListener('click', async function() {
    var namePwd = getUserData();
    if (namePwd[0] && namePwd[1]) {
        const response = await sendPost('createUser/', { name: namePwd[0], password: namePwd[1] });
        if (response.create) {
            alert("Usuário criado com sucesso!"); // User created successfully
            nickInput.value = '';
            passwdInput.value = '';
        } else {
            alert("Usuário já existe!"); // User already exists
        }
    } else {
        alert("Nem usuário nem senha podem estar vazios!"); // Neither username nor password can be empty
    }
});

// Event listener for logging in
loginUser.addEventListener('click', async function() {
    var namePwd = getUserData();
    const response = await sendPost('/authUser/', { name: namePwd[0], password: namePwd[1] });
    if (response.auth) {
        setCookie('user', namePwd[0]);
        setCookie('password', namePwd[1]);
        location.href = '/homepage/';
    } else {
        alert("Usuário e/ou senha incorretos!"); // Incorrect username and/or password
    }
});
