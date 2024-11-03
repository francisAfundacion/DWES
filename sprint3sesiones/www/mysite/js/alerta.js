console.log("llego a alerta.js")

function comprobar_campos_vacios(Event)  {
const TEXTO_EMAIL = document.getElementById("email").value;
const TEXTO_PASS = document.getElementById("password").value;
    if (TEXTO_EMAIL == "" || TEXTO_PASS == ""){
        event.preventDefault(); // Evita que el formulario se envíe
        window.alert("Ha dejado campo/s sin rellenar");
    }
}

const LOGIN_FORMULARIO = document.getElementById("login_formulario");
LOGIN_FORMULARIO.addEventListener("submit",comprobar_campos_vacios);
