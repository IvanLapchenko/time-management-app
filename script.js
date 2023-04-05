window.onload = (event) => {

    const routes = [
      { path: '/time-management-app/', handler: homeHandler },
      { path: '/time-management-app/login.html', handler: loginHandler },
      { path: '/time-management-app/signup.html', handler: signupHandler },
      { path: '/time-management-app/index.html', handler: homeHandler },
    ];
    const urlHost = "http://ilapchenko0.pythonanywhere.com/"
    handleRoutes()



    function loginHandler () {
        const loginForm = document.querySelector('#login-form');
        const urlLogin = `${urlHost}/login`;

        loginForm.addEventListener('submit', (event) => {
                event.preventDefault();
                sendRequestToServer(event.target, urlLogin)
                .then(data => {
                    localStorage.setItem('token', data.token);
                    if ( data.isLogged ) {
                                location.replace('/time-management-app/index.html')
                    };
                })
        })
    }

    function signupHandler () {
        const loginForm = document.querySelector('#signup-form');
        const urlSignUp = `${urlHost}/signup`;

        loginForm.addEventListener('submit', (event) => {
                event.preventDefault();
                sendRequestToServer(event.target, urlLogin)
                .then(data => {
                    if ( data.isAddedToDB ) {
                                location.replace('/time-management-app/login.html')
                    };
        })
    })}

    function homeHandler () {
        const logoutButton = document.querySelector('#logout');
        const eventForm = document.querySelector('#add-new-event');
        const urlEvent = `${urlHost}/create_event`;

        renderEventsForFiveDays();


        eventForm.addEventListener('submit', (event) => {
                event.preventDefault();
                sendRequestToServer(event.target, urlEvent)
                .then(data =>  console.log(data))


        })

        logoutButton.addEventListener('click', (event) => {
            logout();
        })
    }

    function convertStringToDate(str) {
        return new Date(str).toLocaleDateString();
    }

    function logout () {
        localStorage.removeItem('token');
        location.replace('/login.html');
    }


    function sendRequestToServer(form, url) {
      const formData = new FormData(form);
      const data = {};
      const token = localStorage.getItem('token');
      let headersData = { "Content-type": "application/json" };

      for (const [key, value] of formData.entries()) {
        data[key] = value;
      }
      if (token)
        headersData.Authorization = `Bearer ${token}`;


      return new Promise((resolve, reject) => {

          fetch(url, {
              method: "POST",
              headers: headersData,
              body: JSON.stringify(data),
            })
            .then((response) => response.json())
            .then((data) => { resolve(data) })
            .catch((error) => {
              console.error("Помилка:", error);
              reject(error);
            });
      });
    }


    function handleRoutes () {
        const currentPath = window.location.pathname;
        const routeData = routes.find(route => route.path === currentPath);
        if (routeData) {
            routeData.handler();
           }
        else { homeHandler() }
    }


    function getEventsByDate (date) {
        const token = localStorage.getItem('token');
        const apiUrl = `http://127.0.0.1:5000/get_events_by/${date}`;

        return fetch(apiUrl, {
            method: "GET",
                headers: { Authorization: `Bearer ${token}`}
          })
          .then(response => response.json())
          .catch(error => {
            console.error('Error:', error);
          });
    }


function showEvents(eventsFromAPI, date) {

   // отримуємо div на сторінці та перетворюємо його на JS-об'єкт
   const eventsDiv = document.getElementById('events-for-five-days');

   // створоємо новий div для всіх подій на один день та додаємо йому клас single-day
   const dayEventsDiv = document.createElement('div');
   dayEventsDiv.classList.add('single-day');

   // отримуємо дату з першого об'єкта та додаємо її для відображення перед подіями на цю дату
   const displayData = document.createElement('h2');
   displayData.textContent = date;
   dayEventsDiv.appendChild(displayData);

   // Прохід по кожному об'єкту та створення div-елемента з назвою та описом
   eventsFromAPI.forEach(function(event) {
     // перетворюємо дані на об'єкт, так як приходить масив рядків
     event = JSON.parse(event)

     // створюємо елемент h3, в якому буде відображатись назва події
     const header = document.createElement('h3');
     header.textContent = event.header;
     // завдяки role="button" при наведенні буде змінюватись курсор
     header.role = "button";

     // створюємо елемент для відображення часу та, якщо час вказаний - відображаємо
     const time = document.createElement('span');
     if (event.time !== undefined) {
       time.textContent = event.time;
     }

     // додаємо опис та приховуємо його
     const describe = document.createElement('p');
     describe.value = event.describe;
     describe.style.display = 'none';


     // Обробник події натискання на ім'я, змінюємо режим відображення
     header.addEventListener('click', function() {
       describe.style.display = describe.style.display === 'none' ? 'block' : 'none';
     });


     const deleteButton = document.createElement('button');
     deleteButton.textContent = "Delete";
     deleteButton.value = event.header;
     deleteButton.addEventListener('click', () => sendDeleteRequest(deleteButton.value));


     // Створення div-елемента з ім'ям та описом та додавання його до розмітки
     const eventDiv = document.createElement('div');
     eventDiv.classList.add('single-event');
     eventDiv.appendChild(deleteButton);
     eventDiv.appendChild(header);
     eventDiv.appendChild(time);
     eventDiv.appendChild(describe);

     dayEventsDiv.appendChild(eventDiv);

   });
   eventsDiv.appendChild(dayEventsDiv);
 }


function sendDeleteRequest (eventData) {
    const token = localStorage.getItem('token');
    const deleteUrl = `http://127.0.0.1:5000/delete_event_by/${eventData}`;
    fetch(deleteUrl, {
        method: "GET",
        headers: { Authorization: `Bearer ${token}`}
        })
    .then(response => console.log(response));
}




    function renderEventsForFiveDays () {
        const endDate = new Date();
        endDate.setDate(endDate.getDate() + 5);
        let currentDate = new Date();

        while (currentDate <= endDate) {
            console.log(currentDate)
            date = currentDate.toISOString();
            let dateToDisplay = convertStringToDate(currentDate);

            getEventsByDate(date)
            .then(data => showEvents(data, dateToDisplay))
            currentDate.setDate(currentDate.getDate() + 1);
        }
    }

}
