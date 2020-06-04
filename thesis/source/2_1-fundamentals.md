# Fundamentos


## Reproducibilidad


Según una encuesta realizada por Nature, una de las más prestigiosas revistas científicas a nivel mundial,
más del 70 por ciento de los 1,576 investigadores encuestados no han podido reproducir alguno de sus propios
experimentos. Además, los datos son claros, la mayoría piensa que existe una *crisis de reproducibilidad*.

![](https://www.nature.com/news/polopoly_fs/7.36716.1469695923!/image/reproducibility-graphic-online1.jpeg_gen/derivatives/landscape_630/reproducibility-graphic-online1.jpeg)


A día de hoy, los estudios suelen ofrecer los resultados en forma de gráficas y tablas, pero en muchos casos
carecen de la información necesaria para poder contrastar los resultados. Está información suele
ser, el entorno de ejecución, los datos originales y la implementación de los propios métodos (modelos,
algoritmos, etc) entre otros. Para aumentar la accesibilidad de los estudios, los investigadores deben asegurarse
de ofrecer esta información además de las gráficas y tablas.

La verificación independiente tiene como objetivo la confirmación de credibilidad y la extensión del conocimiento
en un area. La investigación relativa al Machine Learning o a otras areas donde se haga uso del mismo, no
está exenta de este requisito de la investigación científica. Por tanto, adoptando un flujo de trabajo reproducible, estamos
ofreciendo a la audiencia las herramientas necesarias que demuestran las decisiones tomadas y que permiten validar nuestros resultados.
Por otro lado, para que un estudio computacional pueda  ser reproducido correctamente por un investigador independiente
 es necesario el acceso completo a los datos, código, parametros de los experimentos, información sobre el entorno de ejecución, etc.
 
 
Otro motivo de interés para la búsqueda de la reproducibilidad es el de facilitar el uso de nuestros métodos por el resto
de la comunidad científica o incluso en aplicaciones comerciales. Ofreciendo acceso a los datos y al código, como se ha comentado antes,
permitimos que nuestros métodos se puedan aplicar a otros problemas, tanto en investigación como para fines comerciales, así como
facilita la extensión de nuestro trabajo.


En los últimos años nos hemos encontrado con muchos casos de publicaciones científicas que
muestran resultados difíciles o incluso imposibles de reproducir. Este fenómeno se conoce como
la crisis de la reproducibilidad, donde incluso estudios prominentes no se pueden reproducir.
Este fenómeno ha estudiado de manera extensiva en otros campos, pero en el area del Machine Learning
está tomando últimamente mucho importancia. Esto es debido a que tradicionalmente, los experimentos
científicos se deben describir de tal forma que cualquiera pueda replicarlos, sin embargo, los experimentos
computacionales tienes varias complicaciones que los hacen particularmente difíciles de replicar: versiones
de software, dependencias concretas, variaciones del hardware, etc.

Con motivo de esta crisis de la reproducibilidad que afecta en gran medida a AI/ML, conferencias como
NeurIPS han optado por añadir este factor en su proceso de revisión, e implementan
políticas para alentar el código compartido. Por otro lado, algunos autores (incluido nosotros) han propuesto
herramientas para facilitar la reproducibilidad, mientras que otros han propuesto una serie de reglas o 
heurísticas que para evaluar este aspecto.


## Tipos de reproducibilidad

Para poder atajar de una manera directa y eficiente el problema de la reproducibilidad es necesario separarla
en diferentes niveles. Esta separación nos permite desarrollar una serie de buenas prácticas y herramientas
específicas para cada nivel, así como ver de una manera clara que aspectos se pueden recoger en un framework común,
y cuales son inherentes del estudio científico en cuestión. Entre los niveles de reproducibilidad podemos destacar:

- Reproducibilidad computacional: Cuando se provee con información detallada del código, software, hardware y decisiones de implementación.


- Reproducibilidad empírica: Cuando se provee información sobre experimentación empírica no computacional u observaciones.


- Reproducibilidad estadística: Cuando se provee información sobre la elección de los test estadísticos, umbrales, p-valores, etc.


Una vez hecha separación del problema en tres capas, podemos ver claramente que la reproducibilidad computacional debe ser nuestro
objetivo a la hora de desarrollar el framework. Mientras que la reproducibilidad empírica se puede conseguir
en mayor medida, haciendo los datos accesibles, la reproducibilidad estadística se consigue mediante el desarrollo de un diseño inicial
del estudio. En este diseño se especifica la hipótesis base, las asunciones del problema, los test estadísticos a realizar, y los p-valores correspondientes.
El establecer las bases estadísticas sobre las que se va a desarrollar el estudio de antemano, nos puede ayudar además a evitar
problemas como el p-hacking.


The terms “reproducible research” and “reproducibility” are used in many different ways to
encompass diverse aspects of the desire to make research based on computation more
credible and extensible. Lively discussion over the course of the workshop has led to some
suggestions for terminology, listed below. We encourage authors who use such terms in
their work to clarify what they mean in order to avoid confusion.
There are several possible levels of reproducibility, and it seems valuable to distinguish
between the following:

- Reviewable Research. The descriptions of the research methods can be independently
assessed and the results judged credible. (This includes both traditional peer
review and community review, and does not necessarily imply reproducibility.)

-  Replicable Research. Tools are made available that would allow one to duplicate
the results of the research, for example by running the authors’ code to produce
the plots shown in the publication. (Here tools might be limited in scope, e.g., only
essential data or executables, and might only be made available to referees or only
upon request.)

- Confirmable Research. The main conclusions of the research can be attained
independently without the use of software provided by the author. (But using the complete
description of algorithms and methodology provided in the publication and any supplementary materials.)

- Auditable Research. Sufficient records (including data and software) have been
archived so that the research can be defended later if necessary or differences
between independent confirmations resolved. The archive might be private, as with
traditional laboratory notebooks.

- Open or Reproducible Research. Auditable research made openly available. This
comprised well-documented and fully open code and data that are publicly available
that would allow one to (a) fully audit the computational procedure, (b) replicate and
also independently reproduce the results of the research, and (c) extend the results
or apply the method to new problems.


### Aspectos críticos


- Conjunto de datos: La información sobre la localización y el proceso de extracción de los datos.

- Preprocesado de datos: Los diferentes pasos del proceso de transformación de los datos.

- 


## Aspectos críticos


• Dataset: Information about the location and the retrieval process of the dataset is needed to
ensure access to the dataset as used in the study.

• Data preprocessing: The process of ridding the input data of noise and encoding it into a
format acceptable to the learning algorithm. Explicit preprocessing information is the first
step towards a successful reproduction exercise. An independent researcher should be able
to follow and repeat how the data was preprocessed in the study. Also, it will be useful to
find preprocessing output information to compare to e.g. final feature vector dimension.

• Dataset Partitions: Details of how the dataset was divided for use as training and test data.

• Model training: The process of fitting the model to the data. Making available, as much
information as possible regarding every decision made during this process is particularly
crucial to reproduction. Necessary information include but not limited to:
1. Study parameters
2. Proposed technique details – codes, algorithms etc. (if applicable)

• Model assessment: Measuring the performance of the model trained in 2. Similar information as in 2 applies here as well.

• Randomization control: Most operations of machine learning algorithms involves randomization. Therefore, it is essential to set seed values to control the randomization process in
order to be able to repeat the same process again.

• Software environment: Due to the fact that software packages/modules are in continual
development with possible alterations to internal implementation algorithms, it is important
that the details of the software environment used (modules, packages and version numbers)
be made available.

• Hardware environment (for large data volume): Some data intensive studies are only
reproducible on the same machine capacity as was used to produce the original result. So,
the hardware information are sometimes essential.


## Proceso de ciencia de datos. ETL



## DevOps aplicado a Machine Learning. MLOps 



## Autoencoders
