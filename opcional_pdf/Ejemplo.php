    <?php 
        //incluir fichero de la clase FPDF
        require('fpdf186/fpdf.php');
        // Valores por defecto P(orientación vertical),mm(unidades medida), A4(tamaño página), 
        $pdf = new FPDF();  
        // Crea página  y el origen de coordenadas es en la esquina superior izq.
        //Por defecto hay un margen de 1cm entre los bordes, se puede cambiar el comportamiento con setMargins()
        $pdf -> AddPage();
        //Escoger fuente , en este caso Arial, negrita y  tamaño 16.
        $pdf -> SetFont('Arial', 'B', 16);
        // 40 => ancho de la celda; 10 => alto de la celda, TEXTO, 1(SÍ BORDE)/ 0 (NO BORDE)
        $pdf->Cell(40,10,'¡Hola, Mundo!',1);
        $pdf -> Output();
    ?>
