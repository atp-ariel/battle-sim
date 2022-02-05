<div id="top"></div>

[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![Pull Request][pull-request]][pull-request-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ArielTriana/battle-sim">
    <img src="https://ik.imagekit.io/atpariel/battle-sim_j-a6B50ZX?updatedAt=1634232107705" alt="Logo" width="100" height="100">
  </a>

<h1 align="center">Battle Sim</h3>

  <p align="center">
    Software para simular batallas bélicas entre ejércitos. Proyecto que vincula conocimientos de Inteligencia Artificial, Simulación y Compilación.
    <br />
    <a href="https://github.com/ArielTriana/battle-sim/blob/dev/doc/reporte%20final/Informe.pdf"><strong>Ver informe »</strong></a>
    <br />
    <a href="https://github.com/ArielTriana/battle-sim/raw/main/doc/reporte%20final/Informe.pdf"><strong> Descargar informe</strong></a> 
    <br />
    <br />
    <a href="https://github.com/ArielTriana/battle-sim/issues/new?assignees=&labels=bug%2C+help+wanted&template=reporte-de-error-en-el-proyecto.md&title=%5BERROR%5D">Reportar Error</a>
    ·
    <a href="https://github.com/ArielTriana/battle-sim/issues/new?assignees=&labels=enhancement&template=solicitud-de-funci-n.md&title=%5BSOLICITUD%5D">Solicitar Función</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Tabla de contenidos</summary>
  <ol>
    <li>
      <a href="#acerca-del-proyecto">Acerca del proyecto</a>
      <!--<ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>-->
    </li>
    <li>
      <a href="#primeros-pasos">Primeros pasos</a>
      <ul>
        <li><a href="#prerequisitos">Prerequisitos</a></li>
        <li><a href="#installaciṕn">Instalación</a></li>
      </ul>
    </li>
    <li><a href="#uso">Uso</a></li>
    <li><a href="#contribuciones">Contribuciones</a>
        <ul>
            <li><a href="#política-de-ramas">Política de ramas</a></li>
            <li><a href="#estuctura-del-repositorio">Estructura del repositorio</a></li>
            <li><a href="#respuesta-a-nuevas-funcionalidades">Respuesta a nuevas funcionalidades</a></li>
            <li><a href="#arreglo-de-errores">Arreglo de errores</a></li>
            <li><a href="#casos-de-prueba">Casos de prueba</a></li>
        </ul>
    </li>
    <li><a href="#licencia">Licencia</a></li>
    <li><a href="#desarrolladores">Desarrolladores</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Acerca del proyecto

A lo largo de la historia, los conflictos bélicos han estado fuertemente ligados al desarrollo de la humanidad. Existen pruebas que desde la prehistoria, los hombres luchaban entre ellos por tierras y recursos naturales. Con el pasar del tiempo, los hombres fueron evolucionando, y así también lo hicieron los objetivos de los conflictos bélicos, los armamentos y estrategias utilizados en estos conflictos.

El  objetivo  de  este  proyecto  es  el  desarrollo  de  un  programa  que  permita  la  simulación  de diferentes batallas que se hayan producido en un pasado distante, en  épocas más recientes e incluso simular batallas futuristas o con elementos de fantasía. Además se podrían simular batallas entre diferentes épocas, por ejemplo podríamos enfrentar 300 soldados armados con las más modernas armas contra 1000 soldados armados con espadas y escudos.

Para  esto  se  tienen  pensado  los  siguientes  aspectos  que  van  a  ser  fijos  en  cada  una  de  las simulaciones:

- La existencia de un mapa o terreno donde ocurre el enfrentamiento.
- Las acciones serán por turnos.
  
Se tiene la idea de poder implementar una opción para que el usuario pueda definir las reglas de la simulación a través del lenguaje de dominio específico, como por ejemplo: definir si las unidades serán destruidas cuando se acaben sus puntos de vida o serán baja al recibir un único impacto, si algunas en específico solo pueden ser destruidas por otras unidades que cumplen ciertas características, etc. Así  mismo  el  usuario  debe  definir  cuál  es  el  objetivo  de  cada  bando  y  poder  elaborar  una estrategia para cada uno. Cuando un bando consiga su objetivo se declara como ganador.

<p align="right">(<a href="#top">volver arriba</a>)</p>




### Construido con

* [Python](https://python.org)
* [Pytest](https://pytest.org)
* [Pytest-cov](https://pytest-cov.readthedocs.io)
* [Typer]([https://https://typer.tiangolo.com](https://typer.tiangolo.com/)/)

<p align="right">(<a href="#top">volver arriba</a>)</p>



## Primeros pasos

Siga la guía de instalación para ejecutar el proyecto de forma local.

### Prerequisitos

Es necesario tener Docker instalado en su ordenador, si usted no tiene Docker obedezca [las siguientes instrucciones](https://docs.docker.com/get-docker/)

### Instalación

Ejecute los siguientes comandos en la consola:

1. `docker build -t battle_sim --rm .`
2. `docker run -it --name compiler --rm battle_sim`

<p align="right">(<a href="#top">volver arriba</a>)</p>



## Uso

Para ejecutar el compilador del lenguaje siga las instrucciones:

### Compilar en un archivo .py

Para obtener el compilado a .py, ejecute `python -m src <bs-path> --py=<py-path> --no-run`, si `py-path` no es provisto, el archivo generado se salvará en el directorio de `bs-path`. 

### Para compilar y ejecutar el archivo

Ejecute la siguiente linea `python -m src <bs-path>`

<p align="right">(<a href="#top">volver arriba</a>)</p>


<!-- CONTRIBUTING -->
## Contribuciones

Si tienes alguna sugerencia de funcionalidades o reporte de errores, puedes ayudarnos revisando los [issues del proyecto](https://github.com/ArielTriana/battle-sim/issues), si no se está trabajando en ello entonces abre un issue nuevo:

- [Reportar error](https://github.com/ArielTriana/battle-sim/issues/new?assignees=&labels=bug%2C+help+wanted&template=reporte-de-error-en-el-proyecto.md&title=%5BERROR%5D)
- [Solicitar funcionalidad](https://github.com/ArielTriana/battle-sim/issues/new?assignees=&labels=enhancement&template=solicitud-de-funci-n.md&title=%5BSOLICITUD%5D)



### Estructura del repositorio

El repositorio tiene la siguiente estructura, sígala para contribuir:

```
battle-sim
|- doc
|  |_ (aquí la documentación)
|- src
|  |_ (aquí los códigos fuentes del proyecto)
|- test
|  |_ (aquí los casos de prueba)
|- LICENSE
|- README.md
|_
```
### Política de Ramas

Se tendrán dos ramas principales:

- `main` donde estará una versión estable del proyecto donde todas las componentes hayan pasado los casos de prueba.
- `dev` donde se irán mezclando las ramas resultantes de nuevas funcionalidades, corrección de errores y ramas personales. Luego de que en esta rama todo funcione bien y pase los casos de prueba entonces se mezcla hacia `main`. 

### Respuesta a nuevas funcionalidades

Abre una nueva rama a partir de `main` con el siguiente nombre `features/<funcionalidad>` y ahí implementa la funcionalidad, realiza los casos de prueba y haz un [pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) para revisar entre todos los cambios, para posteriormente aprobar los cambios.

### Arreglo de errores

Abre una nueva rama con el siguiente nombre `bug/<error>`, corrige el error, corre los casos de prueba, y haz el pull request correspondiente. Para posteriormente mezclar.

### Casos de prueba

Usted debe siempre que arregle un error o añada nuevas funcionalidades agregar casos de prueba utilizando la librería `pytest` y el plugin `pytest-cov` para verificar cuanto de su código está probando con sus casos de prueba. Antes de hacer un pull request todo su código debe pasar los casos de prueba con un coverage mayor a 90%, y no introducir que fallen los casos de prueba de otras funcionalidades.

Sus casos de prueba deben ir en la carpeta `test`. Para ejecutar los casos de pruba ejecute los comandos siguientes:

```
python -m pytest --cov
```

El primer comando ejecutará todos los comandos en la carpeta `test` y calculará el `coverage` de los casos de prueba.

<p align="right">(<a href="#top">volver arriba</a>)</p>



<!-- LICENSE -->

## Licencia

El siguiente proyecto está distribuido bajo MIT License. Ver [LICENSE.txt](https://github.com/ArielTriana/battle-sim/blob/main/LICENSE) para más información.

<p align="right">(<a href="#top">volver arriba</a>)</p>



<!-- Contributors -->

## Desarrolladores

<table align="center">
   <tr>
       <td align="center">
            <a href="https://github.com/rocioog00"><img height='60' src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/56322127?v=4&h=300&w=300&fit=cover&mask=circle"/></a>
            <br/>
            Rocio Ortiz Gancedo
            <br/>
            🤔📝💻
            <br/>
            <a href="https://github.com/rocioog00"><img src="https://upload.wikimedia.org/wikipedia/commons/a/ae/Github-desktop-logo-symbol.svg" height="18"></a>
            <a href="https://t.me/rocioog"><img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" height="18"/></a>
            <a href="mailto:rocio.ortiz@estudiantes.matcom.uh.cu"><img src="https://upload.wikimedia.org/wikipedia/commons/9/97/Android_Email_4.0_Icon.png" height="18"/></a>
       </td>
       <td align="center">
            <a href="https://github.com/CTS-crypto"><img height='60' src="https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/72420685&v=4&w=300&h=300&fit=cover&mask=circle&fit=cover"/></a>
            <br/>
            Carlos Toledo Silva
            <br/>
            💻🤔📝
            <br/>
            <a href="https://github.com/CTS-crypto"><img src="https://upload.wikimedia.org/wikipedia/commons/a/ae/Github-desktop-logo-symbol.svg" height="18"></a>
            <a href="https://t.me/cts-crypto"><img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" height="18"/></a>
            <a href="mailto:carlos.toledo@estudiantes.matcom.uh.cu"><img src="https://upload.wikimedia.org/wikipedia/commons/9/97/Android_Email_4.0_Icon.png" height="18"/></a>
       </td>
       <td align="center">
            <a href="https://github.com/ArielTriana"><img height='60' src="https://images.weserv.nl/?url=avatars.githubusercontent.com/u/61637781?v=4&h=300&w=300&fit=cover&mask=circle"/></a>
            <br/>
            Ariel Alfonso Triana Pérez
            <br/>
            💻🤔📝
            <br/>
            <a href="https://github.com/atp_ariel"><img src="https://upload.wikimedia.org/wikipedia/commons/a/ae/Github-desktop-logo-symbol.svg" height="18"></a>
            <a href="https://t.me/atp_ariel"><img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" height="18"/></a>
            <a href="mailto:usich37@gmail.com"><img src="https://upload.wikimedia.org/wikipedia/commons/9/97/Android_Email_4.0_Icon.png" height="18"/></a>
       </td>
   </tr>
</table>


<p align="right">(<a href="#top">volver arriba</a>)</p>






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ArielTriana/battle-sim.svg?style=for-the-badge
[contributors-url]: https://github.com/ArielTriana/battle-sim/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues/ArielTriana/battle-sim.svg?style=for-the-badge
[issues-url]: https://github.com/ArielTriana/battle-sim/issues
[license-shield]: https://img.shields.io/github/license/ArielTriana/battle-sim.svg?style=for-the-badge
[license-url]: https://github.com/ArielTriana/battle-sim/blob/master/LICENSE.txt
[pull-request]: https://img.shields.io/github/issues-pr/ArielTriana/battle-sim.svg?style=for-the-badge
[pull-request-url]: https://github.com/ArielTriana/battle-sim/pulls