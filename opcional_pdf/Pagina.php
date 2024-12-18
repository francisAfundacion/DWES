<?php
    require('fpdf186/fpdf.php');
    class PDF extends FPDF{
        function cabecera() {

        }
    }
    function validar_campo ($campo) {
        $LETRAS = "abcdefghijklmnopqrstuvwxyz";
        $campo = strtolower($campo);
        for ($pos_cadena = 0; $pos_cadena < strlen($campo) ; $pos_cadena ++){
            if (!stripos($LETRAS, $campo[$pos_cadena])) {
                die ("<p>El campo pasado no es una cadena válida, ya que contiene caracteres no permitidos.</p>");
            }
        }
    }

    function comprobar_query_params(){
        if (!isset($_GET['name'])){
            die ("<p>No ha  llegado correctamente el nombre del diplomado.</p>");
        }
        else {
            echo $_GET['name'];
            validar_campo($_GET['name']);
        }

        if (!isset($_GET['surname'])) {
            die ("<p>No ha llegado correctamente el apellido del diplomado.</p>");
        }
        else {
            echo $_GET['surname'];
            validar_campo($_GET['surname']);
        }
        
    }
    comprobar_query_params();
?>