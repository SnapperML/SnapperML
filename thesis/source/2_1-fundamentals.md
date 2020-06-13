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



## Redes neuronales

Las redes neuronales son algoritmos de aprendizaje automático que han adquirido una gran
popularidad en los últimos años, y que han sido desarrollados y utilizados en una gran variedad
de problemas, desde aprendizaje supervisado, hasta no supervisado, pasando por aprendizaje por refuerzo
y reducción de la dimensionalidad.

Para describir una red neuronal vamos a empezar por la arquitectura más básica, una sola neurona.
Una forma de representar dicha neurona en una diagrama es la siguiente:

![](https://cdn.mathpix.com/snip/images/i9Ls1o_dULHhOoNqiKOukfVpPWEokabL2a5FvYo21nA.original.fullsize.png)

Una neurona no es más que una unidad computacional que toma como entrada un vector $x$ (más un elemento a 1 para el sesgo),
y cuya salida es $h_{W, b}(x)=f\left(W^{T} x\right)=f\left(\sum_{i=1}^{3} W_{i} x_{i}+b\right)$, donde
$f: \mathbb{R} \mapsto \mathbb{R}$ es la llamada **función de activación**. Entre las función de activación
más comunes se encuentran: sigmoide, tanh, RELU, LeakyRELU y Swish.

Una red neuronal se construye juntando varias neuronas, de forma que las salidas de unas neuronas son las
entradas de otra, como se muestra en la figura X. En la figura, los circulos representan una neurona, y aquellos
con etiqueta +1 son las **unidades de sesgo**. Por otro lado, las unidades o neuronas se agrupan en capas, una
capa está representada como una columna de círculos. Dentro de estas capas, podemos diferenciar tres tipos:
la capa de entrada (más a la izquierda), la capa interna, y la capa de salida que solamente contiene una neurona (a la derecha).

Vamos a denotar, $n_l$ como el numero de capas de nuestra red, $n_l=3$ en nuestro ejemplo.
A la capa de entrada la denotamos como $L_1$, y la capa de salida por tanto sería $L_{n_l}$.
Nuestra red neuronal tiene como parametros $(W, b)= \left(W^{(1)}, b^{(1)}, W^{(2)}, b^{(2)}\right)$,
donde cada elemento $W_{i j}^{(l)}$ corresponde con el parametro asociado a la conexión entre la neurona
$j$ de la capa $l$ y la neurona $i$ de la capa $l + 1$. Por otro lado, $b_{i}^{(l)}$ es el sesgo asociado
a la unidad $i$ de la capa $l + 1$.

Podemos denotar a la activación (valor de salida) de una neurona $i$ de la capa $l$ como $a_{i}^{(l)}$. En el
caso de la capa de entrada ($l = 1$), es obvio que $a_{i}^{(1)}=x_{i}$. Gracias a la notación vectorial,
podemos definir el vector de activaciones de una capa como:

$$
\begin{aligned}
z^{(l+1)} &=W^{(l)} a^{(l)}+b^{(l)} \\
a^{(l+1)} &=f\left(z^{(l+1)}\right)
\end{aligned}
$$

Finalmente, la función hipótesis, o salida de la red, se puede definir como:

$$h_{W, b}(x)=a^{(n_l)}=f\left(z^{(n_l)}\right)$$

Teniendo en cuenta esta nomenclatura, la función de salida de la red mostrada en la figura X, corresponde
con la siguiente ecuación:

$$
\begin{aligned}
z^{(2)} &=W^{(1)} x+b^{(1)} \\
a^{(2)} &=f\left(z^{(2)}\right) \\
z^{(3)} &=W^{(2)} a^{(2)}+b^{(2)} \\
h_{W, b}(x) &=a^{(3)}=f\left(z^{(3)}\right)
\end{aligned}
$$

Una de las ventajas principales de usar la notación vectorial es que a la hora de implementarlo,
podemos aprovechar bibliotecas y rutinas de algebra lineal con implementaciones eficientes como
BLAS o LAPACK.



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
debemos inicializar $W$ y $b$ con valores aleatorios próximos a cero, por ejemplo, con valores muestrados
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
El algoritmo de propagación hacia atrás nos ofrece una forma eficiente de calcular las derivadas
parciales necesarias para actualizar los pesos mediante gradiente descendiente. Para calcular
las derivadas parciales, es necesario formular dichas derivadas. 

$$
\begin{aligned}
\frac{\partial}{\partial W_{i j}^{(l)}} J(W, b) &=\left[\frac{1}{m} \sum_{i=1}^{m} \frac{\partial}{\partial W_{i j}^{(l)}} J\left(W, b ; x^{(i)}, y^{(i)}\right)\right]+\lambda W_{i j}^{(l)} \\
\frac{\partial}{\partial b_{i}^{(l)}} J(W, b) &=\frac{1}{m} \sum_{i=1}^{m} \frac{\partial}{\partial b_{i}^{(l)}} J\left(W, b ; x^{(i)}, y^{(i)}\right)
\end{aligned}
$$

El motivo por el que ambas ecuaciones difieren, es que la regularización no se aplica al sesgo.
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

## Autoencoders

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
de reconstrucción $e = L(g(f(x)), x)$, donde $L$ puede ser cualquier métrica de distancia, va
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

Según el tamaño del código existen dos categorías de autoencoders.
Cuando el código tiene un tamaño menor que los datos de entrada, ase le conocen como autoencoders
**undercomplete**. Si por el contrario, el código es mayor que los datos de entrada, esos autoencoders
reciben el nombre de **overcomplete**.

Una de las formas más importantes para hacer que el encoder extraiga características relevantes de los datos,
en lugar de meramente copiarlos, es restringir $h$ para que tenga una dimensión menor que $x$. Es decir,
tener un autoencoder *undercomplete*. De esta forma, el encoder es forzado a aprender las caracteristicas más
importantes que van a permitir restaurar la mayoría de información.

El proceso de aprendizaje de los autoencoders se puede resumir en la optimización de la siguiente función de coste:

$$L(\boldsymbol{x}, g(f(\boldsymbol{x})))$$

Para todos los ejemplos $x$ del conjunto de entrenamiento. $L$ corresponde, como se ha mencionado anteriormente,
a la métrica de similaridad. La métrica más común es el error cuadrático medio. Un aspecto interesante de esta métrica,
es que cuando se usa con un autoencoder *undercomplete* cuyo decoder sea lineal
(aquel cuya función de activación para todas sus neuronas sea $f(x) = x$), este aprende a generar un subespacio
equivalente al de PCA.

Por otro lado, los autoencoders *overcomplete* no suelen ser muy útiles en la práctica. Debido principalmente a
que si el código es mayor o igual que el tamaño de los datos de entrada, no hay nada que impida al autoencoder
aprender a copiar la información, ya que si $x \in \mathbb{R}^N$, cualquier espacio vectorial $\mathbb{R}^{N'}$ donde
$N'$ sea mayor que $N$ puede generar todos los datos de entrada. Para poder utilizar este tipo de autoencoders
es necesario el uso de **regularización**.

### Autoencoders regularizados

Como se ha descrito anteriorente, los autoencoders *undercomplete*, cuya dimensión del código es menor que la de la entrada, pueden
aprender las características o patrones mas relevantes de la distribución de los datos. El problema principal de este
tipo de arquitecturas, tanto *undercomplete* como *overcomplete*, es que el autoencoder sea demasiado potente como
para no tener aprender nada útil y simplemente se encarguen de copiar la información. Este problema se hace obvio
cuando en el caso de los autoencoders *overcomplete*, (incluso en aquellos con una dimensión del código igual que la
entrada). En esos casos, hasta un autoencoder lineal puede aprender a copiar la entrada en la salida.

El objetivo de la regularización es permitir entrenar cualquier arquitectura de
autoencoder de manera que esta aprenda correctamente, donde el tamaño del código
y la profundidad de la red no esté limitada por el aprendizaje, sino por la complejidad
de la distribución de datos. En lugar de restringir la arquitectura, los autoencoders
regularizados utilizan una función de coste que penaliza la copia de datos, o al menos, favorece
características intrínsicas del modelo. Entre estas características se encuentra, la dispersión,
robustez frente a ruido, etc. Al hacer uso de ese tipo de funciones de coste con regularización,
incluso autoencoders no lineales y *overcomplete* pueden aprender patrones útiles sobre los datos.
Incluso si la capacidad del modelo es suficiente como para aprender la función identidad.


### Autoencoders variacionales

### Autoencoders apilados

### Aplicaciones de los autoencoders
