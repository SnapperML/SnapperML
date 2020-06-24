# Introducción


## El problema de la reproducibilidad

Hoy en día, los proyectos de ciencia de datos se desarrollan de una forma desestructurada en la mayoría casos,
lo cual lo hacen muy difícil de reproducir @olorisadeReproducibilityMachineLearningBased2017 . Siendo conscientes de
las dificultades que conlleva ser rigurosos con el desarrollo de este tipo de trabajos para asegurar la reproducibilidad,
este trabajo presenta un framework que facilita  el rastreo de experimentos y la operacionalización del machine learning,
combinando tecnologías open source existentes y apoyadas fuertemente por la comunidad.
Estas tecnologías incluyen Docker @boettigerIntroductionDockerReproducible2015, MLFlow @zahariaAcceleratingMachineLearning2018,
y Ray @moritzRayDistributedFramework2018, entre otros.

El framework ofrece un flujo de trabajo concreto para el diseño y ejecución de experimentos en un entorno local o remoto.
Para facilitar la integración con código existente, se ofrece además un sistema de *tracking* automático para los frameworks de
Deep Learning más famosos: Tensorflow @abadiTensorFlowLargeScaleMachine2016 , Keras @gulliDeepLearningKeras2017, Fastai
@howardFastaiLayeredAPI2020, además de otros paquetes de Machine Learning como Xgboost @chenXGBoostScalableTree2016 y
Lightgdm @keLightGBMHighlyEfficient2017 . 
Por otro parte, se ofrece un soporte de primera clase para el entrenamiento de modelos y la hiperparametrización en entornos
distribuidos. Todas estas características se hacen accesibles al usuario por medio de un paquete de Python con el que instrumentalizar
el código existente, y un CLI con el que empaquetas y ejecutar trabajos.

La reproducibilidad es un reto en la investigación moderna y produce bastante debate @ArtificialIntelligenceFaces
@collbergMeasuringReproducibilityComputer @freireReproducibilityDataOrientedExperiments2016 @freireComputationalReproducibilityStateoftheart2012.
Entre los diferentes tipos de trabajos reproducibles, este trabajo se centra en trabajos computacionales, desarrollando
un flujo de trabajo específico bastado en los principios de Control de Versiones, Automatización, Tracking y Aislamiento
del entorno .

- El control de versiones permite  rastrear los diferentes ficheros del proyecto y sus cambios, así como facilitar la colaboración.
- Automatizar los procesos, desde ficheros de shell hasta pipelines de alto nivel, permite que otra persona puede reproducir los pasos del trabajo
fácilmente. Estos pasos incluyen: creación de ficheros, preprocesado de datos, ajuste de modelos, etc.
- *Tracking* o recolección de información: Durante la ejecución de estos pasos, se generan gráficos, artefactos, nuevos datos, etc.
Por este motivo, es necesario proporcionar una forma sistemática de recolectar toda esa información generada y mostrarla
de manera accessible desde un único lugar (*Knowledge Center*).

Finalmente, el aislamiento del sistema anfitrión mediante el uso de contenedores o máquinas virtuales, permite ampliar el ámbito de control
sobre los experimentos, proporcionando un "escenario común" para la ejecución de los mismo. De otra forma,
los factores externos al proyecto, como las versiones de las paquetes de análisis, los drivers de la GPU, o
la propia versión del sistema operativo donde se ejecuten pueden incrementar la incertidumbre del experimento @nagarajanDeterministicImplementationsReproducibility2019.
Otra ventaja de aislar las dependencias y la imagen del sistema operativo (entre otros factores), combinado con la automatización
 de los diferentes procesos, es que que facilita enormemente la ejecución de los experimentos y los hace dependiente de la
 plataforma, evitando tener que instalar las diferentes dependencias, modificar ficheros de configuración, etc. Por no decir
 que las dependencias del proyecto pueden ser incompatibles con las globales instaladas en el sistema.


## Clasificación de primarios

Uno de los misterios de Astrofísica a día de hoy es la forma en la que se generan los rayos cósmicos de ultra alta energía (UHECRs).
Para comprender mejor el comportamiento de estas partículas, el observatorio de Pierre Auger @PierreAugerCosmic2015 fue construido.
Supone un proyecto muy ambicioso y uno de los experimentos de mayor magnitud a día de hoy.
Un area de 3000 kilómetros cuadrados se ha diseñado y construido para alojar detectores de agua Cherenkov (WCDs) @agliettaResponsePierreAuger2005.
Estos detectores son unos tanques grandes de agua ultra-pura donde se detecta la radiación de Cherenkov, normalmente
utilizando fotomultiplicadores (PMTs) @lubsandorzhievHistoryPhotomultiplierTube2006 @d2011new.
Estos detectores son capaces de medir la señal generada por
las partículas mientras viajan a través del agua. Las interacciones de los UHECRs con las moléculas de aire de la
atmósfera producen lo que se conoce como *Cascada atmosférica extensa* @PierreAugerCosmic2015. Esto ocurre cuando la partícula primaria colisiona
con la parte superior de la atmósfera y genera una cascada de partículas secundarias como protones, electrones y muons.
Utilizando la señal recogida, los científicos pueden tratar de responder a varias cuestiones: que tipo de partícula llego
a la atmósfera, de donde procede, y como se originó.

La respuesta a la primera pregunta es uno de los objetivos de este trabajo. Tradicionalmente, la clave para
conocer el tipo de primario es el número muones generados en la cascada. Cuando una partícula
colisiona en la atmosférica y llega el suelo,  esta genera una señal en cada WCD, la cual es una
combinación de la señal electromagnética y la muónica de la cascada. Estimar la naturaleza de la partícula
incidente utilizando la señal muónica es un desafío con los dispositivos disponibles actualmente. El objetivo
en este caso, es el de aplicar técnicas de Machine Learning y Deep Learning para la detección del tipo de Partícula
primaria a partir de señales de WCDs.
