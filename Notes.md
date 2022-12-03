# Notas del de la crecion de la rest api

ERRORES
        un server error cuandondo el token expira (time 7:39)

**Creacion del development enviroment**

*   virtualenv -p python3 envName
        El modulo de python virtualenv crea un entorno vitual con ese name. Es como maquina virtuales
        Esto es util para poder instalar diferentes version de python dependiendo del projecto que estaremos desarrollando. Ademas se puede instalar paquetes exclusivo para este projecto

* Ctrg + shif + p (Python: Select interpreter)
    Con esto selecionamo la version dy python en visual s code para trabajar con este
  
*   source EnvName/bin/activate
        activa el entor no virtual le la terminal para trabajar con este

*   deactivate
        para salir del entorno de trabajo

*   pip list
        para var la lista de los paquetes instalados


# Instalacion de FastAPI¶
        https://fastapi.tiangolo.com/tutorial/

*        pip install "fastapi[all]"
                todos los package se intalaran en lib
        
*       pip freeze
        pip list
                par ver los paqutes inatalado

# Server start
*    uvicorn main:app
        inicializa el web server


# Pyton own package
  Crear el dir app y dentro el file:
   __ini__py
        este file permite que python reconosca tu dir como un paquete

# Reiniciar la app depues de ser movida al dir app
*   uvicorn app.main:app --reload
        --reload
                mantiene el server en ejcucion 

# Objest Relacional Mapper(ORM)
        Layer of abstraction that sits between the database and us.
        We can perform all database operations though traditional python code. NO more SQL

        1 Nosotros interactuamos con el ORM
        2 El ORM interactua con la db

        Los mas habituales son:
                Sqlalchemy

        Source
          orm.png

          https://www.sqlalchemy.org/
          https://docs.sqlalchemy.org/en/14/orm/session.html


# Creacion de los modelos 
        para la estructura de los datos con los que se van a interactuar

# Creacion schema model
        pydantic model define la extrutura del request and response . con esto se controla exactamente qu es lo que queremos del user al crear un post y que recbira  como repuesta

# ORM Model para

# Creacion de user

# password hasing
        https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

# get_user funcin 
        para manejar informaciones especificas sobre un user

# Router Divicion de la app en files 

# atuthentication JWT

# enviroment
        para cambiar variables que cambien dependiendo en que entorno se encuentren
        En postman en la sessin de Env configuran los entornos

# automatizando el losging time par no estar losgeandose cada x tiempo
        esto es para cuando el tiempo de expiracin del token es cotto
        Esta automatizacion la haremos com codigo para Thunder


# Relation

# Query paramethers

# Enviroment variable in my machine

# likes o vote system

# implemtntar el numero de votos en los post (JOIN TABLES)

# alembic
Para hacer cambio en la DB
        para potenciar sqlalchemy. para cuando agregeumo una columa a las tablas estas se puedan añadir automaticamente a las tablas

        alembic --help
                for the help
        
        alembic init alembiDB
                crea un dir con el name allembiDB
        alembic upgrade 74db0f4d1be7
                crea primer table
        alembic current
                mustra la el numero de la revision actual

# cors implemntation

# requirements.txt create
        pip install requirements.txt
                para instalar las dependencias del projecto

