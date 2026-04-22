# Objetivos


El objetivo de este proyecto es el de desarrollar un marco de trabajo para *Machine Learning* enfocado
en la reproducibilidad y buenas prácticas. Por otro lado, como objetivo
secundario tenemos la aplicación de dicho framework para resolver un problema real.


De un modo más específico, los principales objetivos son:

- Diseño e implementación de un framework de reproducibilidad: El desarrollo de una herramienta 
que permita instrumentalizar proyectos de *Machine Learning* con mínimo esfuerzo, orientada a mantener unas buenas
prácticas de desarrollo y seguir una filosofía *MLOps* (ver *Fundamentos*). Dentro de este objetivo, de manera secundaria, incluimos
una contribución de código a uno de los proyectos de código libre que componen el módulo central de nuestra
herramienta, *Mlflow*.

- Especificación de buenas prácticas: La creación de una lista de pautas y requisitos necesarios para
hacer reproducible un proyecto. Desde la recolección de datos hasta la gestión de experimentos.

- Aplicación de la herramienta a la resolución de un problema real: Aplicación de diferentes técnicas de *Machine
Learning* tradicional y Deep learning para la resolución de un problema importante en física, la clasificación de partículas.
El problema consiste en la detección del tipo de partícula primaria de una *cascada de partículas extensa*
a partir de una señal registrada por un detector de partículas que almacena una mezcla de señal electromagnética y muónica.
El objetivo es encontrar un buen modelo  para el dominio en cuestión, y hacer un uso extensivo de la herramienta
y para valorar los beneficios para este caso concreto.


## Alcance de los objetivos

Para el primer objetivo, el alcance incluye el desarrollo integral de una herramienta en Python
que permita cumplir con la mayoría de requisitos que consideramos necesarios para que un proyecto
sea reproducible fácilmente por la comunidad científica. Esta herramienta debe ser flexible y permitir
integrarse con frameworks de *Machine Learning* tradicional o *Deep learning* existentes, así como con proyectos orientados
al análisis de datos exclusivamente en lugar de al modelado.

En relación con el primer objetivo, se debe desarrollar una especificación de buenas prácticas basadas en
problemas existentes, con el objetivo de reducir aquella deuda técnica que concierne a este tipo de proyectos,
tanto durante el desarrollo o experimentación, como en el momento de compartir el trabajo con otras personas.
Estas buenas prácticas son bastante comunes en el desarrollo de software, pero no tanto en ciencia de datos,
debido, entre otros motivos, a la heterogeneidad de perfiles que componen este campo. Dentro de esta relación
entre el desarrollo de software y el desarrollo de proyectos de *Machine Learning* o ciencia de datos en general,
se van tener en cuenta también aspectos relacionados con el despliegue e integración de software, lo
que se conoce como DevOps, cuya aplicación al machine learning es más bien conocida como MLOps.

El tercer y último objetivo comprende el desarrollo de un proyecto de *Machine Learning* real, enfocado al modelado
y a la experimentación. El alcance comprende la parte de análisis de modelado del *proceso de ciencia de datos* (ver Fundamentos) -
entendimiento del problema, procesado de datos, modelado, etc. Como objetivo secundario, se profundiza en el desarrollo
de los autoencoders, atajando el problema de clasificación desde un enfoque de aprendizaje no supervisado, para
finalmente compararlo con el resto de métodos tradicionales.
