                                  
<html>
        <head>
                <title>Sprint 1 , parte 2,ejercicio 2</title>
        </head>
        <body>
                <h1>Sprint 1,parte 2,ejercicio 2</h1>
                <h2>Página de Bienvenidas</h2>
		<?php
			function mensaje_jubilacion ($edad){
				$mensaje="No tienes edad de jubilación";
				if ( edad_en_10_anos ($edad) > 65){
					$mensaje="Tienes edad de jubilación";
				}
				return $mensaje;
			}
			function edad_en_10_anos ($edad){
				return $edad +10;
			}			
		 ?>
		<table>
			<tr>
				<th>Edad</th>
				<th>Info</th>
			</tr>
			<?php
			//	$edad = $_GET['edad'];
				echo "<tr>";
				echo "<td>".$_GET['edad']."</td>";
				echo "<td>". mensaje_jubilacion ($_GET['edad'])."</td>";
				echo "</tr>";
			?>
		</table>
        </body>
</html>

 
