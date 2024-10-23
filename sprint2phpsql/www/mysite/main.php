<html>
	<head>
			<style>
					table {
						width:500px;
						height:200px;
					}
					table,td,th{
						border: 2px solid black;
						border-collapse:collapse;
					}
					td{
						width:50px;
						height:5px;
					}
					td,th{
						border-collapse:collapse;
						padding:5px 20px ;	
						height:20px;
						text-align:center;
					}
			</style>
	</head>
	<?php
		$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Fail');
	?>
	<h1>Conexión establecida</h1>

	<table>
		<tr>
			<th>id</th>
			<th>nombre</th>
			<th>url_imagen</th>
			<th>autor</th>
			<th>precio</th>
		</tr>
	
		<?php
				//echo "ENTRO EN EL PHP PARA GENERAR FILAS";
				$consulta = "SELECT * FROM tLibros";
				$resultado = mysqli_query($db,$consulta) or die ("Query error");
				$fila ="";
				$columna = 0;
				while($fila = mysqli_fetch_array($resultado)){
					//echo "ENTRO EN EL BUCLE de iterar rows";
					//echo "<br>";
					echo "<tr>";
					for ($columna = 0; $columna < 5 ; $columna ++){
						//echo "ENTRO EN EL BUCLE MOVERME POR LAS COLUMNAS <br>";
						//echo "valor columna =>". $fila[$columna].;
						if ($columna == 2){
							echo "<td><img src=".$fila[$columna]."></td>";
						}
						else {
							echo "<td>".$fila[$columna]."</td>";
						}
					}
					echo "</tr>";
				}
		?>


	</table>
</html>
