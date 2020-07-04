# Fundamentos y estado del arte

A lo largo de este capítulo, describiremos principalmente los fundamentos del trabajo y el estado
del arte. Para los fundamentos, destacaremos la nomenclatura utilizada, añadiendo un pequeño
glosario de términos. Posteriormente, se define el concepto de *reproducibilidad* en los proyectos de investigación
basados de *Machine Learning* (ML), y los aspectos críticos de dictaminan cuando un proyecto es reproducible o no.
Por otro lado, se define el proceso de ciencia de datos, con una descripción de cada uno de los pasos, y la
deuda técnica asociada a dicho proceso. 

En las sección de *MLOps* se describe un concepto novedoso sobre un conjunto de buenas prácticas para el desarrollo
de proyectos de ciencia de datos que la industria está implementando progresivamente. En las posteriores secciones, 
se describen varios de los algoritmos de *Machine Learning* y *Deep Learning* utilizados en la experimentación, con especial
atención a los *autoencoders*. Finalmente, se hace un repaso del estado del arte para las herramientas para reproducibilidad,
*MLOps* y para los algoritmos implementados.

## Nomenclatura

El área de la ciencia de datos, *Machine Learning* y *MLOps*, se hace uso de una terminología concreta
[@wardenBigDataGlossary2011; @hutsonAIGlossaryArtificial2017; @provost1998glossary],
basada principalmente en la terminología de *Aprendizaje estadístico*, *Desarrollo Software*, y 
*DevOps* en el caso de *MLOps*. En esta sección se desarrollan algunos de los términos más utilizados:

- **Canalización o Pipeline**: Consiste en una definición e implementación exhaustiva de las diferentes
etapas de un proceso. Un pipeline se puede definir como un script, conjunto de scripts, ficheros de
configuración, etc. Además, permite la ejecución del proceso de manera automatizada  . 

- **Conjuntos de datos** – Colección de datos estructurada que se utiliza para entrenar modelos de [!ml],
para análisis, o para inferencia. Aunque los conjuntos de datos pueden contener información de
diferentes fuentes, el conjunto en sí tiene una sola tesis central (propósito).

- **Experimento** – Un proceso o actividad que permite testear una hipótesis y validarla iterativamente.
Los resultados de una cierta iteración deben ser almacenados para poder ser evaluados, comparados,
y monitorizados para propósitos de auditoría.

- **Artefacto**: Pieza de información generada en un experimento. Incluye modelos entrenados,
datos generados, imágenes, documentación autogenerada, etc.

- **Modelo** – Es un caso concreto de artefacto que permite predecir valores en un sistema [!ml] o bien,
permite ser usado como pieza de otro modelo (mediante *ensamblado* o *transferencia de conocimiento*).

- **Repositorio**: Fuente de código común para la organización. Se entiende por repositorio
aquel directorio gestionado por un control de versiones (como Git). Este repositorio puede
contener implementaciones de pipelines, modelos, datos, ficheros de configuración, decisiones
de dependencias, entre otras cosas.

- **Registro de modelos** – Almacén centralizado donde se almacenan los diferentes modelos
generados en el ciclo de vida de un proyecto de ciencia de datos.

- **Espacio de trabajo**: Los científicos de datos desarrollan sus actividades de manera colaborativa o
individual. Un entorno de trabajo comprime aquellas herramientas e información necesarias para el desempeño
de un rol específico. Un entorno típico de ciencia de datos consiste en un IDE donde escribir código, y
un conjunto de herramientas locales o en línea que permiten acceder a los datos, modelos, etc. Un ejemplo
de espacio de trabajo típico puede ser *Jupyter* [@ProjectJupyter] para desarrollo de código,
*Amazon Sagemaker* [@AmazonSageMaker] para la gestión de modelos, y *DataGrip* [@DataGripIDEMultiplataforma]
para el acceso a base de datos.

- **Entorno objetivo**: El entorno de despliegue de los sistemas de [!ml], es decir, el entorno
donde el modelo va a generar información (en forma de predicciones) para el consumo por el usuario.
Alguno de los entornos objetivos más comunes son:
    - Servicio web, como parte de un backend propio, o como microservicio. Se implementa a partir de una API REST, GRPC o cualquier
    otro protocolo web.
    - Dispositivos finales. El modelo se integra dentro del dispositivo y se hacen las predicciones localmente.
    Útil para dispositivos con conectividad limitada, IoT, etc.
    - Parte de un sistema de predicción por lotes.


## Reproducibilidad

Según una encuesta realizada por Nature, una de las revistas científicas más prestigiosas a nivel mundial,
más del 70 por ciento de los 1,576 investigadores encuestados no han podido reproducir alguno de sus propios
experimentos. Además, los datos son claros, la mayoría piensa que existe una *crisis de reproducibilidad*
(ver Figura \ref{fig:nature}).

![Resultados de la encuesta sobre reproducibilidad. Fuente: [@baker500ScientistsLift2016]](source/figures/nature_survey.jpeg){#fig:nature}

A día de hoy, los estudios suelen ofrecer los resultados en forma de gráficas y tablas, pero en muchos casos
carecen de la información necesaria para poder contrastar los resultados. Está información suele
ser, el entorno de ejecución, los datos originales y la implementación de los propios métodos (modelos,
algoritmos, etc) entre otros. Para aumentar la accesibilidad de los estudios, los investigadores deben asegurarse
de ofrecer esta información además de las gráficas y tablas.

La verificación independiente tiene como objetivo la confirmación de credibilidad y la extensión del conocimiento
en un área. La investigación relativa al *Machine Learning* o a otras areas donde se haga uso del mismo, no
está exenta de este requisito de la investigación científica. Por tanto, adoptando un flujo de trabajo reproducible, estamos
ofreciendo a la audiencia las herramientas necesarias que demuestran las decisiones tomadas y que permiten validar nuestros resultados.
Por otro lado, para que un estudio computacional pueda  ser reproducido correctamente por un investigador independiente
 es necesario el acceso completo a los datos, código, parámetros de los experimentos, información sobre el entorno de ejecución, etc. 
 
Otro motivo de interés para la búsqueda de la reproducibilidad es el de facilitar el uso de nuestros métodos por el resto
de la comunidad científica o incluso en aplicaciones comerciales. Ofreciendo acceso a los datos y al código, como se ha comentado antes,
permitimos que nuestros métodos se puedan aplicar a otros problemas, tanto en investigación como para fines comerciales, así como
facilita la extensión de nuestro trabajo.

En los últimos años nos hemos encontrado con muchos casos de publicaciones científicas que
muestran resultados difíciles o incluso imposibles de reproducir. Este fenómeno se conoce como
la crisis de la reproducibilidad, donde incluso estudios prominentes no se pueden reproducir
[@pengReproducibilityCrisisScience2015; @baker500ScientistsLift2016] .
Este fenómeno ha estudiado de manera extensiva en otros campos, pero en el área del *Machine Learning*
está tomando últimamente mucha importancia. Esto es debido a que tradicionalmente, los experimentos
científicos se deben describir de tal forma que cualquiera pueda replicarlos, sin embargo, los experimentos
computacionales tienes varias complicaciones que los hacen particularmente difíciles de replicar: versiones
de software, dependencias concretas, variaciones del hardware, etc.

Con motivo de esta crisis de la reproducibilidad que afecta en gran medida a AI/ML, conferencias como
NeurIPS han optado por añadir este factor en su proceso de revisión, e implementan
políticas para alentar el código compartido [@gibneyThisAIResearcher2019]. Por otro lado, algunos autores
(incluido nosotros) han propuesto herramientas para facilitar la reproducibilidad, mientras que otros
han propuesto una serie de reglas o heurísticas que para evaluar este aspecto
[@wilsonGoodEnoughPractices2017; @collbergMeasuringReproducibilityComputer; @sandveTenSimpleRules2013].


### Tipos de reproducibilidad

Para poder atajar de una manera directa y eficiente el problema de la reproducibilidad es necesario separarla
en diferentes niveles [@EdgeOrg]. Esta separación nos permite desarrollar una serie de buenas prácticas y herramientas
específicas para cada nivel, así como ver, de una manera clara, cuales aspectos se pueden recoger en un *framework* común,
y cuales son inherentes del estudio científico en cuestión. Entre los niveles de reproducibilidad  podemos destacar:

- **Reproducibilidad computacional**. Cuando se provee con información detallada del código, software, hardware y decisiones de implementación.


- **Reproducibilidad empírica**. Cuando se provee información sobre experimentación empírica no computacional u observaciones.


- **Reproducibilidad estadística**. Cuando se provee información sobre la elección de los test estadísticos, umbrales, p-valores, etc.


Una vez hecha separación del problema en tres capas, podemos ver claramente que la reproducibilidad computacional debe ser nuestro
objetivo a la hora de desarrollar el *framework*. Mientras que la reproducibilidad empírica se puede conseguir
en mayor medida, haciendo los datos accesibles, la reproducibilidad estadística se consigue mediante el desarrollo de un diseño inicial
del estudio. En este diseño se especifica la hipótesis base, las asunciones del problema, los test estadísticos a realizar,
y los p-valores correspondientes. El establecer las bases estadísticas sobre las que se va a desarrollar el estudio de antemano,
nos puede ayudar además a evitar problemas como el *p-hacking* [@headExtentConsequencesPHacking2015].

Por otro lado, el término reproducibilidad además de poder descomponerse según la información o parte del trabajo que se
esté tratando, llamémosla la escala o eje horizontal, también se puede descomponer en otro eje, llamémosle vertical,
que indica como de replicable y reproducible es un estudio en su conjunto. Los niveles de esta nueva escala son los
siguientes [@stoddenSettingDefaultReproducible2013]:

- **Investigación revisable**. Las descripciones de los métodos de investigación pueden ser
evaluados de manera independiente y los resultados juzgados. Esto incluye tanto los tradicionales
*peer-review, community-review*, y no implica necesariamente reproducibilidad.

- **Investigación replicable**. Se ponen a disposición del público las herramientas que
necesarias para replicar los resultados, por ejemplo se ofrece el el código de los autores para producir
las gráficas que se muestran en la publicación. En este caso, las herramientas pueden tener un alcance limitado,
ofreciendo los datos ya procesados y esenciales, así como ofreciéndolas mediante petición exclusivamente.

- **Investigación confirmable**. Las conclusiones del estudio se pueden obtener sin el uso del software proporcionado por el autor.
Pero se debe ofrecer una completa descripción de los algoritmos y la metodología usados en la publicación y cualquier
material complementario necesario.

- **Investigación auditable**. Cuando se registra la suficiente información sobre el estudio
(incluidos datos y programas informáticos) para que la investigación pueda ser defendida posteriormente si es necesario 
o para llevar a cabo una resolución en caso de existir diferencias entre confirmaciones independientes.
Esta información puede ser privada, como con los tradicionales cuadernos de laboratorio.

- **Investigación abierta o reproducible**. Investigación auditable disponible abiertamente. El código y los datos se
encuentran lo suficientemente bien documentados y accesibles al publico para que la parte computacional
se pueda auditar, y lo resultados del estudio se puedan replicar y reproducir de manera independiente.
También debe permitir extender los resultados o aplicar el método desarrollado a nuevos problemas.


### Aspectos críticos

Una vez hemos definido los diferentes niveles de reproducibilidad, vamos a definir los aspectos que consideramos
críticos para lograr una investigación *abierta o reproducible*
[@moraila2014measuring; @olorisadeReproducibilityMachineLearningBased2017; @pengReproducibleResearchComputational2011; @sandveTenSimpleRules2013;
@stoddenSettingDefaultReproducible2013; @wilsonGoodEnoughPractices2017].

- **Conjunto de datos**: La información sobre la localización y el proceso de extracción de los datos. Este factor
es determinante a la hora de hacer un estudio reproducible. El objetivo es el de facilitar los datos y/o
la forma de extraerlos. En caso de que los datos no sean accesibles públicamente, o que los datos que se ofrezcan
no sean los extraídos en crudo, estaríamos ante un *estudio replicable*, pero no reproducible.

- **Preprocesado de datos**: En este aspecto se recogen los diferentes pasos del proceso de transformación de los datos.
Un investigador independiente debería ser capaz de repetir los datos de preprocesado fácilmente.
Sería también interesante incluir datos ya preprocesados con los que comparar y validar que las transformaciones
se han realizado correctamente. Estos procedimientos no son sencillos de documentar ni de compartir.
En algunas ocasiones, las transformaciones se realizan en software privativos o utilizando una interfaz gráfica.
En esos casos, en lugar de ofrecer los scripts de preprocesado, sería más interesante dar una descripción detallada
de como los datos se han transformado. Además, sugerimos favorecer las herramientas de código libre en caso de que
existan como alternativa a algunas de las herramientas privadas.

- **Partición de los datos**: En caso de que los datos se separen, por ejemplo para ajustar un modelo y validarlo,
es necesario proporcionar los detalles de como se ha realizado esta separación. En el caso de que dicha separación
sea aleatoria, como mínimo se debe proporcionar la semilla y el tipo de muestreo (estratificado o no, por ejemplo).
Aunque preferiblemente, todo este procedimiento debe estar recogido en un script.

- **Ajuste del modelo**: Corresponde a toda la información relativa al ajuste de un modelo. En este caso, es necesario
hacer disponible toda la información posible en relación a este proceso y a las decisiones tomadas. La información
mínima que se debe proporcionar es:

    1. Parámetros del experimento
    2. Métodos propuestos: detalles de implementación, algoritmos, código, etc (si es aplicable).

- **Evaluación del modelo**: Información sobre como se evalúa un modelo entrenado. Información similar al punto anterior
se aplica aquí.

- **Control de la estocasticidad**: La mayoría de operaciones en *Machine Learning* tienen un factor de aleatoriedad.
Por tanto, es esencial establecer los valores de las semilla que controlar dichos procesos.
La mayoría de herramientas de cálculo científico ofrecen algún método para establecer la semilla del
generador de números aleatorios.

- **Entorno software**: Debido al hecho de que los paquetes/módulos de software están en continuo
desarrollo y sufren posibles alteraciones de los algoritmos internos, es importante
que los detalles del entorno de software utilizado: módulos, paquetes y números de versión..., estén disponible.

- **Entorno hardware**: Algunos estudios, sobre todo los que contienen grandes cantidades de datos, son
reproducibles exclusivamente cuando se ejecutan en una cierta máquina, o al menos, cuando se cumplen unos
requisitos de hardware determinados. Otro problema que surge en algunos casos y que está estrechamente relacionado
con el punto anterior, es el de las versiones de los drivers. Por este motivo, se requiere una correcta documentación
de los recursos utilizados, tanto [!gpu] como CPU, así como de las versiones de sus drivers correspondientes.


## Proceso de ciencia de datos y deuda técnica

La mayoría de proyectos de ciencia de datos recogen una serie de pasos distinguidos. Una vez definido el caso
comercial (el producto), y la métrica que mide el éxito, los pasos para llevar a cabo un proyecto de *Machine Learning*
son los siguientes [@kelleherSTANDARDDATASCIENCE2018; @MLOpsContinuousDelivery]:

- **Extracción de datos**: Se seleccionan e integran datos de diferentes fuentes que sean relevantes para el problema.

- **Análisis de datos**: En este paso se realiza un análisis exploratorio (EDA) con el fin de comprender el modelo de
datos, realizar asunciones, identificar posibles características relevantes, y preparar un plan para la ingeniería de
características y el preprocesado de datos.

- **Preparación de los datos**: Se preparan los datos para la tarea en cuestión. Se realizan las particiones de datos,
se limpian y transforman los mismos para adaptarlos al problema, y se lleva a cabo la ingeniería de características.
El resultado de este proceso es una seria de conjuntos de datos listos para entrenar, evaluar y validar modelos.

- **Ajuste de modelos**: Aquí se lleva a cabo el entrenamiento de modelos. Se implementan diferentes algoritmos y se
realiza un ajuste de hiperparámetros con el fin de obtener el mejor modelo posible.

- **Evaluación de modelos**: Se evalúa el modelo utilizando los conjuntos de validación y/o test.

- **Validación de modelos**: Se realiza una confirmación del rendimiento del modelo para comprobar que es adecuado
para la implementación. Para ello se compara su rendimiento predictivo con un modelo de referencia determinado,
denominado **baseline**.

- **Entrega o despliegue del modelo**: Se implementa el modelo final en el *entorno de destino* para hacer las predicciones
disponibles a los usuarios.

- **Monitorización del modelo**: Se supervisa el rendimiento del modelo con el fin de planificar las siguientes iteraciones.

### Deuda técnica

Como se puede observar, los pasos de este proceso siguen un orden estricto, lo cual lo hace resonar a un modelo de
desarrollo en cascada. Al igual que el resto de aplicaciones del desarrollo software, la deuda técnica es un factor
vital a tener en cuenta. Un factor que puede ralentizar enormemente las iteraciones, y que se va acumulando
en cada paso del proceso. Además, la alta dependencia que hay en el orden de los pasos del proceso de ciencia de datos,
hace muy difícil la refactorización.

La deuda técnica [@kruchtenTechnicalDebtMetaphor2012] es un concepto acuñado en el desarrollo software para describir
aquellas decisiones, que se toman por falta de tiempo o conocimiento, que provocan un coste adicional
sobre los nuevos cambios conforme pasan el tiempo. Este término está basado en el concepto de *deuda monetaria*,
y al igual que este tipo de deuda, si no se paga temprano, el coste adicional aumenta de manera exponencial
(*intereses compuestos*). Algunas de las causas de deuda técnica son: falta de tests, falta de documentación,
falta de conocimiento, presión comercial (deadlines irreales), refactorización tardía, entre otros.

Además de la deuda técnica originada por el propio desarrollo software, existe
unos elementos particulares al proceso de ciencia de datos que pueden aumentar drásticamente esta deuda
[@sculleyHiddenTechnicalDebt2015; @sculleyMachineLearningHigh2014]:

- **Bucles de retroalimentación**: Este problema ocurre cuando, de manera indirecta, la salida del modelo influencia 
la entrada al mismo. De esta forma, los sistemas de [!ml] modifican su propio comportamiento conforme pasa el tiempo.
Este tipo de errores parecen sencillos de resolver, pero en la práctica, conforme se integran
diferentes sistemas la probabilidad de que estos se retroalimenten entre si es muy alta. Incluso si dos
sistemas de [!ml] parecen no estar relacionados, este problema puede surgir. Imagínese dos sistemas que predicen del valor de
acciones de un mismo mercado para dos compañías distintas. Mejoras o peor aún, bugs de un sistema, pueden influir en el
comportamiento del otro sistema.  

- **Cascadas de corrección**: Este problema ocurre cuando el modelo de [!ml] no aprende lo que se esperaba, y se terminan
aplicando una serie de parches (heurísticas, filtros, calibraciones, etc.) sobre la salida del modelo. Añadir un parche
de este tipo puede sen tentador incluso cuando no hay restricciones de tiempo. El problema principal es que la métrica
que el modelo intenta optimizar se descorrelaciona con la métrica general del sistema. Conforme esta capa de
heurísticas se vuelve más grande, es difícil reconocer cambios sobre el modelo de [!ml] que mejoraren la métrica final,
dificultando de esta forma la iteración y mejora continua.

- **Características basura**: Características que no aportan nada al sistema, incluso pueden perjudicar el rendimiento.
Algunas de las características basura que podemos encontrar son:

    - Características agrupadas: Cuando se agrupan varias características y se evalúan en conjunto, es difícil saber
    si todas las características aportan, o si simplemente hay algunas que son beneficiosas y otras no.
    - $\epsilon$-Características: Algunas características que se añaden mejoran muy poco el rendimiento del modelo. Aunque
    es tentador añadir este tipo de características, el problema emerge cuando dichas características dejan de mejorar
    el modelo o incluso lo empeoran cuando los datos cambian mínimamente.
    - Características obsoletas: Conforme pasa el tiempo, algunas características se vuelven obsoletas, porque o bien
    no aportan la información correcta, o bien la información que aportan ya se recoge en otras variables. Para
    evitar este problema, revaluar la importancia de las características con el paso del tiempo.

- **Deuda de configuración**: Sistemas de [!ml] están compuestos por diferentes partes, cada una con un configuración
específica. Los modelos y pipelines en general, deben de ser fácilmente configurables. Además, la organización
de ficheros y el sistema de configuración debe facilitar lo siguiente:
  - Modificar configuraciones existentes fácilmente
  - Comparar y ver claramente la diferencias entre configuraciones de modelos
  - Detectar configuraciones redundantes
  - Revisión de código sobre las configuración y su inclusión en un control de versiones.

- **Deuda de reproducibilidad**: Como se verá en la sección siguiente, es importante que como investigadores,
podamos reproducir experimentos y obtener los mismos resultados fácilmente. Aunque en los sistemas ML
reales es realmente difícil conseguirlo; debido principalmente a la naturaleza no determinística de los
algoritmos, del entrenamiento en paralelo, y de las interacciones con el mundo exterior.

### Anti-patrones

![Solamente una fracción pequeña es dedicada al código de [!ml]. El resto de código de arquitectura es necesario,
y complejo. Fuente: [@sculleyHiddenTechnicalDebt2015]](source/figures/technical_debt.png){#fig:technical_debt}

Sorprendentemente, en la mayoría de sistemas de [!ml], solamente una pequeña fracción del código está dedicado
al entrenamiento y predicción. El resto de código, conocido como *plumbing*, es susceptible a una serie
de anti-patrones que se describen a continuación:
 
 - **Código pegamento**: A pesar de que en la comunidad existen numerosos paquetes y soluciones para [!ml].
 El utilizar herramientas genéricas puede hacer que el sistema dependa mayoritariamente de ellas.
 Eso provoca que en algunos casos haya una gran cantidad de código solamente para introducir y extraer
 datos de estas soluciones *open source*. Si nuestro sistema tienen una gran proporción del código dedicado
 a adaptar los datos y algoritmos a un paquete de propósito general, deberíamos plantearnos crear
 una solución propia.
 
 - **Junglas de pipelines**: La mayoría de sistema integran multiples fuentes de información.
 Estas fuentes de información, así como las transformaciones pertinentes sobre los datos,
 suelen evolucionar a lo largo del desarrollo. Esto induce a un caso particular de *código pegamento*
 donde se hace muy complicado poder testear, recuperarse de errores, etc. Una forma de subsanar este problema,
 es diseñado el sistema holísticamente (teniendo en cuenta todo el pipeline), en lugar de enfocarse en los
 pasos intermedios. Además, también sería beneficioso, en la medida de lo posible, aplicar los conceptos
 de *programación funcional*.
 
 - **Código muerto**: Los proyectos de [!ml] se basan en la experimentación. Al cabo del tiempo, estos sistemas
 pueden acabar con una gran cantidad de código dedicados experimentos que nunca han visto la luz.
 
 - **Deuda de abstracción**: Los problemas anteriores reflejan una falta de abstracción para los sistemas de [!ml],
 como puede ser un lenguaje común de alto nivel para definir las fuentes de datos, modelo y predicciones.
 
 - ***Code-smells* más comunes**: Algunos de los indicadores de *peligro* en la implementación de sistemas de [!ml] son los siguientes:
    - *Tipos de datos planos*: En un sistema robusto, la información producida en el mismo se almacena enriquecida.
    Se debe saber si un parámetro de un modelo es un *umbral* o no, si una variable está en escala logarítmica, etc.
    Así como debe haber claras indicaciones de cómo se ha producido la información y cómo se debe ser consumida. 
    - *Multiples lenguajes*: Es tentador utilizar diferentes lenguajes para un mismo sistema de [!ml] cuando hay
    soluciones o sintaxis conveniente para cada componente. Sin embargo, esto limita la movilidad del capital humano,
    así como complica el testing.
    - *Prototipos*: Todo sistema de [!ml] parte de un prototipo. Sin embargo, es necesario un código bien testeado y listo
    para producción en cualquier parte de estos sistemas. Aunque es complicado llevarlo a la práctica cuando existen
    unas restricciones de tiempo fuertes.

 
## *Machine Learning Operations (MLOps)*

Durante los últimos años, el papel de la ciencia de datos y del *Machine Learning* ha tomado gran relevancia en la
industria. En la actualidad,  la ciencia de datos se utiliza para resolver problemas complejos, y ofrecer una
gran variedad de productos de datos: traductores automáticos [@bar-hillelPresentStatusAutomatic1960],
sistemas de recomendación [@luRecommenderSystems2012], sistemas de trading de alta frecuencia
[@trippiArtificialIntelligenceFinance1995; @kearns2013machine], etc.  
La ciencia de datos ha podido ser aplicada a una variedad muy amplia de campos, ha aportado valor en cada uno de ellos,
incluso ha revolucionado algunas industrias . Para que esto haya sido posible, y para que siga siendo posible, es necesario
una gran cantidad de datos, recursos de computación (CPU y [!gpu]) accesibles, hardware optimizado para cálculo científico, así
como una activa comunidad de investigadores.

El hecho de que cada vez más industrias estén implementado sistemas de [!ml] como productos o parte de productos comerciales,
hace indispensable unos flujos de desarrollo orientados a la industria. La ciencia de datos parte originalmente de la experimentación,
no obstante, conforme los sistemas de [!ml] se integran con el resto de componentes de una organización, es necesario aplicar
las técnicas y buenas prácticas conocidas en el desarrollo software, con el fin de ofrecer a los usuarios sistemas
predictivos con valor comercial y mínimo coste. Los científicos de datos pueden implementar y entrenar modelos localmente,
sin conexión a Internet incluso, pero el verdadero desafío consiste en implementar un sistema [!ml] completo, y operarlo
en producción de manera continua [@polyzotisDataManagementChallenges2017; @polyzotisDataLifecycleChallenges2018; @schelterChallengesMachineLearning2018].

Como se ha detallado en la sección anterior el ciclo de desarrollo de un producto de
un sistema [!ml] implica diferentes fases. El código relacionado con la propia implementación y entrenamiento de modelos
es mínimo comparado con el resto de código necesario para el desarrollo de estos sistemas (ver Figura \ref{fig:technical_debt}).
Además, debido a la necesidad de grandes cantidades de datos y de recursos computaciones amplios, estos sistemas
deben incluir otros módulos relativos a la infraestructura: manejos de recursos, monitorización, automatización, etc.
Por lo que el desarrollo de sistemas de [!ml] en la industria no consiste solamente en entrenar modelos, o recolectar y procesar datos,
sino que requiere de una amplia base de desarrollo software, la cuál, es carente en muchos equipos de ciencia de datos multidisciplinales.

Para poder lidiar con los problemas inherentes a la aplicación de ciencia de datos a la industria, y para poder abstraer a los científicos de datos sobre
la infraestructura, en los últimos años se ha ido desarrollando el concepto de *MLOps*.
Las prácticas de la filosofía MLOps se fundamentan en DevOps, una filosofía de buenas prácticas para el desarrollo de software.
Es por eso que es necesario hacer una breve introducción ha dicho concepto antes de profundizar en *MLOps*.


### DevOps. Definición

Para poder desarrollar sistemas software complejos, la tendencia actual es utilizar las técnicas de *DevOps*.
*DevOps* es un conjunto de prácticas en el desarrollo y operacionalización. Estas prácticas aumentan la velocidad
de implementación, reducen los ciclos de desarrollo, y facilitan la entrega de actualizaciones. Entre las prácticas
recogidas en este concepto se incluyen:

- **[!ci!]**: Esta práctica de desarrollo software permite a los desarrolladores ejecutar versiones y pruebas automáticas
cuando se combinan cambios de código en el repositorio del proyecto. Esto permite validar y corregir errores con mayor rapidez,
mejorando así la calidad del software.

- **[!ci!]**: Esta práctica de desarrollo software se basa en la compilación, prueba y preparación automática
de artefactos. Estos artefactos se generan automáticamente cuando se producen cambios en el código y se entregan a la
fase de producción. De esta forma, las actualizaciones a los usuarios finales se entregar con mínimo esfuerzo.
Travis o CircleCI son algunos de los servicios que ofrecen tanto *Integración Continua* como *Entrega Continua*.

- **Microservicios**: La arquitectura de microservicios es un enfoque de diseño que permite crear una aplicación
a partir de un conjunto de servicios pequeños. Cada servicio se ejecuta de manera independiente y se comunica con los otros
servicios a través una interfaz ligera, normalmente HTTP. Recientemente, algunos otros protocolos de nivel superior como
gRPC o GraphQL se están utilizando para la interconexión de estos servicios.

- **Infraestructura como código**: Aprovisionar y administrar infraestructura con técnicas de desarrollo de programación
y desarrollo software, como el control de versiones. Algunos servicios como AWS, CloudFormation o Terraform permiten
aprovisionar y gestionar infraestructuras utilizando lenguajes de programación o ficheros de configuración.

- **Monitorización y registro**: Monitorizar métricas y registros para analizar el desempeño de las
aplicaciones y la infraestructura sobre la experiencia usuario.

- **Comunicación y colaboración**: Uno de los aspectos claves en la filosofía *DevOps* es el 
incremento de la comunicación y la colaboración en las organizaciones.


### *DevOps* aplicado al *Machine Learning*

*MLOps* se fundamenta en los principios y prácticas de *DevOps*. Nociones, como se
ha comentado previamente, orientadas a la eficiencia en el desarrollo: integración y entrega
continuos, monitorización, etc. *MLOps* aplica estos principios para la entrega de sistemas
de [!ml] a escala, resultando en:

- Tiempo de comercialización de soluciones basadas en [!ml] menor.
- Ratio de experimentación mayor que fomenta la innovación.
- Garantía de calidad, confidencialidad e *[!ia<] ética*.


![El desarrollo de sistemas de [!ml] es complejo e implica varios pasos bien diferenciados. MLOps tiene
como objetivo mejorar cada uno de los pasos, pero especial aquellos que corresponden a la etapa de
Operaciones. Fuente: [@arnoldAutomatingAIOperations2020]](source/figures/mlops_overview.png){#fig:mlops_overview}


Para poder analizar la interacción entre DevOps y el desarrollo de sistemas de [!ml], es necesario
destacar las tareas claves de este proceso. Teniendo en cuenta el proceso de ciencia de datos
descrito en la sección anterior, (también representado en la Figura \ref{fig:mlops_overview})
podemos destacar las siguientes tareas:

- **Recolectar y preparar datos**: Generar y preparar los conjuntos de datos para el entrenamiento.

- **Aprovisionar y gestionar la arquitectura**: Establecer los entornos de computación donde
se se entrenan los modelos y despliegan los modelos.

- **Entrenar modelos**: Desarrollar el código de entrenamiento y evaluación, y ejecutarlos
en la infraestructura aprovisionada.

- **Registrar modelos**: Después de la ejecución de un experimento, el modelo resultado
se almacena en el *registro de modelos*.

- **Desplegar el modelo**: Validar los resultados del modelo, desplegarlo en el *entorno objetivo*. 

- **Operar el modelo**: Operar el modelo en producción monitorizándolo para conocer
su rendimiento, detectar *desfases de datos*, alerta de fallos, etc.

Esta secuencia de actividades se corresponde con un *pipeline*. La dificultad principal
en el diseño de este pipeline es que cada paso es altamente iterable. Es decir,
los modelos necesitar ser modificados, los resultados testeados, se añaden nuevas fuentes
de información, etc. El poder iterar de una manera eficiente es fundamental para este tipo
de sistemas. Además, existen ciertos requisitos que solamente se conocen una vez que el modelo
se monitoriza. Como pueden ser el *desfase de datos*, sesgo inherente o fallos del sistema.

Para responder a estos desafíos de manera exitosa, los equipos de [!ml] deben implementar las
siguientes prácticas [@mcknightDeliveringVisionMLOps2020].

- **Reproducibilidad**: Como se ha explicado en al principio del capítulo, este aspecto
es fundamental y es uno de los objetivos de *MLOps*. Cuando se automatizan los diferentes
pasos del proceso de ciencia de datos, es necesario que cada paso sea determinista, para
evitar resultados indeseables. 

- **Reusabilidad**: Para poder ajustarse a los principios de *entrega continua*, la *pipeline* necesita
empaquetar y entregar modelos y código de una manera consistente, tanto a los entornos locales de
entrenamiento como a los *entornos objetivos*, de forma que una misma configuración pueda
arrojar los mismos resultados.

- **Manejabilidad** – La habilidad de aplicar regulación, rastrear los cambios en los modelos y código a lo largo
del ciclo de vida, y permitir a los managers y gestores de equipo medir el progreso
del proyecto y el valor comercial.

- **Automatización** – Al igual que en DevOps, para aplicar integración y entrega continua se require
automatización. Los *pipelines* deben ser fácilmente repetibles, especialmente cuando se aplica gobernanza, o
testing. Desarrolladores y científicos de datos pueden adoptar *MLOps* para
colaborar y asegurar que las iniciativas de [!ml] están alineadas con el resto de entrega del software,
así como con el negocio en general.

![Tabla que resume los aspectos claves de la adopción de MLOps en la industria a diferentes niveles según el
modelo de madurez descrito en esta sección. Fuente: [@mcknightDeliveringVisionMLOps2020]](source/figures/mlops_levels.jpg){#fig:mlops_levels}

Las prácticas anteriores son un indicador de la madurez del equipo de ciencia de datos, así como de las relaciones
con el resto de equipos de desarrollo, y la compañía. Cada compañía puede implementar estas prácticas a diferentes
niveles. El modelo de madurez de *MLOps* se denomina *MLOps Maturity Model*. En la figura \ref{fig:mlops_levels}) se muestra un
resumen de cada nivel según este modelo. Las categorías recogidas en él son las siguientes:

- **Estrategia**: Como la compañía puede alinear las actividades de *MLOps* con las prioridades ejecutivas, de organización y culturales.
- **Arquitectura** – La habilidad para manejar datos, modelos, entornos de despliegue y otros artefactos de manera unificada.
- **Modelado** – Habilidades de ciencia de datos y experiencia, que sumados al conocimiento de dominio, permitan el desarrollo y entrega
de sistema de [!ml] para dicho dominio.
- **Procesos** – Entrega y despliegue de actividades de manera eficiente, efectiva y mensurable, que impliquen científicos, ingenieros y administradores.
- **Gobernanza** – En general, la habilidad para construir soluciones de inteligencia artificial seguras, responsables y justas.

### *MLOps* y Reproducibilidad

Como se puede observar, *MLOps* y el problema de la reproducibilidad están estrechamente relacionados.
Para poder implementar correctamente las buenas prácticas de *MLOps*, es necesario que cada paso del
proceso sea lo más reproducible y determinista posible. Esto es un requisito necesario para poder
implementar las prácticas de integración y entrega continua, ya que se fundamentan en la automatización.
Por tanto, las prácticas descritas en la sección de *Reproducibilidad* sobre el control de las particiones
de datos, estocasticidad, parámetros del experimento, etc. deben ser aplicados también para el desarrollo
de sistemas de [!ml] en la industria.

Por la razón anterior, la mayoría de software y plataformas orientadas a *MLOps* ofrecen herramientas para
la gestión y control de experimentos, así como control sobre el entorno software y/o hardware. Además, las herramientas
de *MLOps* están orientadas en su mayoría a la ejecución de trabajos en la nube y la colaboración. Esto puede
ser de utilidad para la investigación, cuando se estén tratando con datos o algoritmos que requieran de una capacidad
de cómputo superior a los ordenadores locales. Es por eso que nuestro objetivo principal va a ser el estudio de las
diferentes herramientas para *MLOps* y el desarrollo de nuestra propia herramienta con foco en la reproducibilidad.

## Estado del Arte

En esta sección vamos a analizar el estado del arte para las herramientas de *MLOps*, herramientas orientadas a la reproducibilidad
exclusivamente, así como el trabajo realizado hasta la fecha en relación al problema a resolver.

### Herramientas para la reproducibilidad

Existen herramientas dedicadas a facilitar la reproducibilidad de experimentos en el campo de la investigación.
A continuación, se resumen algunas de las herramientas más utilizadas:

- **Reprozip**: *Reprozip* [@rampinReproZipReproducibilityPacker2016] es una utilidad de
código libre cuyo objetivo es el de empaquetar todo el trabajo con sus respectivas dependencias,
variables de entorno, etc, en un paquete autocontenido.
Una vez creado ese paquete, *Reprozip* puede restablecer el entorno tal y como se originó para que se
pueda reproducir en una máquina distinta, ahorrando al usuario de la instalación de dependencias
y la configuración del entorno. *Reprozip* puede utilizarse con cualquier lenguaje de programación y
con una gran variedad de herramientas de análisis, incluidos los cuadernos de *Jupyter*.

- **Sacred**: Sacred [@IDSIASacred2020a] es una herramienta en Python, cuyo objetivo es el de facilitar la configuración, organización y
registro de experimentos. Está diseñada para añadir una sobrecarga mínima y permitir la modularidad y configuración
de experimentos. Las funcionalidades principales de esta herramienta son:
  - Registrar los parámetros de los experimentos
  - Facilitar la ejecución de experimentos con diferente configuración 
  - Almacenar la información sobre los experimentos en una base de datos
  - Reproducir los resultados
Además, se integra fácilmente con herramientas de visualización de monitorización de experimentos como *Tensorboard*.

### Herramientas para *MLOps*

- **MLFlow:** MLFlow [@zahariaAcceleratingMachineLearning2018] es una herramienta de código abierto para el manejo
del ciclo de vida completo de un proyecto de [!ml], incluida la experimentación, reproducibilidad y despliegue.
Actualmente, este proyecto ofrece tres módilos principales: Tracking, Projects, Models.
  - *Tracking*: La API de Tracking permite registrar experimentos, parámetros, métricas, artefactos, y otros metadatos.
  - *Projects*: El module de Projects permite empaquetar y distribuir los proyectos usando un formato simple como YAML.
    En este fichero se le especifican las dependencias, el entorno, los parámetros, y el punto de entrada del proyecto.
  - *Models*: El módulo Models permite empaquetar modelos de los frameworks más conocidos - Tensorflow, Pytorch, Sklearn, MXNet, etc,
    en un formato genérico, almacenarlos en un *Registro de modelos* (ver Nomenclatura), y desplegarlos.
  Soporta múltiples lenguajes y ofrece una API REST para la consulta de información por servicios externos.

- **CometML**: Comet [@CometBuildBetter] ofrece una plataforma para el registro, rastreo, comparación y optimización de experimentos y
modelos. Esta plataforma está basada en cloud (aunque con soporte para alojarlo en servidores propios).
Algunas de las características a destacar son: soporte para cuadernos de *Jupyter*, optimización de hiperparámetros
nativa (*meta-learning* [@seitaLearningLearn]), y un potente sistema de visualización. Además, permite recoger métricas
del sistema - uso de CPU, memoria, etc, a lo largo de la ejecución de los experimentos. Soporta múltiples lenguajes y
ofrece una *API REST* para la consulta de información por servicios externos.

- **Polyaxon**: *Polyaxon* [@PolyaxonMachineLearning] es una herramienta enfocada también al ciclo de vida completo de un proyecto de [!ml].
La plataforma utiliza Kubernetes [@ProductionGradeContainerOrchestration] para hacer los proyectos reproducibles, escalables y portables.
Esta herramienta permite definir experimentos, almacenar información (métricas, parámetros, etc), así como desplegar modelos.
Una funcionalidad que ofrece esta herramienta, que no se encuentra en las dos anteriores, es soporte propio para
optimización de hiperparámetros. Además, ofrece un completo sistema de manejo de usuarios y un marketplace de
integraciones. Esta plataforma es ideal para organizaciones de tamaño medio-grande que requieran una gestión
de usuarios y roles completa, escalabilidad, y gobernanza sobre los modelos desplegados.

- **Kubeflow**: El objetivo de *Kubeflow* [@Kubeflow] no es implementar una plataforma para el ciclo de vida ni para el manejo de modelos,
el objetivo principal es el de despliegue de flujos de trabajo completos en Kubernetes. Esta herramienta
permite desplegar modelos en diferentes infraestructuras de forma sencilla, portable, y escalable.
Por otro lado, con *Kubeflow Pipelines* se pueden desplegar *pipelines* completas usando *Argo* como
motor.

- **Amazon SageMaker**: *SageMaker* [@AmazonSageMaker] es la plataforma de [!ml] de Amazon Web Services (AWS) . Esta plataforma integra
herramientas que cubren todo el proceso de ciencia de datos. Incluye servicios de gestión de datos y etiquetado,
cuadernos de Jupyter en la nube, registro y seguimiento de experimentos, despliegue, monitorización, y optimización
de hiperparámetros. Hay varias características que hacen única esta plataforma, entre ellas: ofrece un IDE orientado
a [!ml] (Amazon SageMaker Studio), ofrece herramientas de depuración (Amazon SageMaker Debugger), y una integración
con el servicio de etiquetado humano Amazon Mechanical Turk.

- **Google AI Platform**: La nube de [!gcp] ofrece un conjunto de herramientas que cubren todo
el proceso de ciencia de datos. A este conjunto de herramientas se le conoce como *Google AI Platform* [@AIPlatform],
aunque cada herramienta se puede utilizar por separado. Para la gestión y procesado de datos Google Cloud
ofrece bases de datos a escala (*BigQuery*), un y un servicio de etiquetado automático (*Data Labelling Service*).
Para la construcción y entrenamiento de modelos, [!gcp] ofrece imágenes de máquinas virtuales, servicios 
de *cuadernos de Jupyter* en la nube, y otras herramientas para la ejecución de trabajos en la nube.
Además, todos los trabajos se pueden ejecutar tanto en máquinas de [!gcp], como en servidores propios gracias
al soporte para *Kubeflow Pipelines*.

- **Azure Machine Learning**: El conjunto de servicios y herramientas para ciencia de datos de Azure se llama
*Azure Machine Learning* [@AzureMachineLearning]. Al igual que la [!gcp], Azure ofrece herramientas para todas las etapas del ciclo de
vida del proceso de ciencia de datos. Azure Machine Learning ofrece soporte para pipelines reproducibles,
imágenes de maquinas virtuales, gestión del código y datos, etc. Además, ofrece soporte para seguimiento
de experimentos e hiperparametrización. Una característica interesante es que ofrece la posibilidad de
empaquetar modelos en formato ONNX [@OnnxOnnx2020] y desplegarlos en diferentes entornos objetivos ofertados por
Azure, incluido instancias con FPGA [@shawahnaFPGABasedAcceleratorsDeep2019].

- **Neptune**: *Neptune* [@DataScienceCollaboration] ofrece una biblioteca de código libre para Python con la que poder
registrar y hacer un seguimiento de experimentos. Neptune ofrece una gestión de proyectos y un sistema de usuarios y roles completo.
Además, cada experimento puede ser visualizarlo, compartido y debatido entre los diferentes miembros del equipo.
*Neptune* es un framework ligero pero se integra fácilmente con diferentes herramientas, como MLFlow.
En lugar de enfocarse en todo el proceso de ciencia de datos, el objetivo principal de esta herramienta es el
de gestionar experimentos y registrar toda la información de una manera sencilla.


### Análisis de rayos gammas


## Modelos utilizados: Redes neuronales

Para el experimento llevado a cabo se ha propuesto la aplicación de una técnica clásica para la clasificación
de partículas. Se ha trabajado con redes neuronales, en concreto con *autoencoders*, debido principalmente a su
eficacia, robustez, flexibilidad, entre otras característica.

Las redes neuronales son algoritmos de aprendizaje automático que han adquirido una gran
popularidad en los últimos años, y que han sido desarrollados y utilizados en una gran variedad
de problemas: aprendizaje supervisado, no supervisado, aprendizaje por refuerzo, y reducción de la dimensionalidad, entre otros.

Para describir una red neuronal vamos a empezar por la arquitectura más básica, una sola neurona.
Una forma de representar dicha neurona en una diagrama es la siguiente:

![Diagrama de una neurona, también llamada unidad. Fuente: [@ng2011sparse]](source/figures/single_neuron.png){#fig:neuron width=60%}

Una neurona no es más que una unidad computacional que toma como entrada un vector $x$ (más un elemento a 1 para el sesgo),
y cuya salida es $h_{W, b}(x)=f\left(W^{T} x\right)=f\left(\sum_{i=1}^{3} W_{i} x_{i}+b\right)$, donde
$f: \mathbb{R} \mapsto \mathbb{R}$ es la llamada **función de activación**. Entre las función de activación
más comunes se encuentran: sigmoide, tanh, RELU, LeakyRELU y Swish [@nwankpaActivationFunctionsComparison2018].

Una red neuronal se construye juntando varias neuronas, de forma que las salidas de unas neuronas son las
entradas de otra, como se muestra en la figura \ref{fig:neuron}). En la figura, los círculos representan una neurona, y aquellos
con etiqueta +1 son las **unidades de *bias* **. Por otro lado, las unidades o neuronas se agrupan en capas, una
capa está representada como una columna de círculos. Dentro de estas capas, podemos diferenciar tres tipos:
la capa de entrada (más a la izquierda), la capa interna, y la capa de salida que solamente contiene una neurona (a la derecha).

Vamos a denotar, $n_l$ como el numero de capas de nuestra red, $n_l=3$ en nuestro ejemplo.
A la capa de entrada la denotamos como $L_1$, y la capa de salida por tanto sería $L_{n_l}$.
Nuestra red neuronal tiene como parámetros $(W, b)= \left(W^{(1)}, b^{(1)}, W^{(2)}, b^{(2)}\right)$,
donde cada elemento $W_{i j}^{(l)}$ corresponde con el parámetro asociado a la conexión entre la neurona
$j$ de la capa $l$ y la neurona $i$ de la capa $l + 1$. Por otro lado, $b_{i}^{(l)}$ es el *bias* asociado
a la unidad $i$ de la capa $l + 1$.

Podemos denotar a la activación (valor de salida) de una neurona $i$ de la capa $l$ como $a_{i}^{(l)}$. En el
caso de la capa de entrada ($l = 1$), es obvio que $a_{i}^{(1)}=x_{i}$, es decir, la activación de la capa
de entrada es el mismo vector de entrada. Gracias a la notación vectorial, podemos definir el vector de activaciones de una capa como:

$$
\begin{aligned}
z^{(l+1)} &=W^{(l)} a^{(l)}+b^{(l)} \\
a^{(l+1)} &=f\left(z^{(l+1)}\right)
\end{aligned}
$$

Finalmente, la función hipótesis, o salida de la red, se puede definir como:

$$h_{W, b}(x)=a^{(n_l)}=f\left(z^{(n_l)}\right)$$

Teniendo en cuenta esta nomenclatura, la función de salida de la red mostrada en la figura \ref{fig:neuron}, corresponde
con la siguiente ecuación:

$$
\begin{aligned}
z^{(2)} &=W^{(1)} x+b^{(1)} \\
a^{(2)} &=f\left(z^{(2)}\right) \\
z^{(3)} &=W^{(2)} a^{(2)}+b^{(2)} \\
h_{W, b}(x) &=a^{(3)}=f\left(z^{(3)}\right)
\end{aligned}
$$

Donde $x$ es el vector de entrada, es decir, un ejemplo en el conjunto de entrenamiento.

Una de las ventajas principales de usar la notación vectorial es que a la hora de implementarlo,
podemos aprovechar bibliotecas y rutinas de algebra lineal con implementaciones eficientes como
BLAS [@lawson1979basic] o LAPACK [@demmelLAPACKPortableLinear1989].


### Algoritmo de propagación hacia atrás

Suponiendo que tenemos un conjunto de datos
$\left\{\left(x^{(1)}, y^{(1)}\right), \ldots,\left(x^{(m)}, y^{(m)}\right)\right\}$ con $m$ ejemplos.
Podemos entrenar una red neuronal usando gradiente descendiente. La función de coste a optimizar para un
ejemplo es la siguiente:

$$J(W, b ; x, y)=\frac{1}{2}\left\|h_{W, b}(x)-y\right\|^{2}$$

Dado un conjunto de entrenamiento de $m$ ejemplos, el coste total se define como:

$$
\begin{aligned}
J(W, b) &=\left[\frac{1}{m} \sum_{i=1}^{m} J\left(W, b ; x^{(i)}, y^{(i)}\right)\right]+\frac{\lambda}{2} \sum_{l=1}^{n_{l}-1} \sum_{i=1}^{s_{l}} \sum_{j=1}^{s_{l+1}}\left(W_{j i}^{(l)}\right)^{2} \\
&=\left[\frac{1}{m} \sum_{i=1}^{m}\left(\frac{1}{2}\left\|h_{W, b}\left(x^{(i)}\right)-y^{(i)}\right\|^{2}\right)\right]+\frac{\lambda}{2} \sum_{l=1}^{n_{l}-1} \sum_{i=1}^{s_{l}} \sum_{j=1}^{s_{l+1}}\left(W_{j i}^{(l)}\right)^{2}
\end{aligned}
$$

El primer termino de $J(W, b)$ es la media de los cuadrados de los residuos (errores).
El segundo termino corresponde con la regularización. El término $\lambda$ controla la
importancia relativa de la regularización. Esta función de coste se utiliza tanto para
regresión como para clasificación. En el caso de la clasificación, $y$ toma los valores
0 o 1 según la clase que corresponda. Si usamos $tanh$ como función de activación en la
salida en lugar de la sigmoide, usaríamos los valores -1 y 1 en su lugar.

El objetivo es minimizar $J(W, b)$ como función de $W$ y $b$. Para llevar a cabo esta optimización,
debemos inicializar $W$ y $b$ con valores aleatorios próximos a cero, por ejemplo, con valores muestreados
de $\mathcal{N}\left(0, \epsilon^{2}\right)$. El motivo por el que es importante inicializar aleatoriamente los
pesos, es para **romper la simetría**. Posteriormente, aplicamos un algoritmo de optimización, como
puede ser *gradiente descendiente*. Una iteración de gradiente descendiente actualizaría los pesos de
la siguiente forma:

$$
\begin{aligned}
W_{i j}^{(l)} &:=W_{i j}^{(l)}-\alpha \frac{\partial}{\partial W_{i j}^{(l)}} J(W, b) \\
b_{i}^{(l)} &:=b_{i}^{(l)}-\alpha \frac{\partial}{\partial b_{i}^{(l)}} J(W, b)
\end{aligned}
$$

El parámetro $\alpha$ corresponde al ratio de aprendizaje.
El algoritmo de propagación hacia atrás [@hecht-nielsenIIITheoryBackpropagation1992] nos ofrece una forma
eficiente de calcular las derivadas parciales necesarias para actualizar los pesos mediante
gradiente descendiente. Para calcular las derivadas parciales, es necesario formular dichas derivadas. 

$$
\begin{aligned}
\frac{\partial}{\partial W_{i j}^{(l)}} J(W, b) &=\left[\frac{1}{m} \sum_{i=1}^{m} \frac{\partial}{\partial W_{i j}^{(l)}} J\left(W, b ; x^{(i)}, y^{(i)}\right)\right]+\lambda W_{i j}^{(l)} \\
\frac{\partial}{\partial b_{i}^{(l)}} J(W, b) &=\frac{1}{m} \sum_{i=1}^{m} \frac{\partial}{\partial b_{i}^{(l)}} J\left(W, b ; x^{(i)}, y^{(i)}\right)
\end{aligned}
$$

El motivo por el que ambas ecuaciones difieren, es que la regularización no se aplica al *bias*.
El algoritmo que nos permite calcular dichas derivadas de manera eficiente es el siguiente:

1. Una pasada hacia adelante computando los valores de todas las neuronas a partir de la segunda capa.
2. Para cada neurona $i$ de la capa $n_l$ de salida, calculamos:
$$\delta_{i}^{\left(n_{l}\right)}=\frac{\partial}{\partial z_{i}^{\left(n_{l}\right)}} \frac{1}{2}\left\|y-h_{W, b}(x)\right\|^{2}=-\left(y_{i}-a_{i}^{\left(n_{l}\right)}\right) \cdot f^{\prime}\left(z_{i}^{\left(n_{l}\right)}\right)$$
3. Para cada capa $l=n_{l}-1, n_{l}-2, n_{l}-3, \dots, 2$ y para cada neurona $i$ en $l$, calcular:
    $$\delta_{i}^{(l)}=\left(\sum_{j=1}^{s_{l+1}} W_{j i}^{(l)} \delta_{j}^{(l+1)}\right) f^{\prime}\left(z_{i}^{(l)}\right)$$
4. Finalmente, las derivadas parciales vienen dadas por:
    $$
    \begin{aligned}
    \frac{\partial}{\partial W_{i j}^{(l)}} J(W, b ; x, y) &=a_{j}^{(l)} \delta_{i}^{(l+1)} \\
    \frac{\partial}{\partial b_{i}^{(l)}} J(W, b ; x, y) &=\delta_{i}^{(l+1)}
    \end{aligned}
    $$

### Autoencoders

Autoencoders [@baldi2012autoencoders] son redes neuronales entrenadas para reconstruir la entrada,
es decir, para copiar la entrada en la salida. Internamente, estas arquitecturas
contienen un capa interna llamada **código**. Este código es una representación
de los datos de entrada en un espacio vectorial de dimensión igual o distinta a los mismo.
La red puede plantearse como la suma de dos partes bien diferenciadas: un codificador (encoder),
que representa una función $h=f(x)$, y un decodificador (decoder) que produce una reconstrucción
de la salida $r = g(h)$. Esta arquitectura se puede ver fácilmente en la figura \ref{fig:autoencoder}.

![Arquitectura básica de un autoencoder de una sola capa para el codificador y el decodificador. Fuente: [@sublimeAutomaticPostDisasterDamage2019]](source/figures/autoencoder.pbm){#fig:autoencoder}

Si diseñamos un autoencoder que únicamente se encargue de copiar la entrada en la salida, es decir,
si simplemente es capaz de mapear $g(f(x)) = x$ para todos los valores de $x$, no es especialmente
útil. Sin embargo, podemos diseñar autoencoders que no se limiten a copiar la información de entrada,
sino que aprendan patrones de los datos y los utilicen para la reconstrucción. Este es el objetivo
de los autoencoders. Cuando restringimos de alguna forma una arquitectura de este tipo, el error
de reconstrucción $e = L(g(f(x)), x)$, donde $L$ puede ser cualquier métrica de distancia, va
a ser mayor que 0 en mayoría de casos (y positivo siempre). Debido a que solamente podemos reconstruir los datos de entrada
de manera aproximada. Dichas restricciones, fuerzan al el modelo a priorizar partes de información
que deben ser copiadas, encontrando así patrones útiles en los datos.

Tradicionalmente, este tipo de arquitecturas se han utilizado para reducción de dimensionalidad o aprendizaje
de características [@wangAutoencoderBasedDimensionality2016]. La reducción de la dimensionalidad es posible debido que
la capa interna (*código*) contienen información relevante que permite reconstruir los datos originales a
partir de ella. Por ese motivo, si utilizamos una capa de código con un número de neuronas menor que la dimensión de los
datos de entrada, podemos conseguir una representación aproximada de dichos datos
en un espacio de dimension inferior. Para el aprendizaje de características, un uso interesante que se le ha
dado a esta arquitectura es el de preentrenar arquitecturas o partes de ellas a partir de datos sin etiquetas
[@bengioDeepLearning2017]. Esto se consigue entrenando un autoencoder, y transfiriendo los pesos de dicha arquitectura,
normalmente de  la parte del codificador, hay otra arquitectura diseñada para un problema supervisado. De esta forma,
si disponemos de datos no etiquetados, podemos aprovecharlos también para un problema supervisado.


#### Autoencoders según la dimensión del código

Según el tamaño del código existen dos categorías de autoencoders.
Cuando el código tiene un tamaño menor que la dimensión del vector de entrada (columnas del conjunto de entrenamiento), se le conocen como autoencoders
***undercomplete***. Si por el contrario, el código tiene una dimensión mayor, esos autoencoders reciben el nombre de ***overcomplete***.

Una de las formas más importantes para hacer que el encoder extraiga características relevantes de los datos,
en lugar de meramente copiarlos, es restringir $h$ para que tenga una dimensión menor que $x$. Es decir,
tener un autoencoder *undercomplete*. De esta forma, el encoder es forzado a aprender las características más
importantes que van a permitir restaurar la mayoría de información.

El proceso de aprendizaje de los autoencoders se puede resumir en la optimización de la siguiente función de coste:

$$L(\boldsymbol{x}, g(f(\boldsymbol{x})))$$

Para todos los ejemplos $x$ del conjunto de entrenamiento. $L$ corresponde, como se ha mencionado anteriormente,
a la métrica de similaridad. La métrica más común es el error cuadrático medio. Un aspecto interesante de esta métrica,
es que cuando se usa con un autoencoder *undercomplete* cuyo decoder sea lineal
(aquel cuya función de activación para todas sus neuronas sea $f(x) = x$), este aprende a generar un subespacio
equivalente al de [!pca].

Por otro lado, los autoencoders *overcomplete* no suelen ser muy útiles en la práctica. Debido principalmente a
que si el código es mayor o igual que el tamaño de los datos de entrada, no hay nada que impida al autoencoder
aprender a copiar la información, ya que si $x \in \mathbb{R}^N$, cualquier espacio vectorial $\mathbb{R}^{N'}$ donde
$N'$ sea mayor que $N$ puede generar todos los datos de entrada. Para poder utilizar este tipo de autoencoders
es necesario el uso de **regularización**.

#### Autoencoders regularizados

Como se ha descrito anteriormente, los autoencoders *undercomplete*, cuya dimensión del código es menor que la de la entrada, pueden
aprender las características o patrones mas relevantes de la distribución de los datos. El problema principal de este
tipo de arquitecturas, tanto *undercomplete* como *overcomplete*, es que el autoencoder sea demasiado potente como
para no tener aprender nada útil y simplemente se encarguen de copiar la información. Este problema se hace obvio
cuando en el caso de los autoencoders *overcomplete*, (incluso en aquellos con una dimensión del código igual que la
entrada). En esos casos, hasta un autoencoder lineal puede aprender a copiar la entrada en la salida [@bengioRegularizedAutoencoders2017].

El objetivo de la regularización es permitir entrenar cualquier arquitectura de
autoencoder de manera que esta aprenda correctamente, donde el tamaño del código
y la profundidad de la red no esté limitada por el aprendizaje, sino por la complejidad
de la distribución de datos. En lugar de restringir la arquitectura, los autoencoders
regularizados utilizan una función de coste que penaliza la copia de datos, o al menos, favorece
características intrínsecas del modelo. Entre estas características se encuentra, la dispersión,
robustez frente a ruido, etc. Al hacer uso de ese tipo de funciones de coste con regularización,
incluso autoencoders no lineales y *overcomplete* pueden aprender patrones útiles sobre los datos.
Incluso si la capacidad del modelo es suficiente como para aprender la función identidad.


##### Autoencoders dispersos

Un autoencoder disperso [@bengioDeepLearning2017; @ng2011sparse] es simplemente un autoencoder cuya función de
coste contiene una penalización por dispersión. La nueva función de coste es la siguiente:

$$L(\boldsymbol{x}, g(f(\boldsymbol{x})))+\Omega(\boldsymbol{h})$$

Donde $\Omega(\boldsymbol{h})$ es la penalización por dispersión. El objetivo es el de maximizar la
dispersión del vector de activaciones en la *capa oculta o interna* (código). Para ello, la penalización
que se propone es la siguiente:

$$\Omega(\boldsymbol{h}) = \beta \sum_{j=1}^{s_{2}} \mathrm{KL}\left(\rho \| \hat{\rho}_{j}\right)$$

Donde $\beta$ es el parámetro que controla el peso de la penalización, $\rho$ es el **parámetro de dispersión**
y $\hat{\rho}_{j}$ es la activación media de la neurona $j$ de la capa interna, cuya
expresión viene dada por:

$$\hat{\rho}_{j}=\frac{1}{m} \sum_{i=1}^{m}\left[a_{j}^{(2)}\left(x^{(i)}\right)\right]$$

Básicamente, se calcula la salida o activación de una misma neurona para todos
los ejemplos de entrenamiento, y se hace la media. Por otro lado, la función Kullback-Leibler
$\mathrm{KL}\left(\rho \| \hat{\rho}_{j}\right)=\rho \log \frac{\rho}{\hat{\rho}_{j}}+(1-\rho) \log \frac{1-\rho}{1-\hat{\rho}_{j}}$
mide la divergencia entre una variable aleatoria de Bernoulli con media $p$ y una variable aleatoria de Bernoulli
con media $\hat{\rho}_{j}$. Esta función es un estándar a la hora de medir la similitud de dos distribuciones.

Los autoencoders dispersos se suelen usar para aprender características útiles para otra tarea,
como puede ser clasificación. Un autoencoder disperso debe encontrar patrones inherentes a la
distribución de datos, en lugar de actuar como una simple función identidad.


#### Denoising Autoencoders

Para este tipo de autoencoders, en lugar de añadir una penalización a la función de coste,
se modifican los datos de entrada. Siguiendo la formulación del problema de apartados anteriores,
tenemos la siguiente función a optimizar:

$$L(\boldsymbol{x}, g(f(\tilde{\boldsymbol{x}})))$$

Donde $\tilde{\boldsymbol{x}}$ es una copia de los datos de entrada a la que se le ha añadido ruido
o algún otro tipo de corrupción. De esta forma, no basta con aprender la función identidad, es necesario
además aprender patrones interesantes que permitan eliminar el ruido. Una forma sencilla de implementar
este arquitecturas, es añadiendo una capa de **Dropout** como capa de entrada.

#### Autoencoders variacionales

Los autoencoders variacionales [@kingmaIntroductionVariationalAutoencoders2019] tienen dos enfoques, el enfoque de
*Deep Learning* o el enfoque probabilístico. En nuestro caso, este tipo de arquitecturas se describen desde
el enfoque del *Deep Learning*.

El principal uso de este tipo de arquitecturas es como *modelos generacionales*. Se utilizan para producir
nuevos datos (especialmente imágenes) a partir de unos datos de entrenamiento. Desde el punto de vista de
los modelos generativos, un autoencoder regular es ineficiente para este tipo de problemas. El motivo es
que el espacio de representación intermedias (código), también conocido como **espacio latente**, tiene
discontinuidades. Una forma de generar un nuevo ejemplo es aplicar el codificador y obtener la representación
en el espacio latente. Posteriormente, ese vector se modifica ligeramente en una dirección deseada y se aplica
el decodificador sobre el nuevo vector, generando así un nuevo ejemplo similar al anterior. El nuevo dato resultante
es una combinación de aquellos ejemplos cercanos al nuevo vector. Si el espacio latente tiene discontinuidades,
y el vector a reconstruir resulta estar en alguna de esas discontinuidades, el resultado va a ser muy poco realista.
El objetivo de los autoencoders variacionales (*VAE*) es el de generar un espacio latente continuo para suavizar 
las interpolaciones.

Para entrenar este tipo de autoencoders necesitamos modificar la función de coste original. La nueva
función de coste es la siguiente:

$$l_{i}(\theta, \phi)=-\mathbb{E}_{z \sim q_{\theta}\left(z | x_{i}\right)}\left[\log p_{\phi}\left(x_{i} | z\right)\right]+\mathbb{K} \mathbb{L}\left(q_{\theta}\left(z | x_{i}\right) \| p(z)\right)$$


Donde los parámetros $\theta$ y $\phi$ representan la matriz de pesos y el vector de *bias*,
$q_{\theta}(z | x)$ denota el codificador, $p_{\phi}(x | z)$ denota el decodificador, y $p_{\phi}(x | z)$
representa el error de reconstrucción.

#### Truco de la reparametrización

El termino de la esperanza en la función de coste implica la generación de ejemplos de la distribución
$\mathbf{z} \sim q_{\phi}(\mathbf{z} | \mathbf{x})$.
Muestrear es un proceso estocástico, por tanto, no podemos aplicar la propagación hacia atrás.
Para poder optimizar dicha función de coste, se aplica el truco de la reparametrización (**reparameterization trick**)
[@kingmaAutoEncodingVariationalBayes2014].

Una variable aleatorio $\mathbf{z}$ se puede expresar como una variable determinística 
$\mathbf{z}=\mathcal{T}_{\phi}(\mathbf{x}, \boldsymbol{\epsilon})$, donde $\epsilon$ es una variable aleatoria 
independiente, y la función de transformación $\mathcal{T}_{\phi}$ parametrizada por
$\phi$ convierte $\epsilon$ a $\mathbf{z}$.

![Ilustración de como el truco de la reparametrización hace el proceso de muestreo de $\mathbf{z}$ entrenable.
Fuente: Dispositiva 12 en el workshop de Kingma para NIPS 2015](source/figures/reparameterization-trick.png)

Como ejemplo, una forma común para esto $q_{\phi}(\mathbf{z} | \mathbf{x})$ es una Gaussiana multivariable con
estructura de covarianza diagonal.

$$
\begin{array}{l}
\mathbf{z} \sim q_{\phi}\left(\mathbf{z} | \mathbf{x}^{(i)}\right)=\mathcal{N}\left(\mathbf{z} ; \boldsymbol{\mu}^{(i)}, \boldsymbol{\sigma}^{2(i)} \boldsymbol{I}\right) \\
\mathbf{z}=\boldsymbol{\mu}+\boldsymbol{\sigma} \odot \boldsymbol{\epsilon}, \text { where } \boldsymbol{\epsilon} \sim \mathcal{N}(0, \boldsymbol{I})
\end{array}
$$

Donde $\odot$ corresponde al producto elemento a elemento.

El truco de la reparametrización funciona también para otro tipo de distribuciones, no solo la Gaussiana.
En el caso de la Gaussiana multivariable, se hace posible entrenar el modelo aprendiendo la media y la varianza
de la distribución. $\mu$ y $\sigma$, usando explícitamente este truco, mientras que la estocasticidad permanece
en la variable aleatoria $\boldsymbol{\epsilon} \sim \mathcal{N}(0, \boldsymbol{I})$.

### Autoencoders apilados

Aunque en las secciones anteriores tanto el codificador como el decodificador se han tratado como dos capas
dentro de una red de 3 capas. La realidad es que en muchos casos se necesita más capas tanto a un lado como
a otro. Aquellos autoencoders donde o bien el codificador o bien el decodificador tienen más de una capa,
se les conoce con el nombre de Autoencoders apilados (**Stacked Autoencoders**) [@bengioDeepLearning2017] .
Al igual que para el resto de arquitecturas de *Deep Learning*, añadir más capas permite reducir la linealidad y aprender
patrones más complejos.

El principal factor a tener en cuenta en estos casos, es que los autoencoders son muy potentes de por sí,
en relación con la función que tienen que modelar (identidad). Es por esto, por lo que la regularización
se vuelve esencial a la hora de apilar diferentes capas a un lado u a otro.

En cuanto a diseño, la forma más común de diseñarlos es de manera simétrica - el mismo número de capas
y unidades para el encoder y el decoder. Además, las capas suelen tener un número de neuronas decrecientes
para el encoder y crecientes para el decoder. Esto permite aplicar un técnica conocida como **Tied Weights** .
Esta técnica consiste en compartir los pesos entre el codificar y el decodificador, haciendo que los
pesos de este último corresponda con la transpuesta del primero:

$$\theta_{d} = \theta_{e}^T$$

Esta técnica mejora el rendimiento en el entrenamiento, ya que se entrenan menos parámetros, pero además,
sirve como método de regularización [@vincentConnectionScoreMatching2011].

### Aplicaciones de los autoencoders

Las aplicaciones principales de los autoencoders han sido la **reducción de la dimensionalidad** y
**recuperación de información**. Autoencoders no lineales pueden ofrecer un error de reconstrucción
menor que [!pca], y al no estar limitados a una proyección lineal, pueden aprender una representación
más fácil de interpretar. En el caso de clasificación, los autoencoders pueden encontrar una
representación donde los datos estén agrupados en clusters y las categorías estén bien diferenciadas.
Además, encontrar una proyección a un espacio de dimensión inferior que mantenga la mayoría de
la información, permite mejorar el rendimiento de modelos, ya que estos en espacios inferiores tiene un menor
coste de cómputo y memoria.

Otra aplicación que se ha ido desarrollando en los últimos años es la de **detección de anomalías**.
Los autoencoders pueden utilizarse para modelar la distribución de datos, y el error de reconstrucción
se puede utilizar como indicador para detectar anomalías. Cuando un autoencoder se ha entrenado correctamente,
el error de reconstrucción sobre datos de de entrenamiento es bajo. Así como el error otros datos de la misma
distribución que no hayan usado para entrenar (conjunto de validación y test por ejemplo). Pero en el caso
de utilizar datos de una distribución distinta, al no poder extraer las características más importantes
eficazmente, el error de reconstrucción es mayor. Por este motivo, se puede entrenar un autoencoder
sobre los datos "no anómalos", y establecer un umbral sobre el error de reconstrucción que indique si
el ejemplo que se ha pasado por la red es una anomalía.

Por otro lado, cabe destacar el uso de los autoencoders variacionales como modelos generativos,
aunque se ven opacados en su mayoría por GAN y similares.

Una última aplicación que cabe destacar es la de **clasificación**. Los autoencoders, pese a modelos
de aprendizaje no supervisado, pueden usarse para problemas de clasificación [@juDeepLearningMethod2015].
Si se entrena un autoencoder para cada clase (con ejemplos exclusivos de esa clase),
el error de reconstrucción de cada autoencoder se puede  puede utilizar para decidir la clase.
Presuntamente, aquellos ejemplos cercanos a una determinada clase, tendrán un error de reconstrucción menor en su autoencoder correspondiente.
De esta forma, podemos aplicar este tipo de arquitecturas a problemas de clasificación. No obstante, los autoencoders se
entrenan de manera independiente minimizando el error de reconstrucción y la regularización (si aplica),
esto implica que no hay una optimización directa del error de clasificación. Al perder esa relación directa con la
métrica objetiva, este aplicación puede dar lugar a resultados subóptimos.
