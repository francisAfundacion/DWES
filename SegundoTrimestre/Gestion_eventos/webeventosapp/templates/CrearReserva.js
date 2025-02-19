const response_login = fetch('http://127.0.0.1:8000/login', {
          method: 'GET',
         headers: {
               'Authorization': 'Token ' + localStorage.getItem('token')
           }
  })
  console.log(response_login);
  if (!response_login.ok) {
       window.location.href = "http://127.0.0.1:8000/crear_reserva";
  }
  else {
    document.getElementById('post-form').addEventListener('submit', async function(event) {
        const formData = new Formdata(this);
        const response_crear = fetch('/http://127.0.0.1:8000/crear_reserva/', {
        method: 'POST',
        headers: {
             'Authorization': 'Token' + localStorage.getItem('token'),
              'Content-Type': 'application/json'
              },
         .then(response => response.json())
          .then(data => console.log(data));
          body: JSON.stringify({
                  estado: formData.get('estado'),
                   evento: formData.get('evento'),
                   max_asistencias: formData.get('max_asistencias')
          })

     })
     console.log("exito");
     console.log(response_crear.ok);
  }

}
