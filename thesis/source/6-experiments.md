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
contienen más energía que cualquier otra partícula observada en la naturaleza. Los rayos cósmicos de mayor energía
contiene cientos millones de veces más energía que la partícula con mayor energía hoyada en la naturaleza.

Este fenómeno de la Física fue descubierto en 1912 por Hess y Kohlhorster [@stanevOverview2010], y algunas de sus propiedades
siguen siendo un misterio después de más de un siglo. Un ejemplo es el origen de los rayos, la mayoría de los científicos sospechan
que el origen de los rayos cósmicos está relacionado con las *supernovas*, aunque no descartan otro tipo de fuentes [@burrowsBaadeZwickySupernovae2015].
Además, no es del todo claro como las supernovas pueden generar estos rayos cósmicos tan rápido. 

Para aprender más sobre la naturaleza de este fenómeno, los científicos miden la energía y la dirección
de los rayos conforme llegan a la tierra. Los rayos cósmicos de baja energía se miden utilizando globos aerostáticos y satélites
situados por encima de la atmósfera terrestre, mientras que para los rayos cósmicos de alta energía,
es más eficiente medirlos indirectamente observado la cascada de partículas que produce.

![Cascada atmosférica extensa. (Observatorio Pierre Auger)](source/figures/comic_air_shower.jpg){#fig:shower}

Una *cascada atmosférica extensa* [@stanevHighEnergyCosmic2010] se produce cuando un rayo cósmico de alta energía
(y de alta velocidad) penetra en la atmósfera. Cuando una partícula colisiona violentamente con las moléculas de aire,
se fragmenta generando hadrones. Los fragmentos desprendidos a su vez colisionan con otras partículas del aire,
produciendo así una cascada donde la energía de la partícula original
se dispersa entre millones de partículas que caen hacia la tierra (ver figura \ref{fig:shower}).
Al estudiar las *cascadas atmosféricas*, los científicos pueden medir algunas propiedades de las partículas
originales que llegaron a la atmósfera, también llamadas *primarios*.

![Mapa del observatorio de Pierre Auger. Cada punto negro representa un detector WCD](source/figures/observatory_map.pbm){#fig:observatory}

El Observatorio de Pierre Auger [@PierreAugerCosmic2015] se propuso para descubrir y entender la fuentes de los rayos
cósmicos de energía más altas. El observatorio, situado en la ciudad de Malargüe, en la provincia de Mendoza, Argentina,
es una colaboración única entre 18 países, cuya construcción empezó en 2002 y finalizó en 2008.
El observatorio es un detector híbrido, utiliza un detector de gran superficie (SD) y un detector
de fluorescencia (FD). El SD se compone de 1660 WCDs situados estratégicamente formando una malla triangular.
En esta malla, los detectores están separados con una distancia de 1500 metros. Además, existe otra malla más pequeña cuyos
detectores están separados 750 metros. En la figura \ref{fig:observatory} se muestra la distribución de los
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
El flujo de generación de los datos se muestra en la figura \ref{fig:simulation_flow}. CORSIKA [@heckCORSIKAMonteCarlo1998]
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


Como se ha descrito anteriormente, los datos se basan en la simulación de
la señal recogida en los WCDs. Esta señal recoge tanto la parte muónica $\mu$,
como la parte electromagnética $em$. A simple vista, la señal muónica se puede
utilizar para separar entre las diferentes tipos de primario. Pero al existir
varios PMTs en un mismo detector, pueden existir relaciones entre las señales de
cada fotomultiplicador. Para poder atajar este problema con ML/DL es necesario
encontrar un representación del problema tal que nos permita utilizar las señales
de muónicas capturadas por los PMTs para clasificar entre primarios.
Una representación utilizada en trabajos previos, consiste en integrar la señal muónica,
obteniendo un único valor real para cada PMT. Disponiendo así de un vector con N valores reales,
tantos como PMTs haya en el WCD.

La representación que se propone en este trabajo consiste en utilizar la señal de los PMTs de manera independiente,
es decir, modelar un clasificador a nivel de PMT en lugar de WCDs. De esta forma podemos profundizar en la información
recogida en la señal, en lugar de condensar toda esa información en un solo número real (la integral).
Elegir la granularidad con la que se analizan los datos es uno de los retos más importantes de este problema.
Como se ha mencionado al principio del capítulo, una *cascada atmosférica extensa* puede producir una señal en
multiples PMTs dentro de un mismo detector WCD, pero además, puede afectar a varios detectores vecinos.
Teniendo esto en cuenta, el problema se puede modelar a nivel de PMT, a nivel de WCD, o a nivel de estación.
En nuestro caso lo vamos a analizar a nivel de PMT.

Como trabajar con la señal en crudo puede ser muy costosa en términos de memoria, y recursos
de CPU, los valores de cada vector se extraen a partir de la salida de *Offline de Auger*.
La señal recogida está discretizada por lo que se puede utilizar como un vector de tamaño
fijo. Sin embargo, la traza puede ser caracterizada completamente mediante un conjunto más
pequeño de variables que se describen a continuación:

**Variables extraídas directamente de las simulaciones**

- Energía Monte Carlo ·E·: La energía total (en EeV, Exaelectron Voltios) del rayo cósmico primario (transformada con *log10*)
- Angulo de Zenit Monte Carlo $\Theta$: Angulo en grados entre el zenit y la trayectoria del rayo cósmico primario.
- Distancia al núcleo $r$: Distancia entre cada estación y la posición estimada del núcleo de la cascada, medida en metros.
- Señal total $S_{total}$: Número real en muones equivalentes verticales (VEMs) de la señal capturada por los WCD.
- Longitud de la traza: Tamaño del vector de la señal recogida. La señal está discretizada en *bins* de 25 nanosegundos.

**Variables generadas mediante ingeniería de atributos:**

- Ángulo Azimuth $\zeta$: medido en radianes.
- Tiempo de subida $t_{1 / 2}$: medido en nanosegundos.
- Tiempo de caída: Tiempo en el que la señal empieza a descender.
- Area sobre el punto máximo de la señal: Suma de todas las señales en cada traza dividida por el máximo valor en cada traza.

## Procedimiento

Para el desarrollo de los diferentes experimentos se utilizado el framework descrito en el capítulo anterior.
Para cada algoritmo de ML o arquitectura de DL se ha implementado un script de entrenamiento y un fichero
de configuración asociado. Como la cantidad de datos o la dimensionalidad no son relativamente grandes, se ha
podido aplicar optimización de hiperparámetros. Para ello, el fichero de configuración asociado a cada algoritmo
define un Grupo de experimentos (ver *Diseño y desarrollo del framework*) con un espacio de hiperparámetros
diseñado especialmente para cada tipo de modelo. Los grupos de experimentos se han ejecutado de manera local,
aprovechando todos los núcleos de la CPU. Por otra parte, el proyecto de experimentación se llevado a cabo
teniendo en cuenta los aspectos críticos de la reproducibilidad descritos en *Fundamentos*, y aplicando las buenas prácticas de MLOps.

![Todos los experimentos ejecutados con parámetros, métricas, artefactos, y otros metadatos, se almacenan en un servidor de MLFlow en local](source/figures/mlflow_experiments.png){#fig:mlflow_experiments}

Por una parte, el procedimiento de partición y procesado de los datos se realiza desde una interfaz compartida por todos los scripts
de entrenamiento utilizando un *DataLoader* (ver Manual). Además, las semillas para la partición, procesado y entrenamiento de modelos
se establece y queda almacenada como metadatos en cada experimento. Esto nos asegura que todos los modelos son entrenados y validados
con los mismos datos, así como facilita la *replicabilidad* del experimento. Por otra parte, los parámetros, métricas y artefactos de
cada experimento están almacenados en el servidor de *MLFlow* (ver figura \ref{fig:mlflow_experiments}), permitiendo visualizar
y comparar entre las modelos y entre las diferentes configuraciones de hiperparámetros para cada algoritmo. Finalmente,
la información relativa al hardware y el software donde se han ejecutado los experimentos también queda almacenada,
en concreto, la información relativa al hardware es la siguiente:

|       Tag      |                                    Value                                   |
|:--------------:|:--------------------------------------------------------------------------:|
|    CPU Info    |                  Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz                  |
| Python Version | 3.7.7 (default, Mar 10 2020) [Clang 11.0.0 (clang-1100.0.33.17)] |
|    GPU Info    |                                      -                                     |


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
