<?php
    $db = mysqli_connect('localhost','root','1234','mysitedb')or die('Error al conectarse a la base de datos!');
?>
<html>
    <head>
    </head>
    <body>
        <?php
            if (!isset($_GET['id'])){
                die('No se ha especificado la canción');
            }
            //RECORRO LOS CAMPOS DEL LIBRO CON ID ESPECIFICADO Y LOS MUESTRO
            $id_libro = $_GET['id'];
            $consulta = "SELECT * FROM tLibros WHERE  id =".$id_libro;
            $resultado = mysqli_query($db,$consulta) or die ("Query error");
            $fila = mysqli_fetch_array($resultado);
            $columna = 0;
            echo "<ul>";
            for ($columna = 0; $columna < 5 ; $columna ++){
                if ($columna == 2){
                    echo "<li><img src=".$fila[$columna]."></li>";
                }
                else {
                    echo "<li>".$fila[$columna]."</li>";
                }
            }
            echo "</ul>";
        ?>
        <!--
        <p>Deja un nuevo comentario:</p>
        <form action="/comment.php" method="post">
            <textarea rows="4" cols="50" name="new_comment"></textarea><br>
            <input type="hidden" name="id" value=<?php echo $id?>>
            <input type="submit" value="Comentar">
        </form>
        -->
    </body>
</html>