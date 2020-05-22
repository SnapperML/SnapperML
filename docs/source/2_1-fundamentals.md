# Fundamentos


## Reproducibilidad

Los estudios suelen ofrecer los resultados en forma de gráficas y tablas, pero en muchos casos
carecen de la información necesaria para poder constrastar los resultados. Está información suele
ser, el entorno de ejecución, los datos originales y la implementación de los propios métodos (modelos,
algoritmos, etc) entre otros. Para aumentar la accesibilidad de los estudios, los investigadores deben asegurarse
de ofrecer esta información además de las gráficas y tablas.

La verificación independiente tiene como objetivo la confirmación de credibilidad y la extensión del conocimento
en un area. La investigación relativa al Machine Learning o a otras areas donde se haga uso del mismo, no
está exenta de este requisito de la investigación científica. Por tanto, adoptando un flujo de trabajo reproducible, estamos
ofreciendo a la audiencia las herramientas necesarias que demuestran las decisiones tomadas y que permiten validar nuestros resultados.
Por otro lado, para que un estudio computacional pueda  ser reproducido correctamente por un investigador independiente
 es necesario el acceso completo a los datos, código, parametros de los experimentos, información sobre el entorno de ejecución, etc.
 
 
Otro motivo de interés para la búsqueda de la reproducibilidad es el de facilitar el uso de nuestros métodos por el resto
de la comunidad científica o incluso en aplicaciones comerciales. Ofreciendo acceso a los datos y al código, como se ha comentado antes,
permitimos que nuestros métodos se puedan aplicar a otros problemas, tanto en investigación como para fines comerciales, así como
facilita la extensión de nuestro trabajo.


En los ultimos años nos hemos encontrado con muchos casos de publicaciones cientificas que
muestran resultados dificiles o incluso imposibles de reproducir. Este fenómeno se conoce como
la crisis de la reproducibilidad, donde incluso estudios prominentes no se puden reproducir.
Este fenómeno ha estudiado de manera extensiva en otros campos, pero en el area del Machine Learning
está tomando últimamente mucho importancia. Esto es debido a que tradicionalmente, los experimentos
científicos se deben describir de tal forma que cualquiera pueda replicarlos, sin embargo, los experimentos
computacionales tienes varias complicaciones que los hacen particularmente dificiles de replicar: versiones
de software, dependencias concretas, variaciones del hardware, etc.

Con motivo de esta crisis de la reproducibilidad que afecta en gran medida a AI/ML, conferencias como
NeurIPS han optado por añadir la reproducibilidad como un factor en su proceso de revisión, e implementan
políticas para alentar el código compartido. Por otro lado, algunos autores (incluido nosotros) han propuesto
herramientas para facilitar la reproducibilidad, otros han propuesto una serie de reglas o heurísticas que
para evaluar este aspecto.


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
