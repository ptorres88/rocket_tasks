# Prueba técnica Rocket

## Contenido

1. Introducción
2. Paquetes e instalación
3. Arquitectura
4. Metodología

### Introducción

Desarrollar una API en Python [con cualquier framework] que dará soporte a una aplicación web de productividad en la que los usuarios puedan gestionar una lista de tareas.

Se seleccionó *Flask* como microframework debido a la flexibilidad y facilidad, asi como por el
tiempo de prototipado.

### Paquetes e instalación

Los siguientes puntos fueron considerados para la elaboración de esta prueba técnica:

* Sistema de control de versiones (Git)
* Tipo y motor de base de datos (Postgresql)
* Pruebas unitarias (unittest)
* Ambientes de desarrollo (dev, test, prod)

Puntos importantes que no fueron considerados:

* Seguridad
* Autenticación
* Deploy automatizado

### Arquitectura

En términos de diseño y arquitectura se optó por la arquitectura más simple
posible, además de mantener un árbol de directorios como el siguiente:

+ notas
++ app
+++ api_v1_0
    __init__.py
     errors.py
     tasks.py
+++ main
    __init__.py
    exceptions.py
    models.py
++ tests
   test_api.py
   test_basics.py
++ venv
config.py
manage,py
readme.md
requirements.txt


### Metodología

1. Creación de un ambiente virtual usando _virtualenv_
2. Instalación de los paquetes requeridos (véase requirements.txt)
  * ```pip install flask```
  * ```pip install flask-script```
  * ```pip install flask-sqlalchemy```
  * ```pip install flask-migrate```
  * ... favor de revisar requirements.txt


#### Pruebas manuales de la API
```curl -H "Content-Type: application/json" -X POST -d '{"description":"xyz"}' http://127.0.0.1:5000/api/v1.0/tasks/```

```curl -H "Content-Type: application/json" -X PUT -d '{"description":"zzz"}' http://127.0.0.1:5000/api/v1.0/tasks/5```

```curl -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/api/v1.0/tasks/4```

#### postgresql

```psql postgres```

```CREATE DATABASE tasks;```

```CREATE DATABASE testtasks;```

```CREATE DATABASE devtasks;```

```postgres=# GRANT ALL PRIVILEGES ON DATABASE tasks TO usr_notas;```

```postgres=# GRANT ALL PRIVILEGES ON DATABASE testtasks TO usr_notas;```

```postgres=# GRANT ALL PRIVILEGES ON DATABASE devtasks TO usr_notas;```


#### Configuración

Algunas variables de ambiente fueron definidas y probadas en ambiente osx

~/.bash_profile

```export TEST_DATABASE_URL="postgresql://usr_notas:_rocket_@127.0.0.1/testtasks"```
```export DEV_DATABASE_URL="postgresql://usr_notas:_rocket_@127.0.0.1/devtasks"```
```export DATABASE_URL="postgresql://usr_notas:_rocket_@127.0.0.1/tasks"```

#### Flujo de ejecución

Base de datos: ```python manage.py db init```

```python manage.py db migrate -m "initializing db"```

```python manage.py db upgrade```

Correr pruebas unitarias: ```python manage.py test```

```python manage.py test_data```

Shell interactivo con app y db listos ```python manage.py shell```

Ejecutar servidor ```python manage.py run_server```

#### Documentación

visitar http://localhost:5000/apidocs
