“Este directorio contiene backups de los archivos de
configuración de los virtual hosts”.

<h1>CHESSS</h1>
<h2>índice</h2>

[Introducción](#introducción)

[Insignias](#insignias)

[Acceso al proyecto](#acceso-al-proyecto)

[Tecnologías Utilizadas](#tecnologías-utilizadas)

[Personas Desarrolladoras](#personas-desarrolladoras)

[Personas Contribuyentes](#personas-contribuyentes)

[Funcionalidades](#funcionalidades)

[Estado Del Proyecto](#estado-del-proyecto)

<p align="center">
  <img src="https://github.com/user-attachments/assets/20e13f32-e8a5-48f6-8ef4-b1da87473d8a">
</p>

## Introducción

El proyecto de desarrollo de Chess 3.0,busca añadir nuevas funcionalidades en la propia sensación de juego, algunas estéticas como poder incorporar o no a elección del jugador modificaciones en el entorno de juego, como podría ser el temporizador que indica el tiempo de cada turno que dispone el jugador para realicar su jugada pasaría a presentar la  forma de un reloj de arena, un  nuevo modo competitivo, con rangos, para que los usuarios de nuestro juego puedan medir entre ellos que tanta destreza tienen en el ajedrez, el cúal se mediría a través de un sistema de puntos.De modo que si ganas una partida se te adicionarán puntos a tu cuenta,en caso contrario se te reducirían.

## Insignias

<ul>
  <li><img alt="Apache" src="https://img.shields.io/badge/Lisense-Apache%202.0-yellow?style=plastic&labelColor=black"></li>
  <li><img alt="Version" src="https://img.shields.io/badge/Version-Chess%203.2-red?style=plastic&labelColor=black"></li>
  <li><img alt="Static Badge" src="https://img.shields.io/badge/licence-MIT-purple?style=plastic&labelColor=black"></li>
  <li><img alt="Static Badge" src="https://img.shields.io/badge/Tests-developing-green?style=plastic&labelColor=red"></li>
  <li><img alt="Static Badge" src="https://img.shields.io/badge/Release%20Date-September-orange?style=plastic&labelColor=Grey"></li>
  <li><img alt="Static Badge" src="https://img.shields.io/badge/requirejs-2.3.7-blue?style=plastic"></li>
   <li><img alt="Static Badge" src="https://img.shields.io/badge/version%20-html5-orange?style=plastic&labelColor=Grey"></li>
</ul>

## Estado Del Proyecto
  <p align="center">
    <img alt="Static Badge" src="https://img.shields.io/badge/Status-En%20Desarrolo-yellow">
  </p>


## Funcionalidades

1.-Implementación de un temporizador con forma de reloj de arena, sustituyendo al contador de tiempo tradicional.
    De modo que de tener la apariencia que se muestra en  la siguiente imagen de uno de nuestros jugadores disfrutando de nuestro juego sin haber añadido de momento el cambio en el temporizador.
<p align="center">
  <img src="https://github.com/user-attachments/assets/4a044f0f-6dc2-4e2a-b5e4-b55a0b5102d5">
</p>
Pues pasaría a presentar esta forma, la cúal estamos aún desarrollando y estudiando como incoporarla. Pero a pesar de todo podría presentar una apariencia similar a :
<p align="center">
  <img src="https://github.com/user-attachments/assets/638210e9-1452-4dd5-a1a6-475dced4137c">
</p>
2.-Incorporación de un sistema de ranking: Antiguamente teníamos acostumbrados a nuestros jugadores a simplemente poder disfrutar de chess de manera casual.Por ello para avivar a nuestra comunidad los deseos de seguir jugando en nuestra app ,
hemos decicido implementar un modo competitivo,el cuál consistirá en aumentar tu rango a medida que vas ganando.
  Tendremos 5 ligas las cuales serán : bronce, plata,oro,platino y diamante que a su vez cada una tendrá subcategorías que se representarán con números romanos de V hasta I, siendo este el borde para promocionar a la siguiente liga.
  En esta imagen que adjuntamos, podemos apreciar como sube de liga uno de nuestros desarroladores , mientras testeaba la funcionalidad, para asegurarse de que no hubiera ningún fallo: 
  <p align="center">
    <img src="https://github.com/user-attachments/assets/5ba4baed-c0aa-403f-b375-1b0e32b0d006"
  </p>
    
 ## Tecnologías Utilizadas
 
<ol>
  <li>Apache2</li>
  <li>requirejs</li>
  <li>css</li>
  <li>html5</li>
  <li>javascript</li>
  <li>node.js</li>
</ol>

## Acceso al Proyecto

<ol> Instalaciones necesarias para poder desarrollar con Chess en Debian
  <li>Instalar Git :</li> <br>
  Previamente antes de proceder directamente con la instlación deberemos de actualizar los repositorios con la intrucción siguiente :<br>
  sudo apt get update.<br><br>A posteriori ejecutaremos el comando relacionado con la instalación:<br>
  sudo apt install git.<br><br>A continuación configuraremos el nombre de usuario y correo con la que nos identificaremos en los futuros repositorios que trabajaremos, tal que:
  git config --global user.name "UsuarioGithub"<br>  git config --global user.name "correoUsuarioGithub"<br><br>
  Crearemos la clave ssh  del siguiente modo :<br> ssh-keygen -t rsa -b 4096 -C "correoGithub"<br><br>Por último deberemos de copiar el contenido de la clave pública generada y  pegarla en la sección de clave SSH de Github.<br>Para ello con la instrución:<br><br> cat < ~/.ssh/id_rsa.pub 
<br>
<li>Instalar Apache2</li>
    Antes de  implicarnos directamente con la instalación, actualizaremos los repositorios con :<br>
     sudo apt get update.A continuación ejecutaremos el comando que ya nos permitirá trabajar con Apache2:<br>
     sudo apt get install Apache2.
</ol>
    
 ## Personas desarrolladoras
 
<br> <br>
<img width="200" height="200" src="https://github.com/user-attachments/assets/177d09ae-c773-4833-b830-3cd9fa5db213">
<img width="250" height="200" src="https://github.com/user-attachments/assets/cc619e2e-491f-4af5-9569-33d3f67bcb03">
<img width="200" height="200" src="https://github.com/user-attachments/assets/58887f3d-2615-4303-b8d4-15b325c04ba9">

## Personas Contribuyentes

<br> <br>
<img width="200" height="200" src="https://github.com/user-attachments/assets/e6e2d6df-3e92-450f-b34e-76315ed6ea29">
<img width="250" height="200" src="https://github.com/user-attachments/assets/41d8ac3d-59ac-41d1-b2d0-eafa1d8eca22">
<img width="200" height="200" src="https://github.com/user-attachments/assets/657d8dce-57cd-446e-a924-41c1359d813b">
    
## Licencia.

<p align="center">
    Chess utiliza licencia MIT.
    La documentación de Chess que se guarda en la carpeta doc presenta la licencia Creative Commons.
</p>

