
<!-- CONTRIBUTING -->
# Contribuciones

Si tienes alguna sugerencia de funcionalidades o reporte de errores, puedes ayudarnos revisando los [issues del proyecto](https://github.com/ArielTriana/battle-sim/issues), si no se está trabajando en ello entonces abre un issue nuevo:

- [Reportar error](https://github.com/ArielTriana/battle-sim/issues/new?assignees=&labels=bug%2C+help+wanted&template=reporte-de-error-en-el-proyecto.md&title=%5BERROR%5D)
- [Solicitar funcionalidad](https://github.com/ArielTriana/battle-sim/issues/new?assignees=&labels=enhancement&template=solicitud-de-funci-n.md&title=%5BSOLICITUD%5D)



## Estructura del repositorio

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

## Política de Ramas

Se tendrán dos ramas principales:

- `main` donde estará una versión estable del proyecto donde todas las componentes hayan pasado los casos de prueba.
- `dev` donde se irán mezclando las ramas resultantes de nuevas funcionalidades, corrección de errores y ramas personales. Luego de que en esta rama todo funcione bien y pase los casos de prueba entonces se mezcla hacia `main`. 

## Respuesta a nuevas funcionalidades

Abre una nueva rama a partir de `dev` con el siguiente nombre `features/<funcionalidad>` y ahí implementa la funcionalidad, realiza los casos de prueba y haz un [pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) para revisar entre todos los cambios, para posteriormente aprobar los cambios.

## Arreglo de errores

Abre una nueva rama con el siguiente nombre `bug/<error>`, corrige el error, corre los casos de prueba, y haz el pull request correspondiente. Para posteriormente mezclar.

## Casos de prueba

Usted debe siempre que arregle un error o añada nuevas funcionalidades agregar casos de prueba utilizando la librería `pytest` y el plugin `pytest-cov` para verificar cuanto de su código está probando con sus casos de prueba. Antes de hacer un pull request todo su código debe pasar los casos de prueba con un coverage mayor a 90%, y no introducir que fallen los casos de prueba de otras funcionalidades.

Sus casos de prueba deben ir en la carpeta `test`. Para ejecutar los casos de pruba ejecute los comandos siguientes:

```
pytest test
pytest --cov
```

El primer comando ejecutará todos los comandos en la carpeta `test` y calculará el `coverage` de los casos de prueba.
