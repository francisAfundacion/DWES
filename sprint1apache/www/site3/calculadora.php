<html>
    <head>
        <title>Calculadora</title>
    </head>
    <body>
        <?php
            // FUNCIONES 
            function suma($num1, $num2) {
                return $num1 + $num2;
            }
            function resta($num1, $num2) {
                return $num1 - $num2;
            }
            function multiplicacion($num1, $num2) {
                return $num1 * $num2;
            }
            function division($num1, $num2) {
            	if ($num2 == 0) { 
                    return "ERROR! El denominador no puede ser 0!";
                } else {
                    return $num1 / $num2;
                }
            }
        ?>
        <h1>Calculadora</h1>
        <form action="/calculadora.php" method="post">
            <label for="idc1">Campo 1:</label>
            <input name="campo1" id="idc1" type="number"><br>
            <label for="idc2">Campo 2:</label>
            <input name="campo2" id="idc2" type="number"><br>
            
            <label for="listaOperaciones">Lista de operaciones:</label>
            <select id="listaOperaciones" name="flistaOperaciones">
                <option value="suma">Suma</option>
                <option value="resta">Resta</option>
                <option value="multiplicacion">Multiplicación</option>
                <option value="division">División</option>
            </select><br>
            <input type="submit" value="Realizar Operación">
        </form>

        <p>
        <?php
	    //CÓDIGO PRINCIPAL
            $num1 = 0;
            $num2 = 0;
            $tipoOperacion = "";
	    $resultado ="";

            if (!isset($_POST["campo1"]) or !isset($_POST["campo2"]))  {
		echo !isset($_POST["campo1"]). "  ".!isset($_POST["campo2"]);
		$resultado = "El primer y/o segundo  campo(s) numérico(s) no ha(n) sido introducido(s)";               
            }else {
  	     		 $num1 = $_POST['campo1'];
          		 $num2 = $_POST['campo2'];           
			 $tipoOperacion = $_POST['flistaOperaciones'];

           		 switch ($tipoOperacion) { 
                		case 'suma':
                   			 $resultado = suma($num1, $num2);
                   			 break;
              			 case 'resta':
                   			 $resultado = resta($num1, $num2);
                   			 break;
              			  case 'multiplicacion':
                   			 $resultado = multiplicacion($num1, $num2);
                   			 break;
               			 	default:
                   			 $resultado = division($num1, $num2);
                   			 break;
            		}
		       echo "El resultado es = ".$resultado;
		}

        ?>
        </p>
    </body>
</html>
