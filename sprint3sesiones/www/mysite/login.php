<?php
    $db = mysqli_connect('localhost','root','1234','mysitedb');
    function comprobar_cuenta_existe ($email,$pass){
        echo "llego a comprobar cuenta existe";

        global $db;
        $mensajetxt = "";
        $consulta = $db -> prepare("SELECT * FROM tUsuarios WHERE email=?");
        $consulta -> bind_param("s",$email);
        $consulta -> execute();
        $resultado_consulta = $consulta -> get_result();
        $consulta -> close();

        if (mysqli_num_rows($resultado_consulta) == 0){
            $mensajetxt = "¡ERROR!El email introducido no existe!";
        }
        else{ //existe el email
            $fila = mysqli_fetch_array($resultado_consulta);
            if(!password_verify($pass,$fila['contraseña'])){
                $mensajetxt = "¡ERROR!La contraseña introducida es incorrecta.";
            }
            else{
                session_start();
                $_SESSION['id_usuario'] = $fila['id'];
                echo $_SESSION['id_usuario'];
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
         if(!isset($_POST['email'])){
            echo "No se ha enviado el email.";
        }
        if(!isset($_POST['fpass'])){
            echo "no se ha enviado la contraseña.";
        }
        $email = $_POST['email'];
        $pass = $_POST['fpass'];
        if (!empty($email) and !empty($pass)){
            echo comprobar_cuenta_existe($email,$pass);
              
        }
        else{
            echo "El correo electrónico y/o la contraseña se han  enviado vacíos.";
        }
    ?>
</body>
</html>