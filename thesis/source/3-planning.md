# Planificación del trabajo

La planificación de este trabajo se basa en un desarrollo en etapas.
La primera etapa corresponde a *investigación y descubrimiento*. En periodo
comprende la definición de objetivos, diferentes entrevista con *stakeholders*,
una revisión sobre el estado del arte tanto de reproducibilidad como del 
problema, etc. Este proceso tiene como objetivo elaborar una lista de requisitos con
las que basar el desarrollo del framework. La segunda etapa comprende el desarrollo propio
de *ml-experiment*. A rasgos generales,
el desarrollo del *framework* comprende la creación de la estructura del proyecto,
implementación de los diferentes módulos centrales (*Tracking*, *HPO*, *Callbacks*, etc.),
y el empaquetado de la versión *0.1*. La tercera etapa está orientada a la experimentación. Una vez implementado la versión
inicial del framework, se procede a implementar el código ML para las diferentes técnicas
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
