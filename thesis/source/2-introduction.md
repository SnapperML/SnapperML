# Introducción


## El problema de la reproducibilidad

Hoy en día, los proyectos de ciencia de datos se desarrollan de una forma desestructurada en la mayoría casos,
lo cual lo hacen muy difícil de reproducir. Siendo conscientes de las dificultades que conlleva ser rigurosos con el
desarrollo de este tipo de trabajos para asegurar la reproducibilidad, este trabajo presenta un framework que facilita 
el rastreo de experimentos y la operacionalización del machine learning, combinando tecnologías open source existentes
y apoyadas fuertemente por la comunidad. Estas tecnologías incluyen Docker, MLFlow, Ray, entre otros.

El framework ofrece un flujo de trabajo concreto para el diseño y ejecución de experimentos en un entorno local o remoto.
Para facilitar la integración con código existente, se ofrece además un sistema de rastreo automático para los frameworks de
Deep Learning más famosos: Tensorflow, Keras, Fastai, además de otros paquetes de Machine Learning como Xgboost y Lightgdm.
Por otro parte, se ofrece un soporte de primera clase para el entrenamiento de modelos y la hiperparametrización en entornos
distribuidos. Todas estas características se hacen accesibles al usuario por medio de un paquete de Python con el que instrumentalizar
el código existente, y un CLI con el que empaquetas y ejecutar trabajos.

La reproducibilidad es un reto en la investigación moderna y produce bastante debate [@Hutson725] [@freire_et_al:DR:2016:5817] [@freire2].
Entre los diferentes tipos de trabajos reproducibles, este trabajo se centra en trabajos computacionales, desarrollando
un flujo de trabajo específico bastado en losn principios de Control de Versiones, Automatización, Rastreo y Aislamiento
del entorno [@Olorisade2017ReproducibilityIM] [@10.1371/journal.pcbi.1005510]. El control de versiones permite 
rastrear los diferentes ficheros del proyecto y sus cambios, así como facilitar la colaboración. Automatizar los procesos,
desde ficheros de shell hasta pipelines de alto nivel, permite que otra persona puede reproducir los pasos del trabajo
fácilmente. Estos pasos incluyen: creación de ficheros, preprocesado de datos, ajuste de modelos, etc. Durante la ejecución
de estos pasos, se generan gráficos, artifacts, nuevos datos, etc. Por este motivo, es necesario proporcionar una forma sistemática
de recolectar toda esa información generada y mostrarla desde un único punto.

Finalmente, el aislamiento del sistema anfitrión mediante el uso de contenedores o máquinas virtuales, permite ampliar el ámbito de control
sobre los experimentos, proporcionando un "escenario común" para la ejecución de los mismo. De otra forma,
los factores externos al proyecto, como las versiones de las paquetes de análisis, los drivers de la GPU, o
la propia versión del sistema operativo donde se ejecuten pueden incrementar la estocásticidad del experimento.
Otra ventaja de aislar las dependencias y la imagen del sistema operativo (entre otros factores), combinado con la automatización
 de los diferentes procesos, es que que facilita enormemente la ejecución de los experimentos y los hace dependiente de la
 plataforma, evitando tener que instalar las diferentes dependencias, modificar ficheros de configuración, etc. Por no decir
 que las dependencias del proyecto pueden ser incompatibles con las globales instaladas en el sistema.


## Clasificación de primarios

Uno de los misterios de Astrofísica a día de hoy es la forma en la que se generan los rayos cósmicos de ultra alta energía (UHECRs).
Para comprender mejor el comportamiento de estas partículas, el observatorio de Pierre Auger fue construido.
Supone un proyecto muy ambicioso y uno de los experimentos de mayor magnitud a día de hoy.
Un area de 3000 kilómetros cuadrados se ha diseñado y construido para alojar detectores de agua Cherenkov (WCDs).
Estos detectores son unos tanques grandes de agua ultra-pura donde se detecta la radiación de Cherenkov, normalmente
utilizando fotomultiplicadores (PMTs). Estos detectores son capaces de medir la señal generada por
las partículas mientras viajan a través del agua. Las interacciones de los UHECRs con las moléculas de aire de la
atmósfera producen lo que se conoce como *Cascada atmosférica extensa*. Esto ocurre cuando la partícula primaria colisiona
con la parte superior de la atmósfera y genera una cascada de partículas secundarias como protones, electrones y muons.
Utilizando la señal recogida, los científicos pueden tratar de responder a varias cuestiones: que tipo de partícula llego
a la atmósfera, de donde procede, y como se originó.

La respuesta a la primera pregunta es uno de los objetivos de este trabajo. Tradicionalmente, la clave para
conocer el tipo de primario es el número muónes generados en la cascada. Cuando una partícula
colisiona en la atmosférica y llega el suelo,  esta genera una señal en cada WCD, la cual es una
combinación de la señal electromagnética y la muónica de la cascada. Estimar la naturaleza de la partícula
incidente utilizando la señal muónica es un desafío con los dispositivos disponibles actualmente. El objetivo
en este caso, es el de aplicar técnicas de Machine Learning y Deep Learning para la detección del tipo de Partícula
primaria a partir de señales de WCDs.
