<html>
	<body>
		<h1>Conversor de longitudes</h1>
		<p>Convierte de la unidad especificada a metros</p>
		<?php
		//Uso estas dos variables para la modificación de conversor2.php
		$v_ft = 0;
		$v_metros=0;
		//

		if (isset($_POST["funidad"])) {
			if ($_POST["funidad"] == "pulgada") {
				$v_pulgadas = $_POST["fcantidad"];
				$v_metros = $v_pulgadas * 0.0254;
				echo $v_pulgadas."pulgada(s) = ".$v_metros." metro(s)";
		}
			 else {
				if ($_POST["funidad"] == "ft"){
					$v_ft = $_POST["fcantidad"];
					$v_metros = $v_ft * 3.28084;
					echo $v_ft." ft(s) = ". $v_metros. " metro(s)" ;
			}
			}
		}
		?>
	
		<form action="/conversor2.php" method="post">
			<label for="cantidad_input">Cantidad:</label><br>
			<input type="text" id="cantidad_input" name="fcantidad"><br>
			<input type="radio" id="ft_input" name="funidad" value="ft">
			<label for="ft_input">ft(s)</label><br>
			<input type="radio" id="pulgada_input" name="funidad" value="pulgada">
			<label for="pulgada_input">Pulgada(s)</label><br>
			<input type="radio" id="otro_input" name="funidad" value="otro">
			<label for="otro_input">Otro</label><br>
			<input type="submit" value="Convertir">
		</form>
	</body>
</html>
