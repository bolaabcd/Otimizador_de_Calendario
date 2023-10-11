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

// Check and set the global object to be used based on the environment
var _global = typeof window === 'object' && window.window === window
  ? window : typeof self === 'object' && self.self === self
  ? self : typeof global === 'object' && global.global === global
  ? global
  : this

// Function to add a Byte Order Mark (BOM) to text-based blobs for certain types
function bom(blob, opts) {
  if (typeof opts === 'undefined') opts = { autoBom: false }
  else if (typeof opts !== 'object') {
    console.warn('Deprecated: Expected the third argument to be an object')
    opts = { autoBom: !opts }
  }

  // Prepend BOM for UTF-8 XML and text/* types (including HTML)
  // Note: browsers automatically convert UTF-16 U+FEFF to EF BB BF
  if (opts.autoBom && /^\s*(?:text\/\S*|application\/xml|\S*\/\S*\+xml)\s*;.charset\s=\s*utf-8/i.test(blob.type)) {
    return new Blob([String.fromCharCode(0xFEFF), blob], { type: blob.type })
  }
  return blob
}

// Function to download a file from a given URL
function download(url, name, opts) {
  var xhr = new XMLHttpRequest()
  xhr.open('GET', url)
  xhr.responseType = 'blob'
  xhr.onload = function () {
    saveAs(xhr.response, name, opts)
  }
  xhr.onerror = function () {
    console.error('Could not download the file')
  }
  xhr.send()
}

// Function to check if Cross-Origin Resource Sharing (CORS) is enabled for a URL
function corsEnabled(url) {
  var xhr = new XMLHttpRequest()
  // Use a synchronous request to avoid popup blockers
  xhr.open('HEAD', url, false)
  try {
    xhr.send()
  } catch (e) {}
  return xhr.status >= 200 && xhr.status <= 299
}

// Function to simulate a click on a DOM node
function click(node) {
  try {
    node.dispatchEvent(new MouseEvent('click'))
  } catch (e) {
    var evt = document.createEvent('MouseEvents')
    evt.initMouseEvent('click', true, true, window, 0, 0, 0, 80, 20, false, false, false, false, 0, null)
    node.dispatchEvent(evt)
  }
}

// Detect if the application is running inside a macOS WebView
var isMacOSWebView = _global.navigator && /Macintosh/.test(navigator.userAgent) && /AppleWebKit/.test(navigator.userAgent) && !/Safari/.test(navigator.userAgent)

// Define the `saveAs` function for saving files
var saveAs = _global.saveAs || (
  // Probably in some web worker
  (typeof window !== 'object' || window !== _global)
    ? function saveAs() { /* Noop */ }

  // Use the download attribute first if possible (e.g., Lumia mobile) unless this is a macOS WebView
  : ('download' in HTMLAnchorElement.prototype && !isMacOSWebView)
  ? function saveAs(blob, name, opts) {
    var URL = _global.URL || _global.webkitURL
    // Namespace is used to prevent conflicts with Chrome Popper Blocker extension (Issue #561)
    var a = document.createElementNS('http://www.w3.org/1999/xhtml', 'a')
    name = name || blob.name || 'download'

    a.download = name
    a.rel = 'noopener' // tabnabbing

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
      setTimeout(function () { URL.revokeObjectURL(a.href) }, 4E4) // 40 seconds
      setTimeout(function () { click(a) }, 0)
    }
  }

  // Use msSaveOrOpenBlob as a second approach
  : 'msSaveOrOpenBlob' in navigator
  ? function saveAs(blob, name, opts) {
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
  : function saveAs(blob, name, opts, popup) {
    // Open a popup immediately to work around popup blockers
    // Mostly only available on user interaction, and the FileReader is async
    popup = popup || open('', '_blank')
    if (popup) {
      popup.document.title = popup.document.body.innerText = 'downloading...'
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
        popup = null // Reverse tabnabbing issue #460
      }
      reader.readAsDataURL(blob)
    } else {
      var URL = _global.URL || _global.webkitURL
      var url = URL.createObjectURL(blob)
      if (popup) popup.location = url
      else location.href = url
      popup = null // Reverse tabnabbing issue #460
      setTimeout(function () { URL.revokeObjectURL(url) }, 4E4) // 40 seconds
    }
  }
)

// Export the `saveAs` function for the CommonJS environment
if (typeof module !== 'undefined') {
  module.exports = saveAs;
}

// Asynchronous function to send a GET request and return a JSON response
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

// Function to get the value of a cookie by name
function getCookie(name) {
    var cookieValue = null;

    // Check if there are cookies available in the document
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();

            // Check if the cookie starts with the desired name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                // Decode and store the cookie value
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Asynchronous function to send a POST request with CSRF token and data
async function sendPost(url, data) {
    // Get the CSRF token from a cookie
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

        // Check if the response contains JSON data
        if (contentType && contentType.includes('application/json')) {
            return response.json();
        } else {
            return response.text();
        }
    })
    .then(data => {
        return data;
    })
    .catch(error => {
        // Handle any errors that may occur during the process
    });
}

// Function to create an HTML string with a specified element, attributes, and inner content
function createHtmlStr(type, keys, inner) {
    let htmlBuilder = [];

    htmlBuilder.push("<");
    htmlBuilder.push(type);
    
    // Loop through the attribute key-value pairs
    for(var key in keys) {
        htmlBuilder.push(" ");
        htmlBuilder.push(key);
        htmlBuilder.push("=\"");
        htmlBuilder.push(keys[key]);
        htmlBuilder.push("\" ");
    }
    
    // Add the inner content
    htmlBuilder.push("\">");
    htmlBuilder.push(inner);
    htmlBuilder.push("</");
    htmlBuilder.push(type);
    htmlBuilder.push(">");

    return htmlBuilder.join("");
}

// Function to create a <div> HTML string with a specified id, class, and inner content
function createDivStr(id, htmlClass, inner) {
    return createHtmlStr("div", {id: id, class: htmlClass}, inner);
}

// Function to create a <button> HTML string with a specified id, class, and inner content
function createButtonStr(id, htmlClass, inner) {
    return createHtmlStr("button", {id: id, class: htmlClass}, inner);
}

// Function to create an <input> HTML string with a specified id, type, and class
function createInputStr(id, type, htmlClass) {
    return createHtmlStr("input", {id: id, class: htmlClass, type: type}, "");
}

// Define a component for representing an interval
function IntervalComponent(identifier) {

    const id = identifier;

    // Function to get the ID of the "start" input element
    function getStartId() {
        return id + "#start";
    }

    // Function to get the ID of the "end" input element
    function getEndId() {
        return id + "#end";
    }

    // Function to get the value of the "start" input element
    function getStart() {
        const element = document.getElementById(getStartId());
        return element.value;
    }

    // Function to get the value of the "end" input element
    function getEnd() {
        const element = document.getElementById(getEndId());
        return element.value;
    }

// Function to generate the HTML representation of the interval component
function getHtml() {
    let htmlBuilder = [];

    htmlBuilder.push("<div class=\"interval\"><p>");

    htmlBuilder.push("Início: ");
    htmlBuilder.push(createInputStr(getStartId(), "datetime-local", "date-input"));

    htmlBuilder.push(" Fim: ");
    htmlBuilder.push(createInputStr(getEndId(), "datetime-local", "date-input"));

    htmlBuilder.push("</div>");

    return htmlBuilder.join("");
}

function getJs() {
    // Get the start and end times, removing the 'Z' character if present
    return {
        start: getStart().replace('Z', ''),
        end: getEnd().replace('Z', '')
    };
}

// Function to create an object with two methods: getHtml and getJs
return {
    getHtml: getHtml,
    getJs: getJs
}
}

function ScheduleComponent(identifier) {
    const id = identifier;
    let intervals = [];

    function addInterval() {
        // Create and add an IntervalComponent to the intervals array
        intervals.push(IntervalComponent(id + "#interval" + intervals.length));
        
        let el = document.getElementById(id);
        // Add the HTML representation of the newly created interval component
        el.innerHTML += intervals[intervals.length - 1].getHtml();
    }

    function setListeners() {
        const addButtonId = id + "#add";
        // Add a click event listener for the "Add Interval" button
        document.getElementById(addButtonId).addEventListener('click', addInterval);
    }

    function getHtml(el) {
        let htmlBuilder = [];

        const addButtonId = id + "#add";

        htmlBuilder.push("<div class=\"scheduleOut\">");
        htmlBuilder.push("<div class=\"scheduleIn\"");
        htmlBuilder.push("id=\"");
        htmlBuilder.push(id);
        htmlBuilder.push("\">");
        htmlBuilder.push("</div>");
        htmlBuilder.push(createButtonStr(addButtonId, "activity-button", "Adicionar Intervalo"));
        htmlBuilder.push("</div>");

        return htmlBuilder.join("");
    }

    function getJs() {
        let intervalsJs = [];
        for (let i = 0; i < intervals.length; i++) {
            // Get the JavaScript representation of each interval
            intervalsJs.push(intervals[i].getJs());
        }

        return {
            intervals: intervalsJs
        };
    }

    // Return an object with methods for HTML and JavaScript representation
    return {
        getHtml: getHtml,
        getJs: getJs,
        addInterval: addInterval,
        setListeners: setListeners
    }
}

function LocationComponent(identifier) {
    const id = identifier;

    function getHtml() {
        let htmlBuilder = [];

        // Create an HTML input element with the given ID
        htmlBuilder.push(createInputStr(id, "text", "text-input"));

        return createDivStr("", "", htmlBuilder.join(""));
    }

    function getJs() {
        // Get the value of the input element with the given ID
        return document.getElementById(id).value;
    }

    // Return an object with methods for HTML and JavaScript representation
    return {
        getHtml: getHtml,
        getJs: getJs
    }
}

function PersonComponent(identifier) {
    const id = identifier;

    function getHtml() {
        let htmlBuilder = [];

        // Create an HTML input element with the given ID
        htmlBuilder.push(createInputStr(id, "text", "text-input"));

        return createDivStr("", "", htmlBuilder.join(""));
    }

    function getJs() {
        // Get the value of the input element with the given ID
        return document.getElementById(id).value;
    }

    // Return an object with methods for HTML and JavaScript representation
    return {
        getHtml: getHtml,
        getJs: getJs
    }
}

function ActivityComponent(identifier) {
    const id = identifier;
    const addScheduleButtonId = id + "#addSchedule";
    const addLocationButtonId = id + "#addLocation";
    const addPersonButtonId = id + "#addPerson";
    let schedules = [];
    let locations = [];
    let people = [];

    function addLocation() {
        // Create and add a LocationComponent to the locations array
        locations.push(LocationComponent(id + "#location" + locations.length));
        
        let el = document.getElementById(id + "#locations");
        // Add the HTML representation of the newly created location component
        el.innerHTML += locations[locations.length - 1].getHtml();
    }

    function addSchedule() {
        // Create and add a ScheduleComponent to the schedules array
        schedules.push(ScheduleComponent(id + "#schedule" + schedules.length));
        
        let el = document.getElementById(id + "#schedules");
        // Add the HTML representation of the newly created schedule component
        el.innerHTML += schedules[schedules.length - 1].getHtml();

        for (let i = 0; i < schedules.length; i++) {
            // Set event listeners for each schedule component
            schedules[i].setListeners();
        }
    }
// Function to add a person to the activity
function addPerson() {
    // Push a new PersonComponent with a unique ID to the 'people' array
    people.push(PersonComponent(id + "#person" + people.length));

    // Get the element with the 'id + "#people"' and update its inner HTML with the new person's HTML
    let el = document.getElementById(id + "#people");
    el.innerHTML += people[people.length - 1].getHtml();
}

// Function to set event listeners
function setListeners() {
    // Loop through the 'schedules' array and set listeners for each schedule
    for(let i = 0; i < schedules.length; i++) {
        schedules[i].setListeners();
    }

    // Add click event listeners to buttons with specific IDs
    document.getElementById(addScheduleButtonId).addEventListener("click", addSchedule);
    document.getElementById(addLocationButtonId).addEventListener("click", addLocation);
    document.getElementById(addPersonButtonId).addEventListener("click", addPerson);
}

// Function to generate HTML for the activity
function getHtml() {
    let htmlBuilder = [];

    // Push the main div element with an 'id' attribute
    htmlBuilder.push("<div class=\"activity\"");
    htmlBuilder.push("id=\"");
    htmlBuilder.push(id);
    htmlBuilder.push("\">");

    // Generate HTML elements for schedules, locations, and people, and add buttons
    htmlBuilder.push(createDivStr(id + "#schedules", "", "<h3>Horários<h3>"));
    htmlBuilder.push(createButtonStr(addScheduleButtonId, "activity-button", "Adicionar Schedule"));
    htmlBuilder.push(createDivStr(id + "#locations", "", "<h3>Localizações</h3>"));
    htmlBuilder.push(createButtonStr(addLocationButtonId, "activity-button", "Adicionar Localização"));
    htmlBuilder.push(createDivStr(id + "#people", "", "<h3>Pessoas</h3>"));
    htmlBuilder.push(createButtonStr(addPersonButtonId, "activity-button", "Adicionar Pessoas"));

    // Add an input element for the activity's value
    htmlBuilder.push("<div><h3>Valor: </h3>");
    htmlBuilder.push(createInputStr(id + "#value", "number", "text-input"));
    htmlBuilder.push("</div>");

    // Add a button to submit the activity
    htmlBuilder.push(createButtonStr(id + "#activity", "activity-button", "Adicionar atividade."));

    // Join the HTML elements into a single string and log it to the console
    console.log(htmlBuilder.join(""));

    return htmlBuilder.join("");
}

// Function to generate JavaScript representation of the activity
function getJs() {
    let schedulesJs = [];
    for(let i = 0; i < schedules.length; i++) {
        schedulesJs.push(schedules[i].getJs());
    }

    let locationsJs = [];
    for(let i = 0; i < locations.length; i++) {
        locationsJs.push(locations[i].getJs());
    }

    let peopleJs = [];
    for(let i = 0; i < people.length; i++) {
        peopleJs.push(people[i].getJs());
    }

    // Get the value from an input element with the ID 'id + "#value"'
    let value = parseFloat(document.getElementById(id + "#value").value);

    // Return an object representing the activity's data
    return {
        schedules: schedulesJs,
        locations: locationsJs,
        people: peopleJs,
        value: value
    };
}

// Return an object with public methods and properties
return {
    getHtml: getHtml,
    addSchedule: addSchedule,
    setListeners: setListeners,
    getJs: getJs
    };
}

// Create an instance of the ActivityComponent with the ID "activity."
let activity = ActivityComponent("activity");

// Get the element with the ID "create-activity" and store it in the variable "creation."
let creation = document.getElementById("create-activity");

// Define a function to reset the activity selection.
function resetActivitySelection() {
    // Reassign the "activity" variable to a new instance of ActivityComponent with the ID "activity."
    activity = ActivityComponent("activity");
    
    // Update the HTML content of the "creation" element with the HTML generated by the activity component.
    creation.innerHTML = activity.getHtml();
    
    // Set event listeners for the activity component.
    activity.setListeners();

    // Get the element with the ID "activity#activity" and store it in the variable "createActivityButton."
    let createActivityButton = document.getElementById("activity#activity");

    // Add a click event listener to the "createActivityButton."
    createActivityButton.addEventListener("click", function() {
        // Get the JavaScript data representation of the activity.
        let data = activity.getJs();
        
        // Call the resetActivitySelection function to clear the current activity selection.
        resetActivitySelection();
    
        // Push the activity data to the "loadedActivities" array.
        loadedActivities.activities.push(data);

        // Update the calendar and retrieve the event colors.
        const colors = unoptimizedCalendar.update(loadedActivities.activities);

        // Display the updated calendar.
        showCalendar(loadedActivities.activities, activitiesList, colors);
    });
}

// Call the resetActivitySelection function to initialize the activity selection.
resetActivitySelection();

// Define a CalendarManager function that takes a source as a parameter.
function CalendarManager(source) {
    // Define an array of colors for calendar events.
    const activityColors = ['#3498db', '#2ecc71', '#e67e22', '#e74c3c', '#9b59b6', '#1abc9c', '#f1c40f', '#34495e'];

    // Create a new EventCalendar instance with the specified source element and initial configuration.
    let calendar = new EventCalendar(document.getElementById(source), {
        view: 'dayGridMonth',
        events: []
    });

    // Define an update function within the CalendarManager.
    function update(activities) {
        // Initialize an array to store event IDs.
        let ids = [];

        // Get the existing events from the calendar and store their IDs in the "ids" array.
        let events = calendar.getEvents();
        for(let i = 0; i < events.length; i++) {
            ids.push(events[i].id);
        }

        // Remove existing events from the calendar using their IDs.
        for(let i = 0; i < ids.length; i++) {
            calendar.removeEventById(ids[i]);
        }

        // Initialize an array to store event colors.
        let colors = [];

        // Iterate through the activities to add events to the calendar and assign colors.
        for(let i = 0; i < activities.length; i++) {
            const schedules = activities[i].schedules;

            // Generate a random color index from the "activityColors" array.
            const colorIndex = Math.floor(Math.random() * 7.9999);
            const color = activityColors[colorIndex];
            colors.push(color);

            // Iterate through schedules and intervals to add events to the calendar.
            for(let j = 0; j < schedules.length; j++) {
                const intervals = schedules[j].intervals;
                for(let k = 0; k < intervals.length; k++) {
                    const interval = intervals[k];
                    // Add an event to the calendar with the specified start, end, and background color.
                    calendar.addEvent({
                        id: 0, // You may want to assign unique IDs.
                        start: new Date(interval.start),
                        end: new Date(interval.end),
                        startEditable: false,
                        backgroundColor: color
                    });
                }
            }
        }

        // Return the array of event colors.
        return colors;
    }

    // Return an object with the "update" function.
    return {
        update: update
    }
}
// Create two instances of the CalendarManager, one for the unoptimized calendar and one for the optimized calendar.
let unoptimizedCalendar = CalendarManager('unoptimized');
let optimizedCalendar = CalendarManager('optimized');

// Get references to HTML elements by their IDs.
const activitiesList = document.getElementById('loadedCalendar');
const answer = document.getElementById('answer');

// Initialize an object to store loaded activities data.
var loadedActivities = {'name': null, 'password': null, 'activities': []};

// Function to display activities in a list format with specified colors.
function showCalendar(activities, element, colors) {
    // Create a new unordered list element to display activities.
    var ul = document.createElement('ul');
    
    // Iterate through the activities.
    for (var i = 0; i < activities.length; i++) {
        var act = activities[i];

        // Create a new list item for each activity.
        var newLi = document.createElement("li");
        
        // Create an inner unordered list for this activity with a background color.
        var ul2 = document.createElement('ul');
        ul2.style.backgroundColor = colors[i];
        newLi.appendChild(ul2);

        // Add an ID label for the activity if the element is not 'answer'.
        if (element != answer) {
            var liId = document.createElement('li');
            var id = document.createTextNode('ID = ' + String(i));
            liId.appendChild(id);
            ul2.appendChild(liId);
        }

        // Add a value label for the activity.
        var liVal = document.createElement('li');
        var texVal = document.createTextNode('Valor = ' + act.value.toString());
        liVal.appendChild(texVal);
        ul2.appendChild(liVal);

        // Add a list of people associated with the activity.
        var liPeop = document.createElement('li');
        var texPeop = document.createTextNode('Lista de pessoas:\n');
        liPeop.appendChild(texPeop);
        var ulPeop = document.createElement('ul');
        
        // Iterate through people in the activity.
        for (var j = 0; j < act.people.length; j++) {
            var person = act.people[j];
            var liPers = document.createElement('li');
            var texPers = document.createTextNode(person);
            liPers.appendChild(texPers);
            ulPeop.appendChild(liPers);
        }
        liPeop.appendChild(ulPeop);
        ul2.appendChild(liPeop);

        // Add a list of locations associated with the activity.
        var liLocs = document.createElement('li');
        var texLocs = document.createTextNode('Lista de lugares:\n');
        liLocs.appendChild(texLocs);
        var ulLocs = document.createElement('ul');

        // Iterate through locations in the activity.
        for (var j = 0; j < act.locations.length; j++) {
            var locat = act.locations[j];
            var liLoc = document.createElement('li');
            var texLoc = document.createTextNode(locat);
            liLoc.appendChild(texLoc);
            ulLocs.appendChild(liLoc);
        }
        liLocs.appendChild(ulLocs);
        ul2.appendChild(liLocs);

        // Add a list of temporal allocations associated with the activity.
        var liScheds = document.createElement('li');
        var texScheds = document.createTextNode('Lista de alocações temporais:\n');
        liScheds.appendChild(texScheds);
        var ulScheds = document.createElement('ul');

        // Iterate through temporal allocations in the activity.
        for (var j = 0; j < act.schedules.length; j++) {
            var schedul = act.schedules[j].intervals;
            var liSched = document.createElement('li');
            var texSched = document.createTextNode('Alocação número ' + (j + 1).toString() + ':\n');
            liSched.appendChild(texSched);

            var ulSched = document.createElement('ul');

            // Iterate through intervals within the temporal allocation.
            for (var k = 0; k < schedul.length; k++) {
                var interv = schedul[k];
                var liInterv = document.createElement('li');
                var texInterv = document.createTextNode('Começo = ' + interv.start.replace('T',' ').replace('Z','') + ', Fim = ' + interv.end.replace('T',' ').replace('Z',''));
                liInterv.appendChild(texInterv);
                ulSched.appendChild(liInterv);
            }
            liSched.appendChild(ulSched);
            ulScheds.appendChild(liSched);
        }
        liScheds.appendChild(ulScheds);
        ul2.appendChild(liScheds);

        ul.appendChild(newLi);
    }
    
    // Clear the content of the specified element.
    element.innerHTML = '';
    element.appendChild(ul);
}

// Run this code when the window is fully loaded.
window.onload = function() {
    // Get the user and password information from cookies.
    var usr = getCookie('user');
    var pwd = getCookie('password');

    // If user and password are available, send a POST request to authenticate the user.
    if (usr && pwd) {
        const respons = sendPost('/authUser/', {name: usr, password: pwd}).then(response => {
            // If the authentication is successful, update the loadedActivities object.
            if (response.auth) {
                loadedActivities.name = usr;
                loadedActivities.password = pwd;
            } else {
                // If authentication fails, redirect to the home page.
                location.href = '/';
            }
        });
    } else {
        // If user and password information is not available, redirect to the home page.
        location.href = '/';
    }
};
// Get references to various HTML elements by their IDs
const importFileButton = document.getElementById('importFile');  // Import file button
const exportFileButton = document.getElementById('exportFile');  // Export file button
const readButton = document.getElementById('read');              // Read button
const updateButton = document.getElementById('update');          // Update button
const deleteButton = document.getElementById('delete');          // Delete button
const computeButton = document.getElementById('compute');        // Compute button
const cleanButton = document.getElementById('clean');            // Clean button
const goBackButton = document.getElementById('goBack');          // Go back button

/*--------------------------------------------------------------------------------------------------------------- */
/**
 * Function to select a file or multiple files based on content type.
 * @param {String} contentType - The content type of files you wish to select, e.g., "image/*" to select all types of images.
 * @param {Boolean} multiple - Indicates if the user can select multiple files.
 * @returns {Promise<File|File[]>} - A promise of a file or an array of files if 'multiple' is true.
 */
function selectFile(contentType, multiple) {
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

// Add event listeners to the buttons

// Event listener for the "Import" button
importFileButton.addEventListener('click', async function() {
    // Open a file selection dialog to choose a JSON file
    var fil = await selectFile('json', false);
    // Read data from the chosen file and display it on the screen
    var fr = new FileReader();
    fr.onload = function (e) {
        var data = fr.result;
        var activities = JSON.parse(data).activities;

        loadedActivities.activities = activities;

        const colors = unoptimizedCalendar.update(loadedActivities.activities);
        showCalendar(activities, activitiesList, colors);
    }
    fr.readAsText(fil);
});

// Event listener for the "Export" button
exportFileButton.addEventListener('click', function() {
    if (loadedActivities.activities) {
        // Create a JSON file with the data
        var json = JSON.stringify({'activities': loadedActivities.activities});
        var blob = new Blob([json], {type: "application/json;charset=utf-8"});
        // Trigger file download
        saveAs(blob, "calendario.json");
    }
    else {
        alert("Nada a salvar.");
    }
});

// Event listener for the "Read" button
readButton.addEventListener('click', async function() {
    // Display a confirmation prompt if there are activities on the screen
    var conf;
    if (loadedActivities.activities.length != 0) {
        conf = confirm("The data on your screen will be overwritten by what is saved in the system! Do you want to continue?");
    } else {
        conf = true;
    }
    if (conf) {
        // Retrieve activities from the database
        let calend = sendPost('/homepage/getCalendar/', loadedActivities);
        // Display the activities on the screen
        var resp = await calend;
        if (resp.activities.length) {
            var activities = resp.activities;

            loadedActivities.activities = activities;
            const colors = unoptimizedCalendar.update(loadedActivities.activities);
            showCalendar(activities, activitiesList, colors);
        } else {
            alert("Não há nada salvo ainda!");
        }
    }
});
// Event listener for the "Update" button
updateButton.addEventListener('click', function() {
    // Send only the updated version of activities to the database
    if (loadedActivities.activities) {
        if (confirm("The data in the system will be overwritten by what's on your screen. Do you want to continue?")) {
            sendPost('/homepage/saveCalendar/', loadedActivities);
        }
    } else {
        alert("Nada a enviar.");
    }
});

// Event listener for the "Delete" button
deleteButton.addEventListener('click', function() {
    // Display a confirmation prompt to delete activities
    let act = prompt("Enter the ID of the activity to remove:");
    if (act < loadedActivities.activities.length && act >= 0) {
        loadedActivities.activities.splice(act, 1);
        const colors = unoptimizedCalendar.update(loadedActivities.activities);
        showCalendar(loadedActivities.activities, activitiesList, colors);
    } else {
        alert("Não há atividade com esse ID na sua tela.")
    }
});

// Event listener for the "Compute" button
computeButton.addEventListener('click', async function() {
    if (loadedActivities.activities) {
        // Compute a response and display chosen activities
        let promis = sendPost('/homepage/optimizeCalendar/', loadedActivities);
        var resp = await promis;
        if (resp.activities.length) {
            const colors = optimizedCalendar.update(resp.activities);
            showCalendar(resp.activities, answer, colors);
        } else {
            alert("Nenhuma resposta recebida! (o problema pode ser grande demais).");
        }
    } else {
        alert("Nada a enviar.");
    }
});

// Event listener for the "Clean" button
cleanButton.addEventListener('click', function() {
    // Clear data being displayed on the screen
    if (confirm("The data being displayed on your screen will be cleared. Do you want to continue?")) {
        resetActivitySelection();
        unoptimizedCalendar.update([]);
        optimizedCalendar.update([]);
        showCalendar([], answer, []);
        showCalendar([], activitiesList, []);
        loadedActivities.activities = [];
    }
});

// Event listener for the "Go Back" button
goBackButton.addEventListener('click', function () {
    location.href = '/';
});
