
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Verifica se o cookie começa com o nome desejado
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; SameSite = Strict; path=/";
}

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
            // Faça algo com responseData aqui
            return responseData;
        } else {
            const responseText = await response.text();
            // Faça algo com responseText aqui
            return responseText;
        }
    } catch (error) {
        // Lidar com erros aqui
        console.error('Erro:', error);
    }
}


const createUser = document.getElementById('create-user');
const loginUser = document.getElementById('login-user');
const nickInput = document.getElementById('nick');
const passwdInput = document.getElementById('passwd');

function getUserData() {
    let userName = nickInput.value;
    let userPwd = passwdInput.value;
    // tmp
    userName = userName.replaceAll(';','SEMICOLN5WNKVjhLxT');
    userName = userName.replaceAll('=','EQUALSO2vqGHimqN');
    userName = userName.replaceAll('\\','BACKSLASHhTwudhrjLN');
    userPwd  = userPwd.replaceAll(';','SEMICOLN7IYWaNsj2M');
    userPwd  = userPwd.replaceAll('=','EQUALS1O8OXS2Ka8');
    userPwd  = userPwd.replaceAll('\\','BACKSLASHeWvl59Sq1c');
    
    return [userName,userPwd];
}

createUser.addEventListener('click', async function() {
    var namePwd = getUserData();
    if(namePwd[0] && namePwd[1]) {
        const response = await sendPost('createUser/', {name: namePwd[0], password: namePwd[1]});
        if(response.create) {
            alert("Usuario criado com sucesso!");
            nickInput.value = '';
            passwdInput.value = '';
        } else {
            alert("Usuario já existe!");
        }
    } else {
        alert("Nem usuario nem senha nao podem estar vazios!");
    }
});

loginUser.addEventListener('click', async function() {
    var namePwd = getUserData();
    const response = await sendPost('/authUser/', {name: namePwd[0], password: namePwd[1]});
    if(response.auth) {
        setCookie('user',namePwd[0]);
        setCookie('password',namePwd[1]);
        location.href='/homepage/';
    } else {
        alert("Usuário e/ou senha incorretos!");
    }
});