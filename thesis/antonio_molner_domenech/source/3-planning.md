# Planificación del trabajo

La planificación de este trabajo se basa en un desarrollo en etapas.
La primera etapa corresponde a *investigación y descubrimiento de requisitos*.
Este periodo comprende la definición de objetivos, diferentes entrevistas con *stakeholders*
^[Los stakeholders de este proyecto han sido el tutor y los científicos del Laboratório de Instrumentação e Física Experimental de Partíıculas (LIP).],
una revisión sobre el estado del arte, tanto de reproducibilidad como del 
problema, etc. Este proceso tiene como objetivo elaborar una lista de requisitos con
las que basar el desarrollo del framework. La segunda etapa comprende el desarrollo propio
de *ml-experiment*. A rasgos generales, este desarrollo comprende la creación de la estructura del proyecto,
implementación de los diferentes módulos centrales (*Tracking*, *HPO*, *Callbacks*, etc.),
y el empaquetado de la versión *0.1*. La tercera etapa está orientada a la experimentación,
una vez desarrollada la versión inicial del framework, se procede a implementar el código ML para las diferentes técnicas
tratadas en este trabajo. Posteriormente, se ejecutan diferentes configuraciones de cada técnica
y se recogen los resultados. Por último, se ha procedido a la documentación del código, al desarrollo
de la memoria y del manual de usuario.

![Tablero de Trello para *ml-experiment*. En este tablero se recogen las tareas, referencias, futuro desarrollo, y
otra información relevante del proyecto.](source/figures/trello.png){#fig:kanban}

Por otro lado, durante el desarrollo del trabajo se ha utilizado una metodología *Kanban* [@anderson2010kanban] utilizando la plataforma
*Trello* [@Trello]. En la figura \ref{fig:kanban} se puede ver el tablero del proyecto con las diferentes tareas,
referencias, etc. Estás tareas se encuentran especificadas con una granularidad mayor que en el diagrama de Gantt
mostrado posteriormente. Además, en este tablero también están documentadas las funcionalidades previstas
para las siguientes versiones del proyecto.

\includepdf[pages=-]{source/figures/ml-experiment_gantt.pdf}


## Lista de requisitos

La lista de requisitos funcionales y no funcionales del *framework* se ha elaborado a partir de las diferentes reuniones con *stakeholders*,
y mi experiencia personal en la industria (trabajo en una empresa con departamento de Ciencia de Datos).  La lista es la siguiente:

- RF1. Registrar y controlar los aspectos críticos de la reproducibilidad de un experimento (parámetros, artefactos, semillas, etc).

- RF2. Permitir subscribirse a diferentes eventos y enviar notificaciones para el fin e inicio de trabajos.

- RF3. Visualizar con una interfaz Web la información recogida durante la ejecución de experimentos.

- RF4. Permitir la configuración de trabajos mediante ficheros de texto con un especificación concreta.

- RF5. Ofrecer soporte para definir trabajos de HPO para diferentes algoritmos de optimización.

- RF6. La información de los experimentos debe recogerse de manera automática o con mínima intervención del usuario.

- RF7. El usuario debe interaccionar con el *framework* para definir y ejecutar trabajos mediante una [!cli] y una biblioteca de Python.


- RNF1 Soporte para diferentes herramientas (*Pluggability*): Los científicos de datos utilizan una gran variedad de frameworks y herramientas.
El sistema debe ofrecer soporte para la mayoría de *frameworks*, o no estar restringido a ninguno en concreto.

- RNF2 Reusabilidad: Una vez definido un fichero de configuración para un experimento, el sistema debe permitir reutilizarlo y ejecutarlo de la manera más determinística
posible.

- RNF3 Flexibilidad: El sistema no debe soportar solamente un caso de uso. Diferentes roles pueden hacer uso del mismo. Ademas, debe permitir la integración
con servicios y herramientas existentes.

- RNF4 Escalabilidad: El sistema debe proveer escalabilidad, es decir, poder ejecutar experimentos en paralelo aprovechando todos los recursos de computación disponibles.

- RNF5. Los trabajos deben poder ejecutarse en local y en la nube. Preferiblemente esta funcionalidad no debe estar limitada
a un proveedor de servicios *cloud* en concreto.
