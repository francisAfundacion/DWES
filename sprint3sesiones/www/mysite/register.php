
   <!-- /*
    2. Añade un formulario register.html que permita registrar un nuevo usuario, habrá
dos campos para introducir la contraseña. Añade también una página register.php.
En esta página se mostrará un mensaje de error si el correo introducido ya existe
en la base de datos, si hay algún campo vacío o si las contraseñas no coinciden. Si
el registro se hace correctamente se almacenará al usuario a la base de datos y
redirigirá al usuario a la página principal. La contraseña no puede almacenarse
como texto plano. Para cifrarla debemos usar la función
password_hash($password, PASSWORD_DEFAULT). Haz commit y push.
    
RECURSOS USARÉ => mysqli_fetch
                => session_start()
                =>$SESSION
                =>session_destroy()
                =>mysqli_num_rows();
                =>header() 

*/
?>-->
<?php
    $db = mysqli_connect ('localhost','root','1234','mysitedb') or die ('Fallo al conectarse a la base de datos.');

    function comprobar_credenciales ($email,$pass,$pass_confirm){
        global $db; // para poder acceder a la base de datos definida globalmente.
        $valido=true;
        $mensajetxt = "";
        $consulta =$db-> prepare("SELECT * FROM tUsuarios WHERE email=?");
        $consulta -> bind_param("s",$email);
        $consulta -> execute();
        $resultado_consulta = $consulta -> get_result();
        $consulta -> close();

        if (mysqli_num_rows($resultado_consulta) > 0){
            $mensajetxt = "<p>¡Error!Ya existe el email en la base de datos.</p>";
            $valido= false;
        }
        else{
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
        <title>Ejercicio2</title>
    </head>
    <body>
        <?php
            if(!isset($_POST['email']) or !isset($_POST['fpass']) or !isset($_POST['fpass_confirm']) ){
                echo "<p>No ha llegado correctamente alguno de los valores de los campos del formulario.</p>";
            }
            else {
                $email = $_POST['email'];
                $pass = $_POST['fpass'];
                $pass_confirm = $_POST['fpass_confirm'];
                if (!empty($email) and !empty($pass) and !empty($pass_confirm)){
                    echo comprobar_credenciales($email,$pass,$pass_confirm);
                }
                else{
                    echo "<p>El correo electrónico,la contraseña o la confirmación la contraseña se han  enviado vacíos.</p>";
                }
            }
        ?>
    </body>
</html>