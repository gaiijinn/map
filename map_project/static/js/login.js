const loginForm = document.querySelector('#login-form');

loginForm.addEventListener('submit', (e) => {
   e.preventDefault();

   const email = document.getElementById('login-email').value;
   const password = document.getElementById('login-password').value;


   const data = {
      email: email,
      password: password
   };

   fetch('/api/token/', {
      method: 'POST',
      headers: {
         'Content-type': 'application/json'
      },
      body: JSON.stringify(data)
   })
      .then(async response => {
         if (!response.ok) {
            const text = await response.text();
            throw new Error(text);
         }
         return response.json();
      })
      .then(token => {
         setCookie('access_token', token.access, 7);
         setCookie('refresh_token', token.refresh, 7);
         setTimeout(() => {
            window.location.href = `/`;
         }, 3000);
      })
      .catch(error => console.log(`error: ${error}`));
});

function setCookie(name, value, days) {
   let expires = "";
   if (days) {
      const date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
   }
   document.cookie = name + "=" + (value || "") + expires + "; path=/";
}