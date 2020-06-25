# Experimentos

En este último capitulo de la tesis se recogen los experimentos llevados a cabo para la resolución
del problema (Objetivo 2). Primeramente, se describe detalladamente el problema: origen, tipo y estructura
de los datos, tipo de problema, asunciones y/o restricciones, etc. Posteriormente, se detallan los diferentes
algoritmos y arquitecturas de ML/DL empleados - se especifican los parámetros, biblioteca empleada,
detalles de implementación, y otra información relevante. Finalmente, se muestran los resultados obtenidos
para cada tipo de modelo, y algunos trabajos a posteriori que pueden ser interesantes.

## Definición del problema

### Historia

Los rayos cósmicos son fragmentos de átomos (electrones, protones, y núcleos atómicos) que bombardean la tierra desde
todas direcciones. La mayoría de fragmentos corresponden a núcleos atómicos o electrones. Las partículas de rayos cósmicos
viajan a prácticamente la velocidad de la luz, lo que significa que tienen una gran energía. Algunas de ellas incluso
contain más energía que cualquier otra partícula observada en la naturaleza. El rayos cósmicos de mayor energía contiene
cientos millones de veces más energía que la partícula con mayor energía hoyada en la naturaleza.

Este fenómeno de la Física fue descubierto en 1912 por Hess y Kohlhorster, y algunas de sus propiedades siguen siendo
un misterio después de más de un siglo. Un ejemplo de es el origen de los rayos, la mayoría de los científicos sospechan
que el origen de los rayos cósmicos está relacionado con las *supernovas*, aunque no descartan otro tipo de fuentes.
Además, no es del todo claro como las supernovas pueden generar estos rayos cósmicos tan rápido. 

Para aprender más sobre la naturaleza de estos rayos cósmicos de alta energía, los científicos miden la energía y la dirección
de los rayos conforme llegan a la tierra. Los rayos cósmicos de baja energía se miden utilizando globos aerostáticos y satélites
situados por encima de la atmósfera terrestre. Sin embargo, para los rayos cósmicos de alta energía, es más eficiente medirlos
indirectamente observado la lluvia de partículas que produce.

Una *cascada atmosférica extensa* se produce cuando un rayo cósmico de alta energía (y de alta velocidad) penetra en la atmósfera.
Cuando una partícula colisiona violentamente con las moléculas del aire se fragmenta, generando hadrones. Los fragmentos
desprendidos a su vez colisionan con otras partículas del aire, produciendo así una cascada donde la energía de la partícula original
se dispersa entre millones de partículas que caen hacia la tierra. Al estudiar las *cascadas atmosféricas*, los científicos pueden
medir algunas propiedades de las partículas originales que llegaron a la atmósfera, también llamadas *primarios*.

El Observatorio de Pierre Auger se propuso para descubrir y entender la fuentes de los rayos
cósmicos de energía más altas. El observatorio, situado en la ciudad de Malargüe, en la provincia de Mendoza, Argentina,
es una colaboración única entre 18 países, cuya construcción empezó en 2002 y finalizó en 2008.
El observatorio es un detector híbrido, utiliza un detector de gran superficie (SD) y un detector
de fluorescencia (FD). El SD se compone de 1660 WCDs situados estratégicamente formando una malla triangular.
En esta malla, los detectores están separados con una distancia de 1500 metros. Además, existe otra malla más pequeña cuyos
detectores están separados 750 metros. En la figura \ref{#fig:observatory} se muestra la distribución de los
detectores.

Los WCDs del Observatorio de Pierre Auger consisten en tanques de agua de 3.6 metros
de diámetro, que contienen 12,000 litros de agua ultrapura cada uno. En estos tanques están
colocados tres PMTs distribuidos simétricamente, los cuales se encargan de medir 
la radiación Cherenkov. La señal de estos PMTs corresponden a la combinación de la señal muónica y
electromagnética de la *cascada atmosférica extensa*. Como se puede intuir, una sola partícula primaria
puede producir una señal en multiples PMTs, incluso en múltiples WCDs. Lo cual complica el análisis de
la naturaleza de la partícula al tener que estudiar las relaciones entre las señales de los diferentes
detectores.


### Definición formal del problema

Los experimentos recogidos en este trabajo están basados en datos de simulaciones, en lugar de los datos
reales. En concreto, se componen diferentes herramientas para la simulación de *cascadas atmosférica extensas*.
El flujo de generación de los datos se muestra en la figura \ref{#fig:simulation_flow}. CORSIKA [@heckCORSIKAMonteCarlo1998]
se utilizada para la simulación detallada de como se desarrolla la *cascada atmosférica extensa* en la atmósfera.
Las interacciones hadrónicas se modelan utilizando QGSJET-II [@ostapchenkoQGSJETIIReliableDescription2006]
o EPOS-LHC [@pierogEPOSLHCTest2015]. La señales de los WCDs producidas por las partículas se generan utilizando
el software *offline* de Auger [@argiroOfflineSoftwareFramework2007]. Finalmente, los datos de las simulaciones
se almacenan en formato ROOT [@brunROOTObjectOriented1997] para su procesamiento.

Como es de intuir, este tipo de simulaciones requieren una cantidad de recursos de espacio y computacionales enorme,
por este motivo, se utilizada una fracción reducida de los datos. Para esta fracción de los datos, se han recogido
alrededor de 20000 muestras para cada tipo de primario. En este caso, los tipos de primarios disponibles son:
helio, hierro, proton, oxígeno. Para cada primario se han separado los datos en un conjunto de entrenamiento y otro de
test. Siendo la distribución de los datos según el número de ejemplos la siguiente:


| **Primary** | **Training set** | **Test set** | **Total** |
|:-------:|:------------:|:--------:|:-----:|
| Helium  | 16007        | 4001     | 20008 |
| Iron    | 16019        | 4004     | 20023 |
| Proton  | 16026        | 4006     | 20032 |
| Oxygen  | 16021        | 4005     | 20026 |


The algorithms will be trained and tested using these data. For the training, however, another testing stage
will be carried out using the data available from simulations using the EPOS LHC model.
In this way, it is possible to test if the models are able to generalise properly the natural
phenomenon modelled independently of the simulator used to generate the
data.


As described above, there are some inputs that consist of the simula-
tion of a particle being recorded by the WCD. That signal encompasses the
muonic component μ as well as the electromagnetic component em. The
question is how to obtain the muonic component to determine the composi-
tion of the primary particle. As stated, it seems straightforward as a blind
source separation problem which can be tackled using Independent Compo-
nent Analysis. However, the results obtained by our group using this method
were far from being successful. Therefore, the proposed solution was to map
this problem to a ML classical approach. In this case, the muonic signal can
be integrated, providing a continuous value. Thus, it is possible to end up
with a set of inputs ⃗xi ∈ Rd,i = 1...m (particles of the EAS interacting in
a surface detector) and a continuous output value Y = [yi],i = 1...m which
corresponds to the integral of the muonic signal generated.
With this formulation, the mapping from Physics to ML results in a
classical regression problem where it is desired to obtain a function f such
thatf(x⃗)≈y,∀i.

As working with the raw signal might be too expensive in terms of memory
and CPU requirements, the variables used to define ⃗xi where taken from the
output of the Offlinesoftware package [10]. Nevertheless, according to the
experts, the trace can be fully characterized by adding some features that
can help the model to learn the function f. Thus the subset of variables
remained as follows:

Input variables:
- Energía Monte Carlo ·E·: La energía total (en EeV, Exaelectron Voltios) del rayo cósmico primario (transformada con *log10*)
- Angulo de Zenit Monte Carlo $\Theta$: Angulo en grados entre el zenit y la trayectoria del rayo cósmico primario.
- Distancia al núcleo $r$: Distancia entre cada estación y la posición estimada del núcleo de la cascada, medida en metros.
- Señal total $S_{total}$: Número real en muones equivalentes verticales (VEMs) de la señal capturada por los WCD.
- Longitud de la traza: number of bins with signal recorded (each bin considers 25 nanoseconds).

Engineered variables:
- Azimuth Angle ζ: measured in radians .
- Signal risetime t1/2: measured in nanoseconds.
- Signal falltime: real value showing when the signal starts falling.
- Area over peak of the signal: sum of the signals in each trace divided by the maximum value of each trace.

## Procedimiento

## Modelos considerados

### Deep Learning

#### Autoencoders

### Machine Learning tradicional

#### SVM

#### Xgboost

#### Autoencoder Simple

#### Autoencoder Apilado

#### Autoencoder Variacional


## Resultados
