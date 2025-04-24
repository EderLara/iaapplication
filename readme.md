# Guia de instalación de Django==5.2

~~~
pip install Django==5.2 Pillow Dotenv
~~~

## Crear aplicaciones en django:

~~~
 (env) C:\devpython\reconocimiento digital>python manage.py startapp predicciones
 (env) C:\devpython\reconocimiento digital>python manage.py startapp reportes
~~~

# Crear modelo de datos de la aplicación:
1. crear la clase: class Prediccion(models.Model): ...

# Adicionar a admin.py de la aplicacion
1. registrar el modelo de datos en el archivo admin.py de la aplicacion

## Ejecutar para utilizar base de datos:
~~~
 (env) C:\devpython\reconocimiento digital>python manage.py makemigrations predicciones reportes
 (env) C:\devpython\reconocimiento digital>python manage.py migrate
~~~

## Ejecutar para iniciar la aplicacion:

~~~
 (env) C:\devpython\reconocimiento digital>python manage.py runserver
~~~

# Pasos a seguir: