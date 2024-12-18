<?php
    //habilitar mensajeserrores
    ini_set('display_errors', 1);
    error_reporting(E_ALL);
    require('fpdf186/fpdf.php');

    class PDF extends FPDF{
        function Header () {
            $ancho_pag = $this -> GetPagewidth();
            $this -> pintar_fondo_pagina($ancho_pag);
            $titulo = "Certificado Desarrollo de Aplicaciones Web";
            $this -> Image('img/logo.png',0,0, 50, 50);
            $this -> SetFont('Times', 'B', 18);
            $this -> ln(50);
            $this -> Cell($ancho_pag, 10, $titulo, 0, 1,'C', true);
        }

        function pintar_fondo_pagina ($ancho_pag) {
            $alto_pag = $this -> GetPageheight();
            $this -> SetFillColor(245, 245, 220);
            $this -> Cell ($ancho_pag, $alto_pag,'', 0, 0, 'C', true);
        }
       
    }

    function validar_campo ($campo) {
        $LETRAS = "abcdefghijklmnopqrstuvwxyz";
        $campo = strtolower($campo);
        for ($pos_cadena = 0; $pos_cadena < strlen($campo) ; $pos_cadena ++){
            if (stripos($LETRAS, $campo[$pos_cadena]) === false) {
                die ("<p>El campo pasado no es una cadena válida, ya que contiene caracteres no permitidos.</p>");
            }
        }
    }

    function comprobar_query_params(){
        if (!isset($_GET['name'])){
            die ("<p>No ha  llegado correctamente el nombre del diplomado.</p>");
        }
        else {
            //echo $_GET['name'];
            validar_campo($_GET['name']);
        }

        if (!isset($_GET['surname'])) {
            die ("<p>No ha llegado correctamente el apellido del diplomado.</p>");
        }
        else {
            //echo $_GET['surname'];
            validar_campo($_GET['surname']);
        }
        
    }

    comprobar_query_params();
    $pdf  = new PDF();
    $pdf -> SetMargins(0, 0, 0);
    $pdf -> Output();
?>