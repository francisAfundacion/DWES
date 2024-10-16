 <html>
        <head>
                <title>Sprint 1 , parte 2,ejercicio 3</title>
        </head>
        <body>
                <h1>Sprint 1,parte 2,ejercicio 3</h1>
		<?php
			function mensaje_jubilacion ($edad){
				$mensaje="“¡Disfruta de tu tiempo!";
				if ( edad_en_10_anos ($edad) > 65){
					$mensaje="En 10 años tendrás edad de jubilación";
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
				$edad = $_GET["edad"];
				echo "<tr>";
				echo "<td>".$edad."</td>";
				echo "<td>".mensaje_jubilacion ($edad)
				."</td>";
				echo "</tr>";
			?>
		</table>
        </body>
</html>

 
