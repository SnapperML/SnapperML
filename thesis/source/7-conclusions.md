# Conclusiones, trabajos futuros y publicaciones

## Conclusiones

La reproducibilidad es un factor clave a tener en cuenta para todos los investigadores cuyos trabajos incorporen
computación. La importancia de la reproducibilidad se acentúa en el campo de ML o ciencia de datos, donde muchas de las técnicas
que se implementan son estocásticas. Existen diferentes aspectos críticos transversales que pueden facilitar o deteriorar la
reproducibilidad de experimentos, dichos aspectos críticos, que se han desarrollados en este trabajo, pueden servir como *checklist*
para los futuros proyectos de investigación. Por otro lado, se ha explora el concepto de MLOps como una solución acuñada en la industria
que propone una serie de buenas prácticas para reducir la deuda técnica de los proyectos de ML. Uno de los aspectos críticos de la
deuda técnica en sistemas ML es el de reproducibilidad, motivo por el cuál se exploran las diferentes tecnologías actuales de MLOps,
y se analiza la intersección entre la investigación y la industria. Por otro lado, se propone una tecnología de MLOps propia de código
libre llamada *ml-experiment* a partir de tecnologías de *MLOps*, con el fin crear promover la reproducibilidad. La herramienta
implementada ofrece características interesantes como soporte para HPO, control de estocasticidad, empaquetado de proyectos, etc.
Además, durante el desarrollo del trabajo, se han realizado diferentes aportaciones a la comunidad científica y a proyectos de código libre.
Como resultado de una profundización en el lenguaje *Python* para el desarrollo del *framework*, se ha llevado a cabo además un
taller de *Python Avanzado* (divido en varios seminarios) en la empresa donde trabajo. 

Por otro lado, se ha utilizado el análisis de partículas de rayos cósmicos como caso de uso para el *framework*.
El análisis de partículas de rayos cósmicos es un problema relativamente novedoso en el mundo de la física, y en este trabajo
se hace un acercamiento a la resolución del problema de clasificación de partículas primarias. Para este problema de clasificación
se recogen datos de simulaciones de unos detectores denominados WCDs, donde unos fotomultiplicadores (PMTs) capturan la señal
electromagnética y muónica de la *cascada atmosférica extensa*, la cuál se genera al colisionar la partícula primaria con la atmosférica.
Los datos utilizados para el ajuste de modelos se basan en la señal media de los PMTs con un proceso de ingeniería de características posterior.
Durante la experimentación se han implementado diferentes técnicas con un enfoque en autoencoders. En concreto, se han implementado
autoencoders variacionales, apilados, *denoising*, y combinaciones de los anteriores. Además, algunas técnicas de ML tradicional como
XGBoost y SVM también se han utilizado. De las técnicas empleadas, la que mejores resultados ofrece a priori es *XGBoost*, con un porcentaje
de precisión en el conjunto de prueba del ~87%. Los resultados de este experimento evidencian la posibilidad de identificar la
partícula de manera automática, abriendo muchas posibilidades para analizar datos ya recogidos por el observatorio e investigar este misterioso fenómeno.


## Trabajos futuros

En el capítulo de *Planificación del trabajo* se hace una breve mención al desarrollo futuro del *framework*.
En la figura \ref{fig:kanban} aparecen una lista de tareas a investigar para las versiones futuras
del *framework*. En concreto, hay tres versiones o hitos planteados.

- Una versión inicial considerada un MVP ^[Producto Mínimo Viable], que es la que se ha desarrollado en este trabajo.

- Una segunda versión centrada en la aplicación de la herramienta a la investigación,
añadiendo soporte para cuadernos de *Jupyter*, facilitando la configuración de desarrollo en local, entre otros.

- La tercera versión que se plantea está orientada a la industria, en concreto, a facilitar el paso de un desarrollo
experimental a un sistema de ML en producción. Algunas de las características a destacar de esta versión son:
soporte para definición y ejecución de *pipelines*, *CLI* para el despliegue de modelos, etc.

En términos usados anteriormente, podemos decir que la segunda versión está orientada a la *reproducibilidad* en investigación,
mientras que la tercera versión está orientada a *MLOps*. La primera versión está centrada en ambas áreas por igual.

Otra propuesta a futuro que puede ser interesante a explorar, es la comercialización del framework en forma de una plataforma en la nube.
Esta plataforma no tiene como objetivo competir con grandes como *Sagemaker*, *Google AI Platform*, o *Azure Machine Learning*. El objetivo
es desarrollar un sistema en la nube donde tanto científicos de datos como investigadores pueden aprovechar las buenas prácticas de *MLOps*
y la reproducibilidad sin preocupaciones. *MLFlow* por su parte, ofrece una plataforma con grandes características y con apoyo por la comunidad superior a sus
competidores de código libre. Pero carece de una gestión de usuarios y roles, lo cuál hace difícil su uso en empresas que requieran governanza sobre los
experimentos o modelos. Además, la comunidad de *MLFlow* tampoco ofrece un servicio en la nube gestionado, donde científicos de datos puedan
ejecutar y compartir experimentos sin tener que configurar el servidor. Esos dos puntos claves se podrían desarrollar, y junto con las características
especificadas anteriormente, conseguir un producto comercializable. En la figura \ref{fig:canvas_model} se muestra un BCM (Business Canvas Model)
donde se recoge de manera resumida un modelo de negocio para este trabajo.

![Modelo canvas de negocio para una posible comercialización del framework *ml-experiment* en forma de plataforma en la nube.](source/bmc_ml_experiment.pdf){#fig:canvas_model}

En cuanto a la clasificación de partículas primarias, es interesante destacar que es un problema que se sigue desarrollando,
y que hay cabida para multiples mejoras. Este trabajo se ha centrado en la experimentación como medio para la demostración
de un caso de uso del *framework*, pero se puede profundizar bastante más en el problema. Los datos recogidos durante la
experimentación demuestran un gran rendimiento de Xgboost, lo cuál es un indicio de que se podría explorar el uso de
ensamblados basados de este tipo para la resolución del problema. Por otro lado, los datos utilizados provienen de simulaciones,
ésto por un lado nos permite generar un muestra de entrenamiento y test muy grande (en términos de *Big Data* incluso), pero
por otro lado, también sería interesante experimentar con datos reales. De esta forma podríamos comprobar si existe o no *desfase de datos*,
entre otras asunciones.


## Publicaciones y contribuciones

Durante el desarrollo de este trabajo de Fin de Grado se han realizado varias aportaciones a la comunidad científica
y a la comunidad de código libre. Entre estas contribuciones se encuentran:

- Un artículo sobre el *framework* publicado en el congreso APSAC 2020 (cuyos proceedings serán publicados en LNEE), el cuál ha sido seleccionado para ser
extendido y publicado en la *IOP Journal of Physics*. En este artículo se hace un breve resumen de la arquitectura y las funcionalidades del *ml-experiment*,
y se exponen varios ejemplos de uso. El artículo se encuentra en *Anexo 1*.

- Como se explica en el capítulo de *Diseño y desarrollo del framework*, unas de las tecnologías fundamentales de *ml-experiment* es *MLFlow*.
Una de las funcionalidades principales de esta herramientas es *autologging*, la cual consiste en registrar de manera automática los parámetros
con los que se entrena un modelo (no solamente los que recibe el experimento), así como almacenar el modelo entrenado una vez finalizada la
ejecución. Con el objetivo de extender el uso de MLFlow y *ml-experiment* en la comunidad de científicos de datos, se han realizado dos contribuciones
al proyecto de *MLFlow*. Estas dos contribuciones tienen como objetivo ofrecer soporte para *Fastai*, para *autologging* como para el resto
de funcionalidades. Durante la realización de estas dos aportaciones en forma de PR (*Pull Requests*), se ha entablado conversación con los
desarrolladores principales del proyecto, y se ha propuesto una API concreta para esta nueva funcionalidad. En las figuras
\ref{fig:mlflow_pr_flavor} \ref{fig:mlflow_pr_autologging} \ref{fig:mlflow_conversation} se muestran los diferentes PRs realizados
al proyecto, y un ejemplo de las conversaciones con los desarrolladores principales.


![Pull Request para el soporte de *Fastai* a MLFlow](source/figures/mlflow_pr_flavor.png){#fig:mlflow_pr_flavor}

![Pull Request para la funcionalidad de *autologging* de *Fastai* a MLFlow](source/figures/mlflow_pr_autologging.png){#fig:mlflow_pr_autologging}

![Ejemplo de conversaciones con los contribuidores principales de MLFlow](source/figures/mlflow_conversation.png){#fig:mlflow_conversation}


- Seminarios de Python Avanzado en *Celtiberian*. Com se ha comentado en *Desarrollo del framework*, para la implementación del
código de este proyecto ha sido necesario una profundización en el lenguaje *Python*. A raíz de los conocimientos adquiridos durante
el proceso, se impartió un *Workshop* en *Celtiberian* (empresa en la que trabajo actualmente) sobre las técnicas aprendidas
[@domenechAntoniomdkSeminarsTalks2020].

- Workshop de SWGO [@albertScienceCaseWide2019a] en Granada. Una vez finalizado las características principales del framework y aprovechando la llegada
de algunos integrantes del equipo de LIP en Granada, se realizó un *Workshop* con un demostración en vivo del uso del
framework. Ésto permitió además validar las asunciones previas sobre los requisitos funcionales planteados al inicio
del desarrollo.

