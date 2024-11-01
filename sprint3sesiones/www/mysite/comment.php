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
    <body>
       
        <?php
            session_start();
            $db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('Fail');
            if (!empty($_SESSION['id_usuario'])){
                $user_id = $_SESSION['id_usuario'];
            } 
            echo $user_id;
            $fecha = new DateTime();
            $fecha_formateada =  $fecha->format('Y-m-d H-i-s');
            $id_libro = $_POST['id'];
            $nuevo_comentario = $_POST['new_comment'];
            $consulta_insercion = "INSERT INTO tComentarios(libro_id,comentario,usuario_id,fecha) VALUES(".$id_libro.",
            '".$nuevo_comentario."',". $user_id .",'". $fecha_formateada ."')";
            mysqli_query($db,$consulta_insercion) or die ("Error!");

            
            //verificar  mediante una consulta que se ha insertado correctamente con el id_usuario
            /*
            $consultaComprobacion = "SELECT * FROM tComentarios WHERE usuario_id='". $user_id ."'";
            echo $consultaComprobacion;
            $resultado_comprobacion = mysqli_query($db,$consultaComprobacion);
            
            while ($fila = mysqli_fetch_array($resultado_comprobacion)){
                echo "<p>visualizando valores, comprobando  si ha insertado</p>";
                echo "id =>" .$fila['id'];
                for ($columna = 0 ; $columna <5; $columna ++){
                    echo "<p>".$fila[$columna]."<p>";
                }
            }
            */
            //fin comprobación
            
            echo "<p>Nuevo comentario</p>";
            echo mysqli_insert_id($db);
            echo "<p>Se ha generado un nuevo comentario</p>";
            mysqli_close($db);
            echo "<a href=/detail.php?id='".$id_libro."'>Volver</a>";
            
        ?>
    
</html>