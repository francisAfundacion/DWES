<html>
    <style>
        body{
            background-color:hwb(69 87% 5%);
            font-size:30px;
            font-weight:bold;
            text-shadow:1px 1px 1px black;
            color:brown;
            text-align:center;
            letter-spacing:3px;
        }
        a{
            margin:30px 0px;
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
        div{
            margin-top:8%;
        }
    </style>
<?php
		$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Fail');
	?>
    <body>
        <div>
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
        </div>
    
</html>