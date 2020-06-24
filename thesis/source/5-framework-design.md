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

- Registro de experimentos y seguimiento de experimentos: Uno de los pilares fundamentales de la reproducibilidad y de MLOps.
La capacidad para almacenar en una *centro de conocimiento* (base de datos, sistema de directorios, etc) parámetros, métricas, artefactos,
y otros metadatos.
- 
- Control de estocásticidad: Recoger información sobre la semilla utilizada para los diferentes generadores de números aleatorios.

- Optimización de hiperparámetros: Soporte para la ejecución de multiples experimentos en paralelo con el fin de optimizar una
o varias métricas. Además, se pueden aplicar aplicar diferentes algoritmos optimización - Bayesiana, GridSearch, etc.

- Ejecución de experimentos de manera distribuida:

- Manejo de modelos:

- Configuración de experimentos flexible y sencilla: *Deuda de configuración*.

- Instrumentalización mínima: *Código pegamento*


## Herramientas utilizadas


- Docker:

- Optuna:

- MLFlow:

- Ray


## Estructura general


## Tracking de experimentos


## Hiperparametrización y entrenamiento distribuido


## Sistema de notificaciones y callbacks


## Interfaz Web


## Futuro desarrollo
