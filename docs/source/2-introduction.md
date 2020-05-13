# Introducción


Hoy en día, los proyectos de ciencia de datos se desarrollan de una forma destructurada en muchos casos,
lo cual lo hacen muy difícil de reproducir. Siendo conscientes de las dificultades que conlleva ser rigurosos con el
desarrollo de este tipo de trabajos para asegurar la reproducibilidad, este trabajo presenta un framework que facilita 
el rastreo de experimentos y la operacionalziación del machine learning, combinando tecnologías open source existentes
y apoyadas fuertemente por la comunidad. Estas tecnologías incluyen Docker, Mlflow, Ray, entre otros.
El framework ofrece también un flujo de trabajo opionionado para el diseño y ejecución de experimentos en un entorno local o remoto.
Para facilitar la integración con código existente, se ofrece además un sistema de rastreo automático para los frameworks de
Deep Learning más famosos: Tensorflow, Keras,Fastai, además de otros paquetes de Machine Learning como Xgboost y Lightgdm.
Por otro parte, se ofrece un soporte de primera clase para el entrenamiento de modelos y la hyperparametrización en entornos
distribuidos. Todas estas caracteristicas se hacen accesibles al usuario por medio de un paquete de Python con el que instrumentalizar
el código existente, y un CLI con el que empaquetas y ejecutar trabajos.




- Rayos cósmicos
- Remarcar problemas en la reproductibilidad

## Herramientas para el análisis de rayos cósmicos

- ROOT Framework
- Corkiska
- CERN
