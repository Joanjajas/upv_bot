Bot para reservas pistas de deporte de la UPV.

# Instalación local (Únicamente MacOs de momento)

Para instalar localmente el bot únicamente hay que ejecuatar el script de instalación que se encargará de instalar todas las dependencias y de crear las carpetas necesarias.

```bash
sh scripts/setup.sh
```

Una vez ejecutado el script se creará un nuevo `LaunchAgent` que se encargará de ejecutar el bot en el background todos los jueves a las 8 de la mañana, que es cuando se abre la posibilidad de reservar pistas para la siguiente semana. Para cambiar la hora o la periodicidad de ejecución del bot se puede simplemente editar el archivo `.plist` por defecto. También se creará una nueva carpeta `bot_reservas/` bajo `Users/x/` que contendrá un archivo `reservas.toml` donde habrá que poner información sobre la pista que qeramos reservar (en el propio archivo hay un par de ejemplos comentados indicando el formato de las reservas). Además en esta carpeta se guardará un log cada vez que se ejecute el bot para poder comprobar que se ha ejecutado correctamente y que ayude a depurar posibles errores que se produzcan. Es muy importante no mover de lugar ni modificar el nombre de ningún archivo o carpeta creados, ya que si no el bot no será capaz de encontrarlos y no se ejecutará.

La contrapartida de instalar el bot localmente es que el ordenador donde este instalado tiene que estar encendido y activo cuando se vaya a ejecutar el bot. En caso contrario el bot se ejecutará la próxima vez que se encienda el ordenador, pero ya habremos perdido tiempo, por lo que es posible que las pista que se quería reservar ya esté ocupada.
