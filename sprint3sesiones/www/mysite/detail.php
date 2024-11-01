<?php
    $db = mysqli_connect('localhost','root','1234','mysitedb')or die('¡Error al conectarse a la base de datos!');
?>
<html>
    <head>
        <title>Ejercicio 3</title>
        <style>
            body{
                font-family: 'Times New Roman', Times, serif;
                font-size:16px;
                color:brown;
                background-color:hwb(69 87% 5%);
            }
            img {
                width:200px;
                height:200px;
            }
            ul > li .comentarios {
                margin:10px;
                list-style:square;
            }
            ul > li:not(.comentarios) {
                list-style:square;
            }
            input[type='submit'],textarea{
                margin-top:10px;
                border-radius:5px;
                background-color: rgb(247, 233, 213);
                color:brown;
            }

            
            input[type='submit']{
                margin-left:18%;
            }

            input[type='submit'],p{
                font-weight:bold;
            }
        </style>
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
        <h3>Listado comentarios:</h3>
        <ul>
        <?php
            $consulta_comentarios = "SELECT * FROM  tComentarios where libro_id=".$id_libro;
            $resultado_comentarios = mysqli_query($db,$consulta_comentarios) or die("¡Error a la hora de ejecutar la consulta!");
            $filas = "";
                while ($filas = mysqli_fetch_array($resultado_comentarios)){
                         echo "<li class='comentarios'>".$filas['comentario']."    :    <span>".$filas['fecha']."</span></li>";
                    }
            mysqli_close($db);
        ?>
        </ul>
        <p>Deja un nuevo comentario:</p>
        <form action="/comment.php" method="post">
            <textarea rows="4" cols="50" name="new_comment"></textarea><br>
            <input type="hidden" name="id" value=<?php echo $id_libro?>>
            <input type="submit" value="Comentar">
        </form>
    </body>
</html>