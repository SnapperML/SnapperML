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

- Optuna [@akibaOptunaNextgenerationHyperparameter2019]: Opt una es un framework para optimización de hiperparámetros automatizada,
diseñado especialmente para ML. La característica principal que diferencia a esta herramienta de otras como Hyperopt, sk-opt, etc,
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


## Tracking de experimentos


## Hiperparametrización y entrenamiento distribuido


## Sistema de notificaciones y callbacks


## Interfaz Web


## Futuro desarrollo
