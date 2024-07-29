const registrationForm = document.querySelector("#registration-form");

registrationForm.addEventListener("submit", (e) => {
   e.preventDefault();

   const email = document.getElementById('email').value;
   const name = document.getElementById('name').value;
   const lastName = document.getElementById('last-name').value;
   const password = document.getElementById('password').value;
   const submitPassword = document.getElementById('submit-password').value;

   const data = {
      email: email,
      name: name,
      lastName: lastName,
      password: password,
      re_password: submitPassword
   };

   fetch(`/api/djoser/users/`, {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
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
      .then(() => {
         window.location.href = '/users/user-login/';
      })
      .catch(error => {
         console.error(`Помилка: ${error}`);
      });
});
