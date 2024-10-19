c                                  
<html>
        <head>
                <title>Sprint 1 , parte 2,ejercicio 2</title>
        </head>
        <body>
                <h1>Sprint 1,parte 2,ejercicio 2</h1>
                <h2>Página de Bienvenidas</h2>
		<?php
			function mensaje_jubilacion ($edad,$num){
			$anos_jubila = 0;
			$mensaje_anos = "lo sentimos, pero el valor del númer no es primo!";
			$mensajeJubi = "";
			$mensaje = "";
				if ($edad <65){
					$mensajeJubi="¡Disfruta de tu tiempo!";
					if ( comprobar_primo ($num)){
						$anos_jubila = 65 -( edad_en_X_anos ($edad,$num));
						$mensaje_anos="en  ".$anos_jubila." años tienes edad de jubilación ";
					}
				$mensaje =$mensajeJubi." y ".$mensaje_anos;
			}
				return $mensaje;
				
			}
			function edad_en_X_anos ($edad,$num){
				return  $edad +$num;
			}	

			function comprobar_primo ($num){
				$valido = true;
				if ($num % 2 == 0){
					$valido = false;
				}
				return $valido;
			}	
		 ?>
		<table>
			<tr>
				<th>Edad</th>
				<th>Info</th>
			</tr>
			<?php	
				$nprimo = $_GET['primo'];
				$edad = $_GET['edad'];
				echo "<tr>";
				echo "<td>".$edad."</td>";
				echo "<td>". mensaje_jubilacion ($edad,$nprimo)."</td>";
				echo "</tr>";
			?>
		</table>
        </body>
</html>

 
