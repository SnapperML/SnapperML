# Diseño y desarrollo del *framework*

El diseño y desarrollo de un framework orientado a la reproducibilidad es el objetivo principal
de este trabajo. Un framework abierto que soporte cualquier biblioteca de Machine Learning o Deep Learning,
y que se fundamente en los principios de reproducibilidad detallados en *Fundamentos*.

Aunque existen bastantes herramientas de MLOps que cubren en mayor o menor medida la reproducibilidad,
muchas de ellas son privadas (*Amazon Sagemaker, Google AI Platform, CometML*, etc). Y las que son de
código libre (MLFlow, Kubeflow) o híbridas (Polyaxon), no tienen algunas características importantes
como optimización de hiperparámetros *out-of-the-box*, o bien, son complejas de utilizar o configurar (véase Polyaxon).
En cuanto a las herramientas exclusivas de reproducibilidad, tanto *Sacred* como *Reprozip* son buenas soluciones
cuando se realizan análisis en local, pero carecen de soporte para la gestión de trabajos en la nube o en un *cluster* remoto.

INSERTAR TABLA COMPARATIVA

El objetivo de nuestra herramienta es el de ofrecer un marco de trabajo completo, que incluya las características esenciales
de MLOps, pero con un enfoque especial en la reproducibilidad. Como objetivo secundario, la herramienta está pensando para
facilitar un flujo de trabajo tanto en remoto como en local, con una instrumentalización del código mínima. Las características
fundamentales de *ml-experiment* son:

- **Registro de experimentos y seguimiento de experimentos:** Uno de los pilares fundamentales de la reproducibilidad y de MLOps.
La capacidad para almacenar en una *centro de conocimiento* (base de datos, sistema de directorios, etc) parámetros, métricas, artefactos,
y otros metadatos.

- **Control de estocásticidad:** Recoger información sobre la semilla utilizada para los diferentes generadores de números aleatorios.

- **Optimización de hiperparámetros:** Soporte para la ejecución de multiples experimentos en paralelo con el fin de optimizar una
o varias métricas. Además, se pueden aplicar aplicar diferentes algoritmos optimización - Bayesiana, GridSearch, etc.

- **Ejecución de experimentos de manera distribuida:** Una de las características esenciales a la hora de llevar a cabo optimización
de hiperparámetros, es la posibilidad de poder ejecutar los experimentos de manera paralela y/o distribuida. En este sentido,
*ml-experiment* permite la ejecución de los diferentes experimentos en paralelo utilizando los diferentes núcleos de la CPU
(*multiprocessing*), así como ejecutarlos de manera distribuida en un cluster remoto de Ray (ver \ref{Herramientas utilizadas}).

- **Almacenamiento y gestión de modelos:** Esta característica propia de la filosofía MLOps también es interesante desde el punto
de vista de la investigación. Primeramente, el llevar un seguimiento de los modelos entrenados durante la fase de experimentación permite,
entre otras cosas, seleccionar y aplicar los modelos que se consideren adecuados para la resolución del problema. De otra forma, se debería
seleccionar el mejor experimento y replicar todo el proceso hasta obtener el modelo. Por otro lado, si se almacenan los modelos,
y por algún motivo los datos y procedimientos no se pueden compartir con la comunidad científica, al menos se pueden compartir los modelos
acercando el estudio a la *Investigación Replicable* (ver \ref{Reproducibilidad})

- **Configuración de experimentos flexible y sencilla**: Con el fin de reducir la *Deuda de configuración*, *ml-experiment*
ofrece una manera sencilla de definir experimentos y trabajos de optimizar de hiperparámetros utilizando ficheros 
YAML o JSON.

- **Instrumentalización mínima:** Como se ha detallado en la sección de \ref{Deuda técnica}, uno de los *anti patrones*
a evitar en los proyectos de ciencia de datos es el uso *código pegamento*. Por este motivo, nuestro objetivo a la hora
de diseñar *ml-experiment* es el de evitar grandes cambios en el código existente para entrenamiento o análisis,
es decir, reducir la instrumentalización. Gracias a esto, evitamos dicho *anti patrón*.


## Herramientas utilizadas

*ml-experiment* se fundamenta en un pequeño conjunto de herramientas de código abierto muy potentes y activas.
Entre las principales herramientas utilizas, cabe destacar:

- Docker [@merkel2014docker]:  Docker es una plataforma de contenedores software que ayuda a empaquetar aplicaciones
junto con sus dependencias en forma de contenedores para asegurar que la aplicación se ejecuta independientemente
al sistema operativo anfitrión. Un contenedor docker es una unidad software estandarizada que se crea en tiempo real para
desplegar una aplicación o entorno particular. Los contenedores pueden ser entornos - Ubuntu, CentOs, Alpine, etc - o
puede ser aplicaciones enteras - contenedor de NodeJS-Ubuntu por ejemplo.

- Optuna [@akibaOptunaNextgenerationHyperparameter2019]: Optuna es un framework para optimización de hiperparámetros automatizada,
diseñado especialmente para [!ml]. La característica principal que diferencia a esta herramienta de otras como Hyperopt, sk-opt, etc,
es la API *define-by-run*, la cuál es una API imperativa con la que se pueden construir espacios de búsqueda de hiperparámetros de
manera dinámica. Además, soporta diferentes algoritmos de optimización:
TPE, Hyperband, GridSearch, etc [@bergstraAlgorithmsHyperParameterOptimization2011].

- MLFlow [@zahariaAcceleratingMachineLearning2018]: Ver sección de *Fundamentos*.

- Ray [@moritzRayDistributedFramework2018a]: Ray es un framework orientado al desarrollo y ejecución de aplicaciones distribuidas.
Originalmente, este proyecto fue propuesto para el entrenamiento de modelos de Aprendizaje por Refuerzo (RL) [@sutton1998introduction]
distribuido, pero posteriormente se adaptó para cualquier aplicación distribuida en Python. De esta forma, Ray se puede considerar
un framework de propósito general para la computación en clusters. Algunos experimentos requieren de una preprocesado
de datos costoso, o de un entrenamiento de larga duración. Para satisfacer estos requisitos, *Ray* propone una interfaz
unificada con la que se pueden definir dos tipos de tareas: Tareas paralelas, tareas basadas en el modelo *actor* [@hewittActorModelComputation2015].
Las tareas paralelas permiten distribuir la computación de manera balanceada, procesar grandes cantidades de datos, y
recuperarse de errores. Por otro lado, el uso de Actores permite manejar computaciones con estado, y compartir ese estado entre diferentes
nodos de manera sencilla.


## Estructura general

![Diagrama de la estructura general de *ml-experiment*](source/figures/ml_experiment_overview.png){#fig:framework_overview width=300px}

El núcleo principal de *ml-experiment* está divido en 4 módulos (ver Figura \ref{fig:framework_overview}) con los que el usuario interacciona
indirecta o directamente a través de una [!cli] y de una biblioteca de *Python*. El módulo *JobRunner* es el encargado de ejecutar un
código instrumentalizado ^[Un código instrumentalizado comprende un código de Python al que se le aplican los cambios pertinentes para poder utilizarse
con el framework. En concreto, estos cambios se basan en utilizar la biblioteca de Python del *framework*.
El objetivo de *ml-experiment* es que estos cambios sean mínimos.] en un cluster de *Ray*, en un contenedor de Docker,
o en local (utilizando varios procesos si se emplea HPO).  El módulo de seguimiento (*Tracking*) ofrece una abstracción sobre
*MLFlow* para el registro de experimentos, parámetros, métricas, y artefactos. Además, recoge automáticamente otra información
relevante sobre el experimento como el entorno software y hardware,
las semillas de los generadores aleatorios, entre otros. El módulo de empaquetado *Packaging* se encarga de generar una
versión del proyecto que se pueda distribuir fácilmente utilizando la tecnología **Docker** para generar un *imagen* de todas las 
dependencias. El objetivo principal de este módulo es el de simplificar la reproducibilidad de trabajo científico entre diferentes
entornos heterogéneos mediante el uso de *contenedores*. Los cuatro módulos principales que componen el *framework* dependen de una
"centro de conocimiento" (*Knowledge Center*). El *Knowledge Center* se compone de una base de datos SQL y un sistema  de ficheros
(local, compartido, o en la nube). Las métricas, parámetros, y otros metadatos se almacenan en la base de datos SQL, mientras
que los artefactos se almacenan en el sistema de ficheros. La gestión de ambos sistemas de información se delega a *MLFlow*.


## Instrumentalización de código y ejecución del código

El primer paso para poder utilizar el framework es el de instrumentalización. *ml-experiment* ofrece una biblioteca
de Python minimalista con el que se pueden definir *trabajos* a ejecutar. En Listing \ref{instrumented_code} se muestra 
la forma de instrumentalizar un código de Python. Básicamente, se define el punto de entrada del programa *main*
^[El nombre no es relevante. Simplemente tiene que ser la función que se llame al ejecutar el script] con los parámetros
del experimento, y se envuelve con el decorador *\@job*. Toda la información sobre el uso del framework (biblioteca y [!cli] incluida)
se encuentra recogida en el *Manual de Usuario* (ver *Anexo 2*).

``` {#instrumented_code .python caption="Ejemplo de código instrumentalizado."}
from ml_experiment import job

@job
def main(param1, param2, param2):
    # Training code goes here

if __name__ == '__main__':
    main()
```

El uso del decorador *\@job* en el punto de entrada del programa hace imposible poder ejecutar el script directamente. Para poder
ejecutar este código es necesario utilizar las [!cli] de *ml-experiment* (ver *CLI Reference* en *Manual de Usuario*).
Existen tres formas diferentes de ejecutar el código con la [!cli]. La forma principal, la cuál recomienda encarecidamente, es mediante un fichero
de configuración YAML o JSON (ver *YAML/JSON Specification* en *Manual de Usuario*). En Listing \ref{yaml_example} se muestra un ejemplo
de fichero de configuración. En ese mismo fichero de configuración se definen el nombre, parámetros, y el script a ejecutar. Además,
se puede definir en el la configuración de *Docker* o *Ray* en caso de querer ejecutar en un contenedor o cluster. Una vez definido
ese fichero, para ejecutar el código mediante la [!cli] se utiliza el siguiente comando ^[El directorio donde se ejecuta el comando debe tener
acceso al script. Es decir, la ruta definida en el campo *run* del fichero de configuración debe ser una ruta absoluta o una ruta
relativa al directorio donde se ejecuta el comando.]:

``` {#yaml_example .yaml caption="Ejemplo de comando para la ejecución del código definido en Listing \ref{instrumented_code} usando el fichero de configuración de Listing \ref{yaml_example}"}
ml-experiment --config_file=my_experiment.yaml 
````

``` {#yaml_example .yaml caption="Ejemplo de fichero de configuración para Listing \ref{instrumented_code}"}
name: My Experiment

params:
  param1: "hello"
  param2: "ml-experiment"
  param3: 1

run:
  - path/to/script.py
```

La segunda opción para ejecutar el código es utilizar directamente la [!cli]. Esta opción es menos recomendable que la anterior,
principalmente porque los ficheros de configuración facilitan la *replicabilidad* de experimentos, mientras que si se usa la [!cli],
para poder replicar los experimentos es necesario o bien compartir el comando ejecutado, lo cuál es poco legible y susceptible a cambios
en la [!cli], o compartir los parámetros con los que se ha ejecutado manualmente, sin disfrutar de las ventajas del control de versiones
por ejemplo. En Listing \ref{cli_example} se muestra un ejemplo de ejecución de experimentos manualmente.

``` {#cli_example .yaml caption="Ejemplo de comando para la ejecución del código definido en Listing \ref{instrumented_code} usando el fichero de configuración de Listing \ref{yaml_example}"}
ml-experiment \
    --name="My experiment" \
    --params="{'param1': 'hello', 'param2': 'world', 'param3': 1}"
    path/to/script.py
````

La tercera opción consiste en una combinación de las dos anteriores. La [!cli] de *ml-experiment* permite utilizar un fichero de configuración
como base y modificar ciertos campos manualmente. En Listing \ref{cli_yaml_combination} se muestra un ejemplo donde se utiliza el fichero
de configuración definido en \ref{yaml_example}, y se sobreescribe el parámetro "param3". El diccionario definido tanto en *--params*
como *--param_space* se combina con aquel especificado en el fichero de configuración, tomando prioridad el de la [!cli] en caso de colisión
entre claves.

``` {#cli_yaml_combination .yaml caption="Ejemplo de comando donde se combina la especificación de un experimento de un fichero YAML con parámetros introducidos por el usuario mediante la CLI."}
ml-experiment \
    --config_file=my_experiment.yaml
    --params="{'param3': 20}"
````


### Ejecución de experimentos en Docker o Ray





## Tracking de experimentos

El registro y seguimiento de experimentos es un aspecto fundamental de la reproducibilidad, y uno de los pilares de *MLOps* (ver *Fundamentos*).
*MLFlow* ofrece un potente interfaz para el "logging" de parámetros, métricas, y artefactos. La forma de registrar métricas en un experimento
con MLFlow es la siguiente:

```python
with mlflow.start_run():
    mlflow.log_metric(key="quality", value=)
```

Como vemos, la interfaz es fácil de utilizar, el problema principal no es la dificultad de uso de *MLFlow*, sino la mantenibilidad del código.
Los parámetros de un experimento pueden cambiar con el tiempo, haciendo que los parámetros que se registren sean obsoletos, o que los
nuevo parámetros no se registren. Estos problemas se hacen acentúan al tener que mezclar código ML con código de relativo al seguimiento.
El objetivo de *ml-experiment* es el de ofrecer una abstracción sobre la API de *Tracking* de *MLFlow* con el fin de asegurar unas buenas
prácticas de desarrollo y reducir la deuda técnica como se ha comentado anteriormente. La forma en la actúa *ml-experiment* es automatizando
el registro de parámetros, métricas, y artefactos. Cuando un código se instrumentaliza (como se muestra en Listing \ref{instrumented_code_with_return}),
se realiza un seguimiento automático de los los parámetros de la función de entrada (*main*). Es decir, cuando un experimento se ejecuta, los parámetros
de entrada se almacenan en el servidor de *MLFlow*. Además de los parámetros, la función principal puede devolver una tupla de dos diccionarios, un
primer diccionario para las métricas ^[La clave es el nombre de la métrica y el valor es un número entero o flotante], y el segundo diccionario para los
artefactos ^[La clave es un identificador o nombre arbitrario para el artefacto, y la clave es la ruta relativa o absoluta al mismo].


``` {#instrumented_code_with_return .python caption="Ejemplo de código instrumentalizado donde se devuelve un diccionario el diccionario de métricas y el de artefactos."}
from ml_experiment import job

@job
def main(param1, param2, param2):
    {'metric1': 1.0}, {'artifact1': 'path/to/artifact'}

if __name__ == '__main__':
    main()
```

Cuando se ejecuta un experimento, MLFlow por su parte almacena ciertos metadatos, como el nombre el identificador del ultimo *commit* antes de la ejecución del código,
el fichero de Python ejecutado, nombre de usuario en el sistema, etc. Además de esta información, *ml-experiment* almacena otros metadatos teniendo en cuenta los
aspectos críticos de la reproducibilidad descritos en *Fundamentos*. Estos metadatos son los siguientes:

- **Información hardware**: Especificaciones de la CPU y de la GPU, entre los que se incluye, nombre del procesador y de la tarjeta gráfica, cantidad de memoria de la GPU,
versión de los drivers de CUDA [@CUDAToolkit2013], entre otros.

- **Información software**: Se hace una captura de todos los paquetes de Python disponibles en la ejecución del experimento. Esa información se almacena en un fichero
*requirements.txt* y se sube al servidor de *MLFlow*. Por otro lado, se recoge información sobre la versión del interprete de Python utilizado.

- **Logs**: La salida de la consola se almacena en un fichero y se sube también a *MLFlow*.

- **Semilla de generadores aleatorios**: Por último, cuando un meneador de números aleatorios se alimenta con una determinada semilla, *ml-experiment* recoge esa semilla
y la almacena como metadatos. El framework soporta los generadores aleatorios de Tensorflow, Pytorch, Numpy [@NumPy], y el nativo de Python (módulo *random*)


## Hiperparametrización y entrenamiento distribuido

*ml-experiment* tiene soporte de primera clase para [!hpo]. El framework permite ejecutar multiples experimentos simultáneamente en un entorno local o remoto.
Además, permite la asignación de recursos de CPU y GPU para el trabajo de optimización, es decir, podemos especificar el número o fracción de
cores y [!+gpu] (si hay disponible), y el framework distribuirá las tareas entre los recursos disponibles (ver *Hyperparameter Tuning* en *Manual de Usuario*).
Como ejemplo, Listing \ref{group_config} muestra una especificación de un trabajo de de HPO donde se ejecutan 12 experimentos. Los parametros *param1* y param2*
se muestrean de una distribución categórica ^[Se selecciona un elemento de la lista de manera aleatoria con la misma probabilidad.] y de una distribución uniforme
respectivamente, mientras que el parámetro *param3* tiene un valor fijo. Además, de los recursos disponibles en el sistema, se utilizan 4 núcleos exclusivamente.
A nivel de ejecución, el campo *ray_config* permite añadir la dirección del cluster de Ray para ejecutar en remoto, en caso de no especificar ninguna dirección,
o utilizar "localhost", *ml-experiment* crea un cluster de Ray en local ^[Un cluster de Ray en local implica que se levantan varios procesos (num_cpus), y la
los experimentos se divide entre cada proceso (num_trials / num_cpus).].

A la hora de definir trabajos de HPO, el término utilizado en el framework es el de **grupo**. Un grupo es un tipo de trabajo en el que se
ejecutan varios experimentos a la vez. Para poder definir un *grupo* utilizando la especificación YAML/JSON, es necesario añadir el campo
*kind* e igualarlo a "group". De este forma, *ml-experiment* reconoce que el trabajo corresponde a un grupo y configura la infraestructura
correspondiente. El objetivo de un trabajo de HPO (grupo) es el de optimizar un métrica específica, ya sea minimización o minimización,
en otras palabras, encontrar el conjunto de parámetros que maximice o minimice la métrica del experimento 
^[Un experimento puede tener varias métricas y todas ellas quedan recogidas por el módulo de *Tracking*,
pero de momento no hay soporte para optimización  multiobjetivo.].

Por otro lado, *ml-experiment* permite definir el *sampler* y *pruner* de **Optuna**. Un *pruner* es un algoritmo que indica cuando
un experimento debe ser "podado" o no. Podar un experimento significa terminar su ejecución antes de tiempo. Cuando un experimento
no es prometedor, es decir, cuando tiene muy poca probabilidad de mejorar la mejor métrica registrada previamente, los *pruners*
permiten terminar la ejecución ahorrando recursos de computación y tiempo.
Un *sampler* es una implementación de una estrategia de muestreo, es decir, una forma concreta con la que generar los parámetros
de un experimento a partir de un espacio de hiperparámetros. Ese espacio de hiperparámetros viene definido por el campo *param_space*.
*ml-experiment* soporte varias distribuciones de parámetros que cubren la mayoría de necesidades de un experimento de ML
(ver *YAML/JSON Specification* en *Manual de Usuario*). Además, *ml-experiment* soporta todos los *samplers* y *pruners* de *Optuna*.

``` {#yaml_example .yaml caption="Ejemplo de fichero de configuración para un grupo de experimentos sobre Listing \ref{instrumented_code}"}
name: My Experiment
kind: group
num_trials: 12
sampler: TPE

param_space:
  param1: choice(["hello", "world"])
  param2: uniform(0.001, 100)

params:
  param3: 1

metric:
  name: metric1
  direction: maximize

ray_config:
  num_cpus: 4

run:
  - path/to/script.py
```

## Sistema de notificaciones y callbacks


## Interfaz Web


## Desarrollo del framework

1. Calidad del código

2. Python Avanzado.

[@domenechAntoniomdkSeminarsTalks2020]


## Futuro desarrollo
