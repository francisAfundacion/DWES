<html>
<?php
		$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Fail');
	?>
    <body>
        <?php
            $fecha = new DateTime();
            $fecha_formateada =  $fecha->format('Y-m-d H-i-s');
            $id_libro = $_POST['id'];
            $nuevo_comentario = $_POST['new_comment'];
            $consulta_insercion = "INSERT INTO tComentarios(libro_id,comentario,usuario_id,fecha) VALUES(".$id_libro.",
            '".$nuevo_comentario."',1,'".$fecha_formateada."')";
            mysqli_query($db,$consulta_insercion) or die ("Error!");
            echo "<p>Nuevo comentario</p>";
            echo mysqli_insert_id($db);
            echo "<p>Se ha generado un nuevo comentario</p>";
            mysqli_close($db);
            echo "<a href=/detail.php?id='".$id_libro."'>Volver</a>";
        ?>
    
</html>