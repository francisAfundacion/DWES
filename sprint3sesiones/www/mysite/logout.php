<?php
    $db = mysqli_connect('localhost','root','1234','mysitedb');
    function cerrar_sesion(){
        global $db;
        session_start();
        session_destroy();
        header('location:login.html');
    }
    cerrar_sesion();
    mysqli_close($db);
?>