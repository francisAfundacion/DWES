<?php
    $db = mysqli_connect('localhost','root','1234','mysitedb');
    /** 
    *Función que permite cerrar sesión al usuario, tras haber elimiando el valor contenido de la sesión,
    *redirigiendo al mismo  a la página para iniciar sesión.
    */
    function cerrar_sesion(){
        global $db;
        session_start();
        session_destroy();
        header('location:login.html');
    }
    cerrar_sesion();
    mysqli_close($db);
?>