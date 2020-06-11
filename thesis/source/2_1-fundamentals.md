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


### Tipos de reproducibilidad

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
del estudio. En este diseño se especifica la hipótesis base, las asunciones del problema, los test estadísticos a realizar,
y los p-valores correspondientes. El establecer las bases estadísticas sobre las que se va a desarrollar el estudio de antemano,
nos puede ayudar además a evitar problemas como el p-hacking.

Por otro lado, el término reproducibiidad además de poder descomponerse según la información o parte del trabajo que se
esté tratanto, llamémosla la escala o eje horizontal, también se puede descomponer en otro eje, llamemósle vertical,
que indica como de replicable y reproducible es un estudio en su conjunto. Los niveles de esta nueva escala son los
siguientes:


- **Investigación revisable**. Las descripciones de los métodos de investigación pueden ser
evaluados de manera independiente y los resultados juzgados. Esto incluye tanto los tradicionales
peer-review, community-review, y no implica necesariamente reproducibilidad.

- **Investigación replicable**. Se ponen a disposición del publico las herramientas que
necesarias para replicar los resultados, por ejemplo se ofrece el el código de los autores para producir
las gráficas que se muestran en la publicación. En este caso, las herramientas pueden tener un alcance limitado,
ofreciendo los datos ya procesados y esenciales, así como ofreciéndolas mediante petición exclusivamente.

- **Investigación confirmable**. Las conclusiones del estudio se pueden obtener sin el uso del software proporcionado por el autor.
Pero se debe ofrecer una completa descripción de los algoritmos y la metodología usados en la publicación y cualquier
material complementario necesario.

- **Investigación auditable**. Cuando se registra la suficiente informacion sobre el estudio
(incluidos datos y programas informáticos) para que la investigación pueda ser defendida posteriormente si es necesario 
o para llevar a cabo una resolución en caso de existir diferencias entre confirmaciones independientes.
Esta información puede ser privada, como con los tradicionales cuadernos de laboratorio.

- **Investigación abierta o reproducible**. Investigación auditable disponible abiertamente. El código y los datos se
encuentran lo suficientemente bien documentados y accesibles al publico para que la parte computacional
se pueda auditar, y lo resultados del estudio se puedan replicar y reproducir de manera independiente.
También debe permitir extender los resultados o aplicar el método desarrollado a nuevos problemas.


### Aspectos críticos

Una vez hemos definido los diferentes niveles de reproducibilidad, vamos a definir los aspectos que consideramos
críticos para lograr una investigacióin *abierta o reproducible*.

- **Conjunto de datos**: La información sobre la localización y el proceso de extracción de los datos. Este factor
es determinante a la hora de hacer un estudio reproducible. El objetivo es el de facilitar los datos y/o
la forma de extraerlos. En caso de que los datos no sean accesibles públicamente, o que los datos que se ofrezcan
no sean los extraidos en crudo, estaríamos ante un *estudio replicable*, pero no reproducible.

- **Preprocesado de datos**: En este aspecto se recogen los diferentes pasos del proceso de transformación de los datos.
Un investigador independiente debería ser capaz de repetir los datos de preprocesado fácilmente.
Sería también interesante incluir datos ya preprocesados con los que comparar y validar que las transformaciones
se han realizado correctamente. Estos procedimientos no son sencillos de documentar ni de compartir.
En algunas ocasiones, las transformaciones se realizan en software privativos o utilizando una interfaz gráfica.
En esos casos, en lugar de ofrecer los scripts de preprocesado, sería más interesante dar una descripción detallada
de como los datos se han transformado. Además, sugerimos favorecer las herramientas de código libre en caso de que
existan como alternativa a algunas de las herramientas privadas.

- **Particion de los datos**: En caso de que los datos se separen, por ejemplo para ajustar un modelo y validarlo,
es necesario proporcionar los detalles de como se ha realizado esta separación. En el caso de que dicha separación
sea aleatoria, como mínimo se debe proporcionar la semilla y el tipo de muestreo (estratificado o no, por ejemplo).
Aunque preferiblemente, todo este procedimiento debe estar recogido en un script.

- **Ajuste del modelo**: Corresponde a toda la información relativa al ajuste de un modelo. En este caso, es necesario
hacer disponible toda la información posible en relación a este proceso y a las decisiones tomadas. La información
mínima que se debe proporcionar es:

    1. Parametros del experimento
    2. Métodos propuestos: detalles de implementación, algoritmos, código, etc (si es aplicable).

- **Evaluación del modelo**: Información sobre como se evalua un modelo entrenado. Información similar al punto anterior
se aplica aquí.

- **Control de la estocasticidad**: La mayoría de operaciones en Machine Learning tienen un factor de aleatoriedad.
Por tanto, es esencial establecer los valores de las semillar que controlar dichos procesos.
La mayoría de herramientas de cálculo científico ofrecen algun método para establecer la semilla del
generador de números aleatorios.

- **Entorno software**: Debido al hecho de que los paquetes/módulos de software están en continuo
desarrollo y sufren posibles alteraciones de los algoritmos internos, es importante
que los detalles del entorno de software utilizado: módulos, paquetes y números de versión..., estén disponible.

- **Entorno hardware**: Algunos estudios, sobre todo los que continen grandes cantidades de datos, son
reproducibles exclusivamente cuando se ejecutan en una cierta máquina, o al menos, cuando se cumplen unos
requisitos de hardware determinados. Otro problema que surge en algunos casos y que está extrechamente relacionado
con el punto anterior, es el de las versiones de los drivers. Por este motivo, se requiere una correcta documentación
de los recursos utilizados, tanto GPU como CPU, así como de las versiones de sus drivers correspondientes.


## MLOps 



## Autoencoders

### Redes neuronales

Las redes neuronales son algoritmos de aprendizaje automático que han adquirido una gran
popularidad en los últimos años, y que han sido desarrollados y utilizados en una gran variedad
de problemas, desde aprendizaje supervisado, hasta no supervisado, pasando por aprendizaje por refuerzo
y reducción de la dimensionalidad.



Consider a supervised learning problem where we have access to labeled training examples (x
(i), y(i)). Neural networks give a way of defining a complex,
non-linear form of hypotheses hW,b(x), with parameters W, b that we can fit
to our data.
To describe neural networks, we will begin by describing the simplest
possible neural network, one which comprises a single “neuron.” We will use
the following diagram to denote a single neuron:


Autoencoders son redes neuronales entrenadas para reconstruir la entrada,
es decir, para copiar la entrada en la salida. Internamente, estas arquitecturas
contienen un capa interna llamada **código**. Este código es una representación
de los datos de entrada en un espacio vectorial de dimensión igual o distinta a los mismo.
La red puede plantearse como la suma de dos partes bien diferenciadas: un codificador (encoder),
que representa una funcion $h=f(x)$, y un decodificador (decoder) que produce una reconstrucción
de la salida $r = g(h)$. Esta arquitectura se puede ver facilmente en la figura INSERTAR FIGURA.

Si diseñamos un autoencoder que únicamente se encargue de copiar la entrada en la salida, es decir,
si simplemente es capaz de mapear $g(f(x)) = x$ para todos los valores de $x$, no es especialmente
util. Sin embargo, podemos diseñar autoencoders que no se limiten a copiar la información de entrada,
sino que aprendan patrones de los datos y los utilicen para la reconstrucción. Este es el objetivo
de los autoencoders. Cuando restringimos de alguna forma una arquitectura de este tipo, el error
de reconstrucción $e = error(g(f(x)), x)$, donde $error$ puede ser cualquier métrica de distancia, va
a ser mayor que 0 en la mayoría de casos. Debido a que solamente podemos reconstruir los datos de entrada
de manera aproximada. Debido a dichas restricciones, el modelo es forzado a priorizar partes de información
que deben ser copiadas y encontrando así patrones últiles en los datos.

Tradicionalmente, este tipo de arquitecturas se han utilizado para reducción de dimensionalidad o aprendizaje
de características. La reducción de la dimensionalidad es posible debido que la capa interna (*código*)
contienen información relevante que permite reconstruir los datos originales a partir de ella.
Por ese motivo, si utilizamos una capa de código con un número de neuronas menor que la dimensión de los
datos de entrada, podemos conseguir una representación aproximada de dichos datos
en un espacio de dimension inferior. Para el aprendizaje de características, un uso interesante que se le ha
dado a esta arquitectura es el de preentrenar arquitecturas o partes de ellas a partir de datos sin etiquetas.
Esto se consigue entrenando un autoencoder, y transfiriendo los pesos de dicha arquitectura, normalmente de 
la parte del codificador, hay otra arquitectura diseñada para un problema supervisado. De esta forma,
si disponemos de datos no etiquetados, podemos aprovecharlos también para un problema supervisado.


### Autoencoders según la dimensión del código

### Autoencoders regularizados

### Autoencoders variacionales

### Autoencoders apilados
