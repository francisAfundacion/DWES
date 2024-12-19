<?php
    //habilitar mensajeserrores
    ini_set('display_errors', 1);
    error_reporting(E_ALL);
    require('fpdf186/fpdf.php');
    class PDF extends FPDF{
        function Header () {
            $this->SetLeftMargin(0);
            $ancho_pag = $this -> GetPagewidth();
            $posX_logo = ($ancho_pag / 2) - 50;
            $this -> pintar_fondo_pagina($ancho_pag);
            $this -> SetTextColor(0, 0, 128);
            $titulo = "Certificado Desarrollo de Aplicaciones Web";
            $this -> Image('img/logo.png', $posX_logo, 0, 50, 50);
            $this -> setX($posX_logo);
            $this -> SetY(60);
            $this -> SetFont('Times', 'B', 22);
            $this -> Cell($ancho_pag, 0, $titulo, 0, 1,'C', true);
        }

        function pintar_fondo_pagina ($ancho_pag) {
            $alto_pag = $this -> GetPageheight();
            $this -> SetFillColor(230, 230, 250);
            $this -> Cell ($ancho_pag, $alto_pag,'', 0, 0, 'C', true);
            $this -> SetTextColor(75, 0, 130);
            $this -> cuerpo_pagina ();
        }

        function cuerpo_pagina () {
            $ancho_pag = $this -> GetPagewidth();
            $ancho_celda = $ancho_pag - 65;
            $posX_cuerpo = ($ancho_pag - $ancho_celda) / 2 ;
            $fecha_diploma =  date("d-m-Y");
            
            $lineas_cuerpo = [
                ucwords(strtolower($_GET['name'])) . " " . ucwords(strtolower($_GET['surname'])). ",",
                "ha completado satisfactoriamente el curso de ". $fecha_diploma,
                "Desarrollo deAplicaciones Web (DAW)", 
                "que consta de una duración de 20000 horas, en el que ha desarrollado habilidades y conocimiento para el desarrollo y mantenimiento de aplicaciones web empleando",
                "empleando tanto tecnologías de back-end como de front-end"
            ];
            $this -> SetY(70);
            for ($linea = 0; $linea < count($lineas_cuerpo); $linea ++) {
                $this -> SetX($posX_cuerpo);
                if ($linea !== 0 && $linea !== 2 ){
                    $this -> SetFont('Arial','I',14);
                    $this -> MultiCell( $ancho_celda, 10, $lineas_cuerpo[$linea], 0, 1,'');
                }
                else {
                    $this -> SetFont('Arial','B',16);
                    $this -> Cell($ancho_celda, 10, $lineas_cuerpo[$linea], 0, 1,'L');
                }
                $this -> ln(5);
            }
            
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