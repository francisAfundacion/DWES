<?php
    //Realizar la conexión con la base de datos mysitedb
    $db = mysqli_connect ('localhost','root','1234','mysitedb') or die ('Fallo al conectarse a la base de datos.');
    /**
     * Función para comprobar las credenciales del usuario durante el registro.
     *
     * Valida si el correo electrónico ya existe en la base de datos y si las contraseñas coinciden. Si todo es válido,
     * llama a la función `dar_alta` para registrar al usuario.
     *
     * @param string $email Correo electrónico del usuario a registrar
     * @param string $pass Contraseña proporcionada por el usuario
     * @param string $pass_confirm Confirmación de la contraseña proporcionada por el usuario
     * @return string Mensaje de error si alguna validación falla, o vacío si todo es correcto
    */
    function comprobar_credenciales ($email,$pass,$pass_confirm){
        global $db; // para poder acceder a la base de datos definida globalmente.
        $valido=true;
        $mensajetxt = "";
        //Consulta para verificar si el correo ya está registrado en la base de datos
        $consulta =$db-> prepare("SELECT * FROM tUsuarios WHERE email=?");
        $consulta -> bind_param("s",$email);
        $consulta -> execute();
        $resultado_consulta = $consulta -> get_result();
        $consulta -> close();
        //Comprobar que el correo existe
        if (mysqli_num_rows($resultado_consulta) > 0){
            $mensajetxt = "<p>¡Error!Ya existe el email en la base de datos.</p>";
            $valido= false;
        }
        else{
            //Comprobar si son coincidentes la contraseña y su confirmación.
            if ($pass != $pass_confirm){
                $mensajetxt = "<p>¡Error!La contraseña y la confirmación no coinciden.</p>";
                $valido = false;
            }
        }
        if ($valido){
            dar_alta($email,$pass);

         }
        return $mensajetxt;
}
  /**
     * Función para registrar un nuevo usuario a la base de datos
     *
     * Realiza la inserción del nuevo usuario con los valores pasados como parámetros de entrada, entre los cuales la contraseña
     * se guardará cifrada.Posteriormente se inicia la sesión, guardando el valor del id del nuevo usuario.Por último el usuario
     * es redirigido a la página principal
     *
     * @param string $email Correo electrónico del usuario a registrar
     * @param string $pass Contraseña proporcionada por el usuario
     * @param string $pass_confirm Confirmación de la contraseña proporcionada por el usuario
     * @return string Mensaje de error si alguna validación falla, o vacío si todo es correcto
    */

    function dar_alta ($email,$pass){ 
        global $db;
        $pass_heasheada = password_hash($pass, PASSWORD_DEFAULT);
        $consulta = $db -> prepare("INSERT INTO tUsuarios(nombre, apellidos, email, contraseña) VALUES(NULL, NULL,?,?)");
        $consulta -> bind_param("ss",$email,$pass_heasheada);
        $consulta -> execute();
        $resultado_consulta = $consulta -> get_result();
        $consulta -> close();
        session_start();
        sleep(5);
        $_SESSION['id_usuario'] = mysqli_insert_id($db);
        header('Location:main.php');
    }
        

?>
<html>
    <head>
    <link rel="stylesheet" href="errores.css">
        <title>Ejercicio2</title>
    </head>
    <body>
        <?php
            //Comprobar si han llegado correctamente los valores de los campos del formulario
            if(!isset($_POST['email']) or !isset($_POST['fpass']) or !isset($_POST['fpass_confirm']) ){
                echo "<p>No ha llegado corzrectamente alguno de los valores de los campos del formulario.</p>";
            }
            else {//asignar a variables los valores de los campos del formulario.
                $email = $_POST['email'];
                $pass = $_POST['fpass'];
                $pass_confirm = $_POST['fpass_confirm'];
                //Comprobar si las variables están vacías
                if (!empty($email) and !empty($pass) and !empty($pass_confirm)){
                    echo comprobar_credenciales($email,$pass,$pass_confirm);
                }
                else{
                    echo "<p>El correo electrónico,la contraseña o la confirmación la contraseña se han  enviado vacíos.</p>";
                }
            }
            mysqli_close($db);
        ?>
    </body>
</html>