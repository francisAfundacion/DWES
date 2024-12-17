<?php
//habilitar mensajeserrores
ini_set('display_errors', 1);
error_reporting(E_ALL);
require('fpdf186/fpdf.php');

//para poder personalizar cabecera y pie de página
class PDF extends FPDF
{
// Cabecera de página
function Header()
{
    // Logo
    //Image (ruta, coordx, cooordy,ancho,alto)
    $this->Image('img/logo.png',10,40,33);
    // Arial bold 15
    $this->SetFont('Arial','B',15);
    // Movernos a la derecha
    $this->Cell(150);
    // Título
    $this->Cell(30,10,'Title',1,0,'C');
    // Salto de línea Ln(unidades del salto)
    $this->Ln(20);
}

// Pie de página
function Footer()
{
    // Posición: a 1,5 cm del final
    $this->SetY(-15);
    // Arial italic 8
    $this->SetFont('Arial','I',8);
    // Número de página
    // Cell (ancho, alto, texto, borde, salto, alineación)
    $this->Cell(0,10,'Page '.$this->PageNo().'/{nb}',0,0,'C');
    // 0  => ancho
    // 10 => alto
    //pageNo() => DEVUELVE NÚMERO PÁGINA ACTUAL
    //{nb} => es sustuido por el número total de páginas del pdf
    //0 => borde de la celda => no
    // 0 => salto e línea de la celdas => no
    // 'C' =>  alineación del texto (C (centrado) / L(Izquierda) / R (derecha))
}
}

// Creación del objeto de la clase heredada
$pdf = new PDF();
// prepara el marcador {nb} para que sea reemplazado  por el n totales
// de la página, una vez haya generado el PDF COMPLETO
$pdf->AliasNbPages();
//agregar pag vacía
//CUANDO SE LLAMA ADDPAGE, SE HACE UNA LLAMADA INTERNA A HEADER() Y FOOTER(), POR ESO SE EJECUTAN AUNQUE NO LOS LLAMES.
$pdf->AddPage();
//fuente para el texto
$pdf->SetFont('Times','',12);
for($i=1;$i<=40;$i++)
    $pdf->Cell(0,10,'Imprimiendo línea número '.$i,0,1);
$pdf->Output();
?>