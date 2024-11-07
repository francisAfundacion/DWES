<html>
    <head>
    <link rel="stylesheet" href="errores.css">
    </head>
    <body>
        <?php
            // Establece la conexión a la base de datos 'mysitedb' usando los parámetros proporcionados
            $db = mysqli_connect('localhost','root','1234','mysitedb');
             /**
            * Función para comprobar las contraseñas del usuario.
            *
            * Esta función valida que la contraseña antigua coincida con la que está almacenada en la base de datos,
            * que la nueva contraseña no sea igual a la antigua y que la nueva contraseña coincida con la confirmación.
            *
            * @param string $vieja Contraseña antigua proporcionada por el usuario
            * @param string $nueva Nueva contraseña proporcionada por el usuario
            * @param string $confirmacion Confirmación de la nueva contraseña
            * @return string Mensaje de error si alguna validación falla, cadena vacía si todo es correcto
            */
            function comprobar_contrasenas($vieja, $nueva,$confirmacion){
                session_start(); // abrir la sesión para acceder al id de usuario
                global $db;
                $mensajetxt = "";
                // Consulta SQL para obtener la contraseña almacenada del usuario con el ID almacenado en la sesión
                $consulta_contrasena_usuario = $db -> prepare("SELECT contraseña from tUsuarios where id=?");
                $consulta_contrasena_usuario -> bind_param("i",$_SESSION['id_usuario']);
                $consulta_contrasena_usuario -> execute();
                $resultado_contrasena_usuario = $consulta_contrasena_usuario -> get_result();
                $consulta_contrasena_usuario -> close();
                $fila = mysqli_fetch_array($resultado_contrasena_usuario);
                if (!password_verify($vieja,$fila['contraseña']) ){
                    $mensajetxt = "<p>¡ERROR¡La  contraseña antigua no coincide con la que está guardada en la base de datos!</p>";
                }
                else{
                    if($vieja == $nueva){
                        $mensajetxt= "<p>¡ERROR¡La nueva contraseña no puede ser idéntica a la antigua!</p>";
                    }
                    else{
                        if ($nueva != $confirmacion){
                            $mensajetxt= "<p>¡ERROR!¡La nueva contraseña no coincide con su respectiva confirmación!</p>";
                        }
                    }
                }
                return $mensajetxt;
            }
            /** 
            * Función para actualizar la contraseña del usuario en la base de datos.
            *
            * Esta función recibe la nueva contraseña, la encripta y luego la actualiza
            * en la base de datos para el usuario cuya sesión está activa.
            *
            * @param string $nueva Nueva contraseña que será asignada al usuario
            */
            function cambiar_contrasena_bd($nueva){
                global $db;
                session_start(); // abrir la sesión para acceder al id de usuario
                $nueva_contrasena_hasheada = password_hash($nueva,PASSWORD_DEFAULT);
                // Consulta SQL para modificar la contraseña del id del usuario guardada en la sesión actual.
                $consulta_modif_contrasena = $db -> prepare("UPDATE tUsuarios SET contraseña=? where id=?");
                $consulta_modif_contrasena -> bind_param("si",$nueva_contrasena_hasheada,$_SESSION['id_usuario']);
                $consulta_modif_contrasena -> execute();
                $consulta_modif_contrasena -> close();
            }
            
            
        ?>
        <?php
            $valido=true;
            $mensajetxt="";
             //Comprueba que los valores del formulario han llegado correctamente
            if (!isset($_POST['flast_pass']) or !isset($_POST['fnew_pass']) or !isset($_POST['fnew_pass_confirm'])){
                echo "<p>¡ERROR!Alguno de los campos para cambiar la contraseña no han llegado correctamente!</p>";
            }
            else{
                //Asigna los valores del formulario a variables.
                $last_pass = $_POST['flast_pass'];
                $new_pass = $_POST['fnew_pass'];
                $new_pass_confirm =  $_POST['fnew_pass_confirm'];
                //Comprobar si los valores del formulario han llegado vacíos
                if (empty($last_pass)) {
                    echo "<p>ERROR¡Se ha dejado vacío el campo relativo a la antigua contraseña!</p>";
                    $valido=false;
                }
                if (empty($new_pass)){
                    echo "<p>ERROR¡Se ha dejado vacío el campo relativo a la nueva contraseña!</p>";
                    $valido=false;
                }
                if (empty($new_pass_confirm)){
                    echo "<p>ERROR¡Se ha dejado vacío el campo relativo a la confirmación de la nueva contraseña</p>";
                    $valido=false;
                }
                if ($valido){
                        $mensajetxt= comprobar_contrasenas($last_pass,$new_pass,$new_pass_confirm,$email);
                        echo $mensajetxt;
                        if ($mensajetxt == ""){
                            cambiar_contrasena_bd($new_pass,$email);
                            echo "<p>¡Cambiada la contraseña con éxito!</p>";
                        }
                    else{
                        echo "<p>ERROR¡No se ha cambiado la contraseña correctamente!</p>";
                    }
                }
            }
        ?>
    </body>
</html>