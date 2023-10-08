
/*--------------------------------------------------------------------------------------------------------------- */
/*
The MIT License

Copyright © 2016 Eli Grey.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
/*
* FileSaver.js
* A saveAs() FileSaver implementation.
*
* By Eli Grey, http://eligrey.com
*
* License : https://github.com/eligrey/FileSaver.js/blob/master/LICENSE.md (MIT)
* source  : http://purl.eligrey.com/github/FileSaver.js
*/

// The one and only way of getting global scope in all environments
// https://stackoverflow.com/q/3277182/1008999
var _global = typeof window === 'object' && window.window === window
  ? window : typeof self === 'object' && self.self === self
  ? self : typeof global === 'object' && global.global === global
  ? global
  : this

function bom (blob, opts) {
  if (typeof opts === 'undefined') opts = { autoBom: false }
  else if (typeof opts !== 'object') {
    console.warn('Deprecated: Expected third argument to be a object')
    opts = { autoBom: !opts }
  }

  // prepend BOM for UTF-8 XML and text/* types (including HTML)
  // note: your browser will automatically convert UTF-16 U+FEFF to EF BB BF
  if (opts.autoBom && /^\s*(?:text\/\S*|application\/xml|\S*\/\S*\+xml)\s*;.*charset\s*=\s*utf-8/i.test(blob.type)) {
    return new Blob([String.fromCharCode(0xFEFF), blob], { type: blob.type })
  }
  return blob
}

function download (url, name, opts) {
  var xhr = new XMLHttpRequest()
  xhr.open('GET', url)
  xhr.responseType = 'blob'
  xhr.onload = function () {
    saveAs(xhr.response, name, opts)
  }
  xhr.onerror = function () {
    console.error('could not download file')
  }
  xhr.send()
}

function corsEnabled (url) {
  var xhr = new XMLHttpRequest()
  // use sync to avoid popup blocker
  xhr.open('HEAD', url, false)
  try {
    xhr.send()
  } catch (e) {}
  return xhr.status >= 200 && xhr.status <= 299
}

// `a.click()` doesn't work for all browsers (#465)
function click (node) {
  try {
    node.dispatchEvent(new MouseEvent('click'))
  } catch (e) {
    var evt = document.createEvent('MouseEvents')
    evt.initMouseEvent('click', true, true, window, 0, 0, 0, 80,
                          20, false, false, false, false, 0, null)
    node.dispatchEvent(evt)
  }
}

// Detect WebView inside a native macOS app by ruling out all browsers
// We just need to check for 'Safari' because all other browsers (besides Firefox) include that too
// https://www.whatismybrowser.com/guides/the-latest-user-agent/macos
var isMacOSWebView = _global.navigator && /Macintosh/.test(navigator.userAgent) && /AppleWebKit/.test(navigator.userAgent) && !/Safari/.test(navigator.userAgent)

var saveAs = _global.saveAs || (
  // probably in some web worker
  (typeof window !== 'object' || window !== _global)
    ? function saveAs () { /* noop */ }

  // Use download attribute first if possible (#193 Lumia mobile) unless this is a macOS WebView
  : ('download' in HTMLAnchorElement.prototype && !isMacOSWebView)
  ? function saveAs (blob, name, opts) {
    var URL = _global.URL || _global.webkitURL
    // Namespace is used to prevent conflict w/ Chrome Poper Blocker extension (Issue #561)
    var a = document.createElementNS('http://www.w3.org/1999/xhtml', 'a')
    name = name || blob.name || 'download'

    a.download = name
    a.rel = 'noopener' // tabnabbing

    // TODO: detect chrome extensions & packaged apps
    // a.target = '_blank'

    if (typeof blob === 'string') {
      // Support regular links
      a.href = blob
      if (a.origin !== location.origin) {
        corsEnabled(a.href)
          ? download(blob, name, opts)
          : click(a, a.target = '_blank')
      } else {
        click(a)
      }
    } else {
      // Support blobs
      a.href = URL.createObjectURL(blob)
      setTimeout(function () { URL.revokeObjectURL(a.href) }, 4E4) // 40s
      setTimeout(function () { click(a) }, 0)
    }
  }

  // Use msSaveOrOpenBlob as a second approach
  : 'msSaveOrOpenBlob' in navigator
  ? function saveAs (blob, name, opts) {
    name = name || blob.name || 'download'

    if (typeof blob === 'string') {
      if (corsEnabled(blob)) {
        download(blob, name, opts)
      } else {
        var a = document.createElement('a')
        a.href = blob
        a.target = '_blank'
        setTimeout(function () { click(a) })
      }
    } else {
      navigator.msSaveOrOpenBlob(bom(blob, opts), name)
    }
  }

  // Fallback to using FileReader and a popup
  : function saveAs (blob, name, opts, popup) {
    // Open a popup immediately do go around popup blocker
    // Mostly only available on user interaction and the fileReader is async so...
    popup = popup || open('', '_blank')
    if (popup) {
      popup.document.title =
      popup.document.body.innerText = 'downloading...'
    }

    if (typeof blob === 'string') return download(blob, name, opts)

    var force = blob.type === 'application/octet-stream'
    var isSafari = /constructor/i.test(_global.HTMLElement) || _global.safari
    var isChromeIOS = /CriOS\/[\d]+/.test(navigator.userAgent)

    if ((isChromeIOS || (force && isSafari) || isMacOSWebView) && typeof FileReader !== 'undefined') {
      // Safari doesn't allow downloading of blob URLs
      var reader = new FileReader()
      reader.onloadend = function () {
        var url = reader.result
        url = isChromeIOS ? url : url.replace(/^data:[^;]*;/, 'data:attachment/file;')
        if (popup) popup.location.href = url
        else location = url
        popup = null // reverse-tabnabbing #460
      }
      reader.readAsDataURL(blob)
    } else {
      var URL = _global.URL || _global.webkitURL
      var url = URL.createObjectURL(blob)
      if (popup) popup.location = url
      else location.href = url
      popup = null // reverse-tabnabbing #460
      setTimeout(function () { URL.revokeObjectURL(url) }, 4E4) // 40s
    }
  }
)

_global.saveAs = saveAs.saveAs = saveAs

if (typeof module !== 'undefined') {
  module.exports = saveAs;
}
/*--------------------------------------------------------------------------------------------------------------- */

async function sendGet(url) {
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('ERROR');
            }
            return response.json();
        })
        .catch(error => {
            console.log('ERROR');
        });
}

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

async function sendPost(url, data) {
    const csrftoken = getCookie('csrftoken');
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('ERROR');
        }

        const contentType = response.headers.get('content-type');
        if(contentType && contentType.includes('application/json')) {
            return response.json();
        } else {
            return response.text();
        }
    })
    .then(data => {
        return data;
    })
    .catch(error => {
    });
}

const activitiesList = document.getElementById('loadedCalendar');
const answer = document.getElementById('answer');
var loadedActivities = {'name': null, 'password': null, 'activities': null};

async function showCalendar(activities, element) {
    var ul = document.createElement('ul');
    for(var i = 0; i < activities.length; i++) {
        var act = activities[i];

        var newLi = document.createElement("li");
        var ul2 = document.createElement('ul');
        newLi.appendChild(ul2);

        var liVal = document.createElement('li');
        var texVal = document.createTextNode('Valor = '+act.value.toString());
        liVal.appendChild(texVal);
        ul2.appendChild(liVal);


        var liPeop = document.createElement('li');
        var texPeop = document.createTextNode('Lista de pessoas:\n');
        liPeop.appendChild(texPeop);
        var ulPeop = document.createElement('ul');
        for(var j = 0; j < act.people.length; j++) {
            var person = act.people[j];
            var liPers = document.createElement('li');
            var texPers = document.createTextNode(person);
            liPers.appendChild(texPers);
            ulPeop.appendChild(liPers);
        }
        liPeop.appendChild(ulPeop);
        ul2.appendChild(liPeop)


        var liLocs = document.createElement('li');
        var texLocs = document.createTextNode('Lista de lugares:\n');
        liLocs.appendChild(texLocs);
        var ulLocs = document.createElement('ul');
        for(var j = 0; j < act.locations.length; j++) {
            var locat = act.locations[j];
            var liLoc = document.createElement('li');
            var texLoc = document.createTextNode(locat);
            liLoc.appendChild(texLoc);
            ulLocs.appendChild(liLoc);
        }
        liLocs.appendChild(ulLocs);
        ul2.appendChild(liLocs)


        var liScheds = document.createElement('li');
        var texScheds = document.createTextNode('Lista de alocações temporais:\n');
        liScheds.appendChild(texScheds);
        var ulScheds = document.createElement('ul');
        for(var j = 0; j < act.schedules.length; j++) {
            var schedul = act.schedules[j].intervals;
            var liSched = document.createElement('li');
            var texSched = document.createTextNode('Alocação número '+(j+1).toString()+':\n');
            liSched.appendChild(texSched);

            var ulSched = document.createElement('ul');
            for(var k = 0; k < schedul.length; k++) {
                var interv = schedul[k];
                var liInterv = document.createElement('li');
                var texInterv = document.createTextNode('Começo = '+interv.start+', Fim = '+interv.end);
                liInterv.appendChild(texInterv);
                ulSched.appendChild(liInterv);
            }
            liSched.appendChild(ulSched);
            ulScheds.appendChild(liSched);
        }
        liScheds.appendChild(ulScheds);
        ul2.appendChild(liScheds)


        ul.appendChild(newLi);
    }
    element.innerHTML = '';
    texActs = document.createTextNode('Lista de atividades carregadas:\n');
    element.appendChild(texActs);
    element.appendChild(ul);
}

window.onload = function() {
    var usr = getCookie('user');
    var pwd = getCookie('password');
    if (usr && pwd) {
        const respons = sendPost('/authUser/', {name: usr, password: pwd}).then(response => {
                if(response.auth) {
                    loadedActivities.name = usr;
                    loadedActivities.password = pwd;
                } else {
                    location.href = '/';
                }
            });
    } else {
        location.href = '/';
    }
};

function cleanScreen() {
    activitiesList.innerHTML = 'Atividades carregadas aparecerão aqui!';
    loadedActivities.activities = null;
    answer.innerHTML = 'Escolha ótima aparecerá aqui '
}


const importFileButton = document.getElementById('importFile');
const exportFileButton = document.getElementById('exportFile');
const createButton = document.getElementById('create');
const readButton = document.getElementById('read');
const updateButton = document.getElementById('update');
const deleteButton = document.getElementById('delete');
const computeButton = document.getElementById('compute');
const visualizeButton = document.getElementById('visualize');
const cleanButton = document.getElementById('clean');


/*--------------------------------------------------------------------------------------------------------------- */
/**
 * Select file(s).
 * @param {String} contentType The content type of files you wish to select. For instance, use "image/*" to select all types of images.
 * @param {Boolean} multiple Indicates if the user can select multiple files.
 * @returns {Promise<File|File[]>} A promise of a file or array of files in case the multiple parameter is true.
 */
function selectFile(contentType, multiple){
    return new Promise(resolve => {
        let input = document.createElement('input');
        input.type = 'file';
        input.multiple = multiple;
        input.accept = contentType;

        input.onchange = () => {
            let files = Array.from(input.files);
            if (multiple)
                resolve(files);
            else
                resolve(files[0]);
        };

        input.click();
    });
}
/*--------------------------------------------------------------------------------------------------------------- */

importFileButton.addEventListener('click', async function() {
    // Abrir janela de escolher arquivo JSON
    var fil = await selectFile('json',false);
    // Ler do arquivo escolhido os dados e passar pra tela
    var fr = new FileReader();
    fr.onload = function (e) {
        var data = fr.result;
        var activities = JSON.parse(data).activities;
        cleanScreen();
        loadedActivities.activities = activities;
        showCalendar(activities,activitiesList);
    }
    fr.readAsText(fil);
});

exportFileButton.addEventListener('click', function() {
    if(loadedActivities.activities) {
        // Criar arquivo JSON com os dados
        var json = JSON.stringify({'activities':loadedActivities.activities});
        var blob = new Blob([json], {type:"application/json;charset=utf-8"});
        // Fazer download do arquivo
        saveAs(blob, "calendario.json");
    }
    else {
        alert("Nada a salvar");
    }
});

createButton.addEventListener('click', function() {
    // Abrir janelinha pra preencher os dados da atividade
    // Quando o usuário clica em concluído, salva no banco de dados e mostra na listinha
});

readButton.addEventListener('click', async function() {
    // Mandar um aviso de que vai sobrescrever oq tah na tela atualmente pelo que tá salvo no sistema
    var conf;
    if (loadedActivities.activities) {
        conf = confirm("Os dados na sua tela serão sobrescritos pelo que está salvo no sistema! Deseja continuar?");
    } else {
        conf = true;
    }
    if(conf) {
        // Baixar do banco de dados as atividades
        let calend = sendPost('/homepage/getCalendar/', loadedActivities);
        // Mostrar as atividades
        var resp = await calend;
        if(resp.activities.length) {
            var activities = resp.activities;
            cleanScreen();
            loadedActivities.activities = activities;
            showCalendar(activities,activitiesList);
        } else {
            alert("Não há nada salvo ainda!");
        }
    }
});

updateButton.addEventListener('click', function() {
    // Só envia a versão nova das atividades que foram modificados pro banco de dados
    if(loadedActivities.activities) {
        if(confirm("Os dados no sistema serão sobrescritos pelos da sua tela. Deseja continuar?")) {
            sendPost('/homepage/saveCalendar/', loadedActivities);
        }
    } else {
        alert("Nada a enviar");
    }
});

deleteButton.addEventListener('click', function() {
    // Abre aviso de que vai apagar todas as atividades
    if(confirm("Os dados no sistema E na sua tela serão permanentemente deletados! Deseja continuar?")) {
        // Apaga todas atividades no BD e na tela
        sendPost('/homepage/deleteCalendar/', loadedActivities);
        cleanScreen();
    }
});

computeButton.addEventListener('click', async function() {
    if(loadedActivities.activities) {
        // Computa resposta e mostra atividades escolhidas, acho que abaixo das atividades normal serviria já
        let promis = sendPost('/homepage/optimizeCalendar/', loadedActivities);
        var resp = await promis;
        if(resp.activities.length) {
            showCalendar(resp.activities,answer)
        } else {
            alert("Nennuma resposta recebida! (provavelmente o problema é grande demais)");
        }
    } else {
        alert("Nada a enviar");
    }
    
});

visualizeButton.addEventListener('click', function() {
    // Abrir janelinha com as opções de mostrar como semana mês ano etc (queremos isso?)
    // Carregar visualização em formato de calendário com eventos nos horários
    // Talvez nem precise desse botão e possa carregar automaticamente.
    // Talvez esse botão troque entre a visualização como lista e a visualização como calendário
});

cleanButton.addEventListener('click', function() {
    // Limpar dados que estão sendo apresentados
    if(confirm("Os dados apresentados serão apagados da sua tela! Deseja continuar?")) {
        cleanScreen();
    }
});