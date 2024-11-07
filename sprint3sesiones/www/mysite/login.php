<?php
    //Realizar la conexión con la base de datos mysitedb
    $db = mysqli_connect('localhost','root','1234','mysitedb');
     /**
     * Función que comprueba si la cuenta existe en la base de datos y si la contraseña proporcionada es correcta.
     *
     * @param string $email Correo electrónico del usuario a verificar.
     * @param string $pass Contraseña proporcionada por el usuario para verificar.
     * @return string Mensaje de error si alguna de las validaciones falla, o vacío si todo es correcto.
     */
    function comprobar_cuenta_existe ($email,$pass){
        global $db;
        $mensajetxt = "";
        // Consulta para comprobar que el usuario asociado al email pasado exista.
        $consulta = $db -> prepare("SELECT * FROM tUsuarios WHERE email=?");
        $consulta -> bind_param("s",$email);
        $consulta -> execute();
        $resultado_consulta = $consulta -> get_result();
        $consulta -> close();

        if (mysqli_num_rows($resultado_consulta) == 0){
            $mensajetxt = "¡ERROR!El email introducido no existe!";
        }
        else{
            $fila = mysqli_fetch_array($resultado_consulta);
            if(!password_verify($pass,$fila['contraseña'])){
                $mensajetxt = "¡ERROR!La contraseña introducida es incorrecta.";
            }
            else{
                 /*Inicia la sesión,guardando el id del usuario correspondiente y le redirige a la página principal*/
                session_start();
                $_SESSION['id_usuario'] = $fila['id'];
                header('location:main.php');
            }
        }
        return $mensajetxt;
    }  
?>
<html>
<head>
    <title>Ejercicio 3</title>
</head>
<body>
    <?php
         //Comprobar que los campos del formulario han llegado correctamente.
         if(!isset($_POST['email']) or !isset($_POST['fpass'])){
            echo "No ha llegado correctamente alguno de los campos del formulario.";
        }
        else{
            //Guardar los valores asociados a los campos del formulario en variables
            $email = $_POST['email'];
            $pass = $_POST['fpass'];
            //Comprobar que los valores del formulario no estén vacíos.
            if (!empty($email) and !empty($pass)){
                echo comprobar_cuenta_existe($email,$pass);         
            }
            else{
                echo "El correo electrónico y/o la contraseña se han  enviado vacíos.";
            }
        }
        mysqli_close($db);
    ?>
</body>
</html>