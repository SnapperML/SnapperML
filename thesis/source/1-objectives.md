# Objetivos


El objetivo de este proyecto es el de desarrollar un marco de trabajo para machine learning enfocado
en la reproducibilidad y buenas prácticas que explicaremos más adelante. Por otro lado, como objetivo
secundario tenemos la aplicación de dicho framework para resolver un problema real.


A modo de resumen, los principales objetivos son:

- Diseño e implementación de un framework de reproducibilidad: El desarrollo de una herramienta 
que permita instrumentalizar proyectos de Machine Learning con mínimo esfuerzo, orientada a mantener unas buenas
prácticas de desarrollo y seguir una filosofía MLOps. Dentro de este objetivo, de manera secundaria, incluimos
una contribución de código a uno de los proyectos de código libre que componen el módulo central de nuestra
herramienta, Mlflow.

- Especificación de buenas prácticas: La creación de una lista de pautas y requisitos necesarios para
hacer reproducible un proyecto. Desde la recolección de datos hasta la gestión de experimentos.

- Aplicación de la herramienta a la resolución de un problema real: Este objetivo está orientado a la
experimentación, trata de la aplicación de diferentes técnicas de Machine Learning tradicional y Deep learning
para la resolución de un problema común en física, la detección de primarios. En dicha aplicación, hacemos un
uso extensivo de la herramienta y valoramos los beneficios y el coste en recursos de tiempo y capitales de su uso
para este caso concreto.


## Alcance de los objetivos


Para el primer objetivo, el alcance incluye el desarrollo integral de una herramienta en Python
que permita cumplir con la mayoría de requisitos que consideramos necesarios para que un proyecto
sea reproducible fácilmente por la comunidad científica. Esta herramienta debe ser flexible y permitir
integrarse con frameworks de Machine Learning o Deep learning existentes, así como con proyectos orientados
al análisis de datos exclusivamente en lugar de al modelado.


En relación con el primer objetivo, se debe desarrollar una especificación de buenas prácticas basadas en
problemas existentes, con el objetivo de reducir aquella deuda técnica que concierne a este tipo de proyectos,
tanto durante el desarrollo o experimentación, como en el momento de compartir el trabajo con otras personas.
Estas buenas prácticas son bastante comunes en el desarrollo de software, pero no tanto en ciencia de datos,
debido, entre otros motivos, a la heterogeneidad de perfiles que componen este campo. Dentro de esta relación
entre el desarrollo de software y el desarrollo de proyectos de machine learning o ciencia de datos en general,
se van tener en cuenta también aspectos relacionados con el despliegue e integración de software, lo
que se conoce como DevOps, cuya aplicación al machine learning es más bien conocida como MLOps.


El tercer y último objetivo comprende el desarrollo de un proyecto de machine learning real, enfocado al modelado
y a la experimentación. El alcance comprende el entendimiento del problema, procesado de datos, y modelado.
