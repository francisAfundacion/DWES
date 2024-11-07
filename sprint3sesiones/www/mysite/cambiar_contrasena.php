<?php
    $db = mysqli_connect('localhost','root','1234','mysitedb');
    function comprobar_contrasenas($vieja, $nueva,$confirmacion,$email){
        global $db;
        $mensajetxt = "";
        $consulta_contrasena_usuario = $db -> prepare("SELECT contraseña from tUsuarios where email=?");
        $consulta_contrasena_usuario -> bind_param("s",$email);
        $consulta_contrasena_usuario -> execute();
        $resultado_contrasena_usuario = $consulta_contrasena_usuario -> get_result();
        $consulta_contrasena_usuario -> close();
        $fila = mysqli_fetch_array($resultado_contrasena_usuario);

        if (!password_verify($vieja,$fila['contraseña']) ){
            $mensajetxt = "¡ERROR¡La  contraseña antigua no coincide con la que está guardada en la base de datos!";
        }
        else{
            if($vieja == $nueva){
                $mensajetxt= "¡ERROR¡La nueva contraseña no puede ser idéntica a la antigua!";
            }
            else{
                if ($nueva != $confirmacion){
                    $mensajetxt= "¡ERROR!¡La nueva contraseña no coincide con su respectiva confirmación!";
                }
            }
        }
        return $mensajetxt;
    }
    function existe_email($email){
        global $db;
        $existe = true;
        $consulta = $db -> prepare("SELECT * FROM tUsuarios where email =?");
        $consulta -> bind_param("s",$email);
        $consulta -> execute();
        $resultado_consulta = $consulta -> get_result();
        $consulta -> close();

        if (mysqli_num_rows($resultado_consulta) == 0){
            $existe = false;
        }
        return $existe;
    }
    
      
    function cambiar_contrasena_bd($nueva,$email){
        global $db;
        session_start();
        $nueva_contrasena_hasheada = password_hash($nueva,PASSWORD_DEFAULT);
        $consulta_modif_contrasena = $db -> prepare("UPDATE tUsuarios SET contraseña=? where id=?");
        $consulta_modif_contrasena -> bind_param("si",$nueva_contrasena_hasheada,$_SESSION['id_usuario']);
        $consulta_modif_contrasena -> execute();
        $consulta_modif_contrasena -> close();
        echo "consulta update => HECHO CONE EXITO";
    }
    
    
?>
<?php
    $valido=true;
    $mensajetxt="";
    if (!isset($_POST['flast_pass'])or !isset($_POST['fnew_pass']) or !isset($_POST['fnew_pass_confirm']) or !isset($_POST['email']) ){
        echo "¡ERROR!Alguno de los campos para cambiar la contraseña no han llegado correctamente!";
    }
    else{
        $last_pass = $_POST['flast_pass'];
        $new_pass = $_POST['fnew_pass'];
        $new_pass_confirm =  $_POST['fnew_pass_confirm'];

        if (empty($last_pass)) {
            echo "ERROR¡Se ha dejado vacío el campo relativo a la antigua contraseña!";
            $valido=false;
        }
        if (empty($new_pass)){
            echo "ERROR¡Se ha dejado vacío el campo relativo a la nueva contraseña!";
            $valido=false;
        }
        if (empty($new_pass_confirm)){
            echo "ERROR¡Se ha dejado vacío el campo relativo a la confirmación de la nueva contraseña";
            $valido=false;
        }
        if ($valido){
            if (existe_email($email)){
                $mensajetxt= comprobar_contrasenas($last_pass,$new_pass,$new_pass_confirm,$email);
                echo $mensajetxt;
                if ($mensajetxt == ""){
                    echo "entro en cambair contraseña, antes deivnocar la fucion";
                    cambiar_contrasena_bd($new_pass,$email);
                    echo "¡Cambiada la contraseña con éxito!";
                }
            }
            else{
                echo "ERROR¡No está registrado el email ".$email." en la base de datos!";
            }
        }
    }
?>