<html>
	<head>
			<style>
					body{
						font-style: "sans serif,Arial";
						font-size:16px;
						text-align:center;
						color:brown;
						text-shadow:1px 1px 1px black;
						background-color:hwb(69 87% 5%);
					}
					table {
						width:500px;
						height:200px;
						margin:auto;
						background-color:#f7e6e6;
					}
					table,td,th{
						border: 2px solid black;
						border-collapse:collapse;
						border-radius:5px;
					}
					td,th{
						border-collapse:collapse;
						padding:5px 20px ;	
					}
					img {
						width:200px;
						height:200px;
					}
					th{
						background-color:#f5bdcd;
					}
					td {
						color: hsl(330, 80%, 27%);
					}
					@keyframes fadeIn {
						from {opacity:1;}
						to{opacity:0.4;}
					}
					.fadeIn:hover{
						animation:fadeIn 4s ease;
					}
					a:link{
						color:hsl(330, 80%, 27%);
					}
					a:visited{
						color:brown;
					}
					a:active {
						color:rgb(89, 72, 117);
					}
			</style>
	</head>
	<?php
		$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Fail');
	?>
	<h1>Conexión establecida</h1>

	<table>
		<tr>
			<th> <span class="fadeIn">id</span></th>
			<th><span class="fadeIn">nombre</span></th>
			<th><span class="fadeIn">url_imagen</span></th>
			<th><span class="fadeIn">autor</span></th>
			<th><span class="fadeIn">precio</span></th>
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
						if ($columna == 0){
							echo "<td><a class=fadeIn href='http://localhost:8084/detail.php?id=".$fila[$columna]."'>".$fila[$columna]."</a></td>";
						}else{
							if ($columna == 2){
								echo "<td><img class=fadeIn src=".$fila[$columna]."></td>";
							}
							else{
								echo "<td> <span class=fadeIn>".$fila[$columna]."</span></td>";
							}
						}	
					}
					echo "</tr>";
				}
				mysqli_close($db);
		?>

	</table>
	<?php
		echo "<a href=/logout.php>Cerrar Sesión</a><br>";
		echo "<a href=cambiar_contrasena.html>Cambiar contraseña</a>"
	?>
</html>
