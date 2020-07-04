# Experimentos

En este último capítulo de la tesis se recogen los experimentos llevados a cabo para la resolución
del problema (Objetivo 2). Primeramente, se describe detalladamente el problema: origen, tipo y estructura
de los datos, tipo de problema, asunciones y/o restricciones, etc. Posteriormente, se detallan los diferentes
algoritmos y arquitecturas de ML/DL empleados - se especifican los parámetros, biblioteca empleada,
detalles de implementación, y otra información relevante. Finalmente, se muestran los resultados obtenidos
para cada tipo de modelo, y algunos trabajos a posteriori que pueden ser interesantes.

## Definición del problema

### Historia

Los rayos cósmicos son partículas que bombardean la tierra a gran velocidad y que provienen del espacio exterior.
La partículas de rayos cósmicos son protones (90%) y núcleos pesados en su mayoría. Las partículas de rayos cósmicos
viajan a prácticamente la velocidad de la luz, lo que significa que tienen una gran energía. Algunas de ellas incluso
contienen más energía que cualquier otra partícula observada en la naturaleza.

Este fenómeno de la Física fue descubierto en 1912 por Hess y Kohlhorster [@stanevOverview2010], y algunas de sus propiedades
siguen siendo un misterio después de más de un siglo. Un ejemplo es el origen de los rayos, la mayoría de los científicos sospechan
que el origen de los rayos cósmicos está relacionado con las *supernovas*, aunque no descartan otro tipo de fuentes [@burrowsBaadeZwickySupernovae2015].
Además, no es del todo claro como las supernovas pueden generar estos rayos cósmicos tan rápido. 

Para aprender más sobre la naturaleza de este fenómeno, los científicos miden la energía y la dirección
de los rayos conforme llegan a la tierra. Los rayos cósmicos de baja energía se miden utilizando globos aerostáticos y satélites
situados por encima de la atmósfera terrestre, mientras que para los rayos cósmicos de alta energía,
es más eficiente medirlos indirectamente observado la cascada de partículas que produce.

![Cascada atmosférica extensa. (Observatorio Pierre Auger)](source/figures/comic_air_shower.jpg){#fig:shower}

Una *cascada atmosférica extensa* [@stanevHighEnergyCosmic2010] se produce cuando un rayo cósmico de alta energía
(y de alta velocidad) penetra en la atmósfera. Cuando una partícula colisiona violentamente con las moléculas de aire,
se fragmenta generando hadrones. Los fragmentos desprendidos a su vez colisionan con otras partículas del aire,
produciendo así una cascada donde la energía de la partícula original
se dispersa entre millones de partículas que caen hacia la tierra (ver figura \ref{fig:shower}).
Al estudiar las *cascadas atmosféricas*, los científicos pueden medir algunas propiedades de las partículas
originales que llegaron a la atmósfera, también llamadas *primarios*.

![Mapa del observatorio de Pierre Auger. Cada punto negro representa un detector [!wcd]](source/figures/observatory_map.pbm){#fig:observatory}

El Observatorio de Pierre Auger [@PierreAugerCosmic2015] se propuso para descubrir y entender la fuentes de los rayos
cósmicos de energía más altas. El observatorio, situado en la ciudad de Malargüe, en la provincia de Mendoza, Argentina,
es una colaboración única entre 18 países, cuya construcción empezó en 2002 y finalizó en 2008.
El observatorio es un detector híbrido, utiliza un detector de gran superficie (SD) y un detector
de fluorescencia (FD). El SD se compone de 1660 [!+wcd] situados estratégicamente formando una malla triangular.
En esta malla, los detectores están separados con una distancia de 1500 metros. Además, existe otra malla más pequeña cuyos
detectores están separados 750 metros. En la figura \ref{fig:observatory} se muestra la distribución de los
detectores.

Los [!+wcd] del Observatorio de Pierre Auger consisten en tanques de agua de 3.6 metros
de diámetro, que contienen 12,000 litros de agua ultrapura cada uno. En estos tanques están
colocados tres [!+pmt] distribuidos simétricamente, los cuales se encargan de medir 
la radiación Cherenkov. La señal de estos [!+pmt] corresponden a la combinación de la señal muónica y
electromagnética de la *cascada atmosférica extensa*. Como se puede intuir, una sola partícula primaria
puede producir una señal en multiples [!+pmt], incluso en múltiples [!+wcd]. Lo cual complica el análisis de
la naturaleza de la partícula al tener que estudiar las relaciones entre las señales de los diferentes
detectores.


### Definición formal del problema

Los experimentos recogidos en este trabajo están basados en datos de simulaciones, en lugar de los datos
reales. En concreto, se componen diferentes herramientas para la simulación de *cascadas atmosférica extensas*.
El flujo de generación de los datos se muestra en la figura \ref{fig:simulation_flow}. CORSIKA [@heckCORSIKAMonteCarlo1998]
se utilizada para la simulación detallada de como se desarrolla la *cascada atmosférica extensa* en la atmósfera.
Las interacciones hadrónicas se modelan utilizando los paquetes *software* QGSJET-II [@ostapchenkoQGSJETIIReliableDescription2006]
o EPOS-LHC [@pierogEPOSLHCTest2015]. La señales de los [!+wcd] producidas por las partículas se generan utilizando
el software *offline* de Auger [@argiroOfflineSoftwareFramework2007]. Finalmente, los datos de las simulaciones
se almacenan en formato ROOT [@brunROOTObjectOriented1997] para su procesamiento.

Como es de intuir, este tipo de simulaciones requieren una cantidad de recursos de espacio y computacionales enorme,
por este motivo, se utilizada una fracción reducida de los datos. Para esta fracción de los datos, se han recogido
alrededor de 20000 muestras para cada tipo de primario. En este caso, los tipos de primarios disponibles son:
helio, hierro, proton, oxígeno. Para cada primario se han separado los datos en un conjunto de entrenamiento y otro de
test. Siendo la distribución de los datos según el número de ejemplos la siguiente:


| **Primary** | **Training set** | **Test set** | **Total** |
|:-------:|:------------:|:--------:|:-----:|
| Helium  | 16007        | 4001     | 20008 |
| Iron    | 16019        | 4004     | 20023 |
| Proton  | 16026        | 4006     | 20032 |
| Oxygen  | 16021        | 4005     | 20026 |


Como se ha descrito anteriormente, los datos se basan en la simulación de
la señal recogida en los [!+wcd]. Esta señal recoge tanto la parte muónica $\mu$,
como la parte electromagnética $em$. A simple vista, la señal muónica se puede
utilizar para separar entre las diferentes tipos de primario. Pero al existir
varios [!+pmt] en un mismo detector, pueden existir relaciones entre las señales de
cada fotomultiplicador. Para poder atajar este problema con ML/DL es necesario
encontrar un representación del problema tal que nos permita utilizar las señales
de muónicas capturadas por los [!+pmt] para clasificar entre primarios.
Una representación utilizada en trabajos previos, consiste en integrar la señal muónica,
obteniendo un único valor real para cada [!pmt]. 

La representación que se propone en este trabajo consiste en utilizar la media de las señales de los [!+pmt].
Utilizando la media de las tres señales podemos profundizar en la información recogida en la señal, en lugar
de condensar toda esa información en un solo número real (la integral).
Elegir la granularidad con la que se analizan los datos es uno de los retos más importantes de este problema.
Como se ha mencionado al principio del capítulo, una *cascada atmosférica extensa* puede producir una señal en
multiples [!+pmt] dentro de un mismo detector [!wcd], pero además, puede afectar a varios detectores vecinos.
Teniendo esto en cuenta, el problema se puede modelar a nivel de [!pmt], a nivel de [!wcd], o a nivel de estación.
En nuestro caso lo vamos a analizar a nivel de [!wcd].

Como trabajar con la señal en crudo puede ser muy costosa en términos de memoria, y recursos
de CPU, los valores de cada vector se extraen a partir de la salida de *Offline de Auger*.
La señal recogida está discretizada por lo que se puede utilizar como un vector de tamaño
fijo. Sin embargo, según los expertos, la traza puede ser caracterizada en gran medida mediante
un conjunto más pequeño de variables que se describen a continuación:

**Variables extraídas directamente de las simulaciones**

- Energía Monte Carlo ·E·: La energía total (en EeV, Exaelectron Voltios) del rayo cósmico primario (transformada con *log10*)
- Angulo de Zenit Monte Carlo $\Theta$: Angulo en grados entre el zenit y la trayectoria del rayo cósmico primario.
- Distancia al núcleo $r$: Distancia entre cada estación y la posición estimada del núcleo de la cascada, medida en metros.
- Señal total $S_{total}$: Número real en muones equivalentes verticales (VEMs) de la señal capturada por los [!wcd].
- Longitud de la traza: Tamaño del vector de la señal recogida. La señal está discretizada en *bins* de 25 nanosegundos.

**Variables generadas mediante ingeniería de atributos:**

- Ángulo Azimuth $\zeta$: medido en radianes.
- Tiempo de subida $t_{1 / 2}$: medido en nanosegundos [@thepierreaugercollaborationInferencesMassComposition2017].
- Tiempo de caída: Tiempo en el que la señal empieza a descender.
- Area sobre el punto máximo de la señal: Suma de todas las señales en cada traza dividida por el máximo valor en cada traza.

Estas son las variables utilizadas para todos los experimentos llevados a cabo en este capítulo.


## Metodología

Para el desarrollo de los diferentes experimentos se utilizado el framework *ml-experiment* descrito en el capítulo anterior.
Para cada algoritmo de ML o arquitectura de DL se ha implementado un script de entrenamiento y un fichero
de configuración asociado. Como la cantidad de datos o la dimensionalidad de los mismos no son relativamente grandes, se ha
podido aplicar optimización de hiperparámetros. Para ello, el fichero de configuración asociado a cada algoritmo
define un Grupo de experimentos (ver *Diseño y desarrollo del framework*) con un espacio de hiperparámetros
diseñado especialmente para cada tipo de modelo. Estos grupos de experimentos se han ejecutado de manera local
aprovechando todos los núcleos de la CPU. Por otra parte, el proyecto de experimentación se llevado a cabo
teniendo en cuenta los aspectos críticos de la reproducibilidad descritos en *Fundamentos*,
y aplicando las buenas prácticas de MLOps.

![Todos los experimentos ejecutados con sus parámetros, métricas, artefactos, y otros metadatos, se almacenan en un servidor de MLFlow en local](source/figures/mlflow_experiments.png){#fig:mlflow_experiments}

Por una parte, el procedimiento de partición y procesado de los datos se realiza desde una interfaz compartida por todos los scripts
de entrenamiento utilizando las *DataLoader* (ver Manual). En concreto, se ha definido dos *DataLoaders* uno para los autoencoders y otro para el resto de algoritmos.
Para los autoencoders, se genera una pareja de entrenamiento-validación para cada tipo de primario (ver Listing \ref{split_data_loader}).
Para los modelos de aprendizaje supervisado, los datos de entrenamiento de todos los primarios se unifican en un solo conjunto de datos 
y posteriormente se extrae el conjunto de validación (ver Listing \ref{unified_data_loader}).
Finalmente, tanto para conjunto unificado se aplica un *reescalado* *Min-Max*, y para los conjuntos separados 
*estandarización* (mediante *z-score*).

Por otro lado, las semillas para la partición, procesado, y entrenamiento de modelos se establecen y
quedan almacenadas como metadatos en cada experimento. Ésto nos asegura que todos los modelos son entrenados y validados
con los mismos datos, así como facilita la *replicabilidad* del experimento. Además, los parámetros, métricas y artefactos de
cada experimento están almacenados en el servidor de *MLFlow* (ver figura \ref{fig:mlflow_experiments}), permitiendo visualizar
y comparar entre las modelos y entre las diferentes configuraciones de hiperparámetros para cada algoritmo. Finalmente,
la información relativa al hardware y el software donde se han ejecutado los experimentos también queda almacenada,
en concreto, la información relativa al hardware que se ha recogido es la siguiente:

|       Tag      |                                    Value                                   |
|:--------------:|:--------------------------------------------------------------------------:|
|    CPU Info    |                  Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz                  |
| Python Version | 3.7.7 (default, Mar 10 2020) [Clang 11.0.0 (clang-1100.0.33.17)] |
|    GPU Info    |                                      -                                     |


En cuanto a la métrica utiliza para evaluar los modelos, después de conocer que no existe ninguna preferencia respecto a un primario
u otro, y que el conjunto de datos está balanceado, se ha decidido utilizar la precisión (*accuracy*) como métrica. Para evaluar los
modelos se utiliza una partición aleatoria con un ratio 80-20 para entrenamiento y validación respectivamente. Por otro lado, el conjunto de test
se utiliza exclusivamente para evaluar el modelo final seleccionado.


``` {#split_data_loader .python caption="Implementación del DataLoader para autoencoders separados."}
Dataset = Tuple[np.ndarray, np.ndarray]
VALIDATION_SPLIT = 0.2
SEED = 1234


class SplitDataLoader(DataLoader):
    @classmethod
    def load_data(cls) -> Tuple[
                            List[Dataset],
                            List[Dataset]]:
        train_files = glob.glob('data/raw/QGSJet-*-train.txt')
        train_datasets, val_datasets, = [], []
        datasets = [np.genfromtxt(file, delimiter=',')
                    for file in train_files]

        for i, dataset in enumerate(datasets):
            dataset = dataset[:, 3:-1]
            class_vector = np.full(dataset.shape[0], i)

            X_train, X_val, y_train, y_val = train_test_split(
                dataset, class_vector,
                test_size=VALIDATION_SPLIT,
                random_state=SEED)

            scaler = MinMaxScaler()
            X_train = scaler.fit_transform(X_train)
            X_val = scaler.transform(X_val)
            train_datasets.append((X_train, y_train))
            val_datasets.append((X_val, y_val))

        return train_datasets, val_datasets
```

``` {#unified_data_loader .python caption="Implementación de DataLoader para los algoritmos de aprendizaje supervisado."}
class UnifiedDataLoader(DataLoader):
    @classmethod
    def load_data(cls) -> Tuple[np.ndarray,
                                np.ndarray,
                                np.ndarray,
                                np.ndarray]:
        train_files = glob.glob('data/raw/QGSJet-*-train.txt')
        datasets = [np.genfromtxt(file, delimiter=',')
                    for file in train_files]
        X, y = [], []

        for i, dataset in enumerate(datasets):
            X.append(dataset[:, 3:-1])
            y.append(np.full(dataset.shape[0], i))

        X = np.concatenate(X, axis=0)
        y = np.concatenate(y, axis=0)

        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=VALIDATION_SPLIT, random_state=SEED)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_val = scaler.transform(X_val)
        return X_train, X_val, y_train, y_val
```


## Modelos considerados

Entre los algoritmos candidatos, se han empleado [!svm], Xgboost, y Autoencoder (simple, profundo, y variacional).
Como se ha comentado anteriormente, para cada tipo de modelo se utiliza un espacio de hiperparámetros y se ejecuta
un grupo de experimentos (entre 50-100 configuraciones distintas). En las siguientes secciones se especifican el
el espacio de hiperparámetros, detalles de implementación, así como otra información relativa a cada experimento.

### SVM

El primer algoritmo con el que se experimentó fue [!svm] [@cortesSupportvectorNetworks1995]. [!svm] es un algoritmo de aprendizaje
supervisado cuya función de coste tienen como objetivo maximizar el margen entre clases. Además, permite utilizar el
*kernel trick* para entrenar modelos con funciones de decisión complejas mapeando los datos a un espacio de dimensión superior.
La implementación de [!svm] utilizada es LinearSVC de *sklearn* como se puede ver en Listing \ref{svm_code}.
En concreto, se utiliza un [!svm] linear con un transformador basado en *aproximación del kernel*,
una forma de mapear los datos más eficiente que el *kernel trick*, pero también inexacta.
Para la aproximación del kernel se utiliza el método de Nystroem, el cual es un método genérico para aproximaciones de
bajo rango de kernels. A rasgos generales, Nystroem muestrea un número limitado
de ejemplos de entrenamiento (100 por defecto en el caso de *sklearn*) y les aplica el kernel real.
Con esos ejemplos transformados construye una matriz de transformación de bajo rango que aproxima el kernel aplicado 
[@williamsUsingNystromMethod2001]. Ésto permite poder entrenar [!+svm] de manera más eficiente, incluso utilizar *online learning*,
en nuestro caso, nos permite aumentar el número de configuraciones distintas para la optimización de hiperparámetros.
Los detalles del experimento y de la configuración de hiperparámetros son las siguientes:


| Detalle                   | Valor |
|:-------------------------:|:-----:|
| Nombre del experimento    | SVM  |
| Número de configuraciones | 50   |
| Optuna Sampler            | TPE  |

Table: Información general sobre el experimento SVM


| Parámetro | Distribución                          |
|-----------|---------------------------------------|
| C         | loguniform\(0\.001, 1000\)            |
| kernel    | choice\(\['rbf', 'poly', 'linear'\]\) |
| gamma     | choice\(\['scale', 'auto'\]\)         |
| degree    | range\(2, 5\) (solo aplica si kernel = 'poly') |

Table: \label{a1_hyper} Espacio de hiperparámetros para el experimento SVM


``` {#svm_code .python caption="Implementación del script de entrenamiento para SVM."}
from typing import *
from modelling.utils.data import UnifiedDataLoader, SEED
import numpy as np
from ml_experiment import job
from sklearn.svm import LinearSVC
from sklearn.kernel_approximation import Nystroem


@job(data_loader=UnifiedDataLoader())
def main(C: float = 1.0, kernel: str = 'rbf',
         degree: int = 3, gamma: Any = 'scale'):
    np.random.seed(SEED)
    X_train, X_val, y_train, y_val = \
        UnifiedDataLoader.load_data()

    if isinstance(gamma, str):
        if gamma == 'scale':
            gamma = 1.0 / (X_train.shape[1] * X_train.var())
        if gamma == 'auto':
            gamma = 1.0 / X_train.shape[1]

    if kernel != 'linear':
        degree = degree if kernel == 'poly' else None
        feature_map = Nystroem(
            kernel=kernel, gamma=gamma, degree=degree)
        X_train = feature_map.fit_transform(X_train)
        X_val = feature_map.transform(X_val)

    model = LinearSVC(C=C)
    model.fit(X_train, y_train)
    accuracy = model.score(X_val, y_val)
    return {'val_accuracy': accuracy}


if __name__ == '__main__':
    main()
```

### Xgboost

El segundo modelo con el que se ha experimentado a sido XGBoost [@chenXGBoostScalableTree2016].
XGBoost es un algoritmo *gradient boosting* [@masonBoostingAlgorithmsGradient2000] flexible, escalable, y portable. Permite *boosting*
de arboles en paralelo, así como definir funciones de coste propias [@masonBoostingAlgorithmsGradient2000].
Uno de los inconvenientes a la hora de realizar [!hpo] con XGBoost (y con los ensamblados de árboles en general), es la cantidad
de hiperparámetros distintos que se pueden modificar. Ésto hace que el espacio de hiperparámetros sea demasiado grande como para
cubrirlo uniformemente de manera acertada. Por este motivo, es de especial importancia el uso de algoritmos de [!hpo] más novedosos que GridSearch
para poder explorar zonas del espacio más interesantes. En concreto, se utiliza TPE (*Tree-structured Parzen Estimator*) al igual que en el resto
de modelos. A rasgos generales, TPE ajusta un modelo Modelo Gaussiano de Mezcla (*GMM*) $l(x)$ al conjunto de hiperparámetros asociados a los mejores valores
de la métrica hasta el momento, y luego otro GMM $g(x)$ con el resto de valores de hiperparámetros.
Finalmente, se coge el parámetro $x$ que maximice el ratio $l(x)/g(x)$.

| Detalle                   | Valor |
|:-------------------------:|:-----:|
| Nombre del experimento    | XGBoost  |
| Número de configuraciones | 100   |
| Optuna Sampler            | TPE  |

Table: Información general sobre el experimento XGBoost.

| Parámetro | Distribución                          |
|-----------|---------------------------------------|
| num_boost_round | choice([10, 100, 250, 500, 1000, 2500]) |
| learning_rate | loguniform(0.0001, 1) |
| max_depth | range(2, 15) |
| gamma | choice([0, 0.5, 2, 10, 20]) |
| min_child_weight | loguniform(0.01, 1) |
| subsample | uniform(0.1, 0.9) |

Table: \label{a1_hyper} Espacio de hiperparámetros para el experimento XGBoost.

Además, para mejorar el rendimiento del trabajo de [!hpo], se hace uso de varios *callbacks* de XGBoost para *podar* configuraciones no prometedoras (ver Listing \ref{xgboost_code}).
De esta forma, conforme se van probando configuraciones, los modelos menos prometedores no terminan de construirse, ahorrando así cómputo.
El primero de ellos es *XGBoostPruningCallback* de *Optuna* que permite abortar configuraciones no prometedoras según el espacio de hiperparámetros ya explorado y las métricas recogidas
anteriormente. El segundo de ellos es un *callback* de *Early Stopping*, se utiliza para parar el entrenamiento cuando no existe mejora (o incluso empeora) en sucesivas iteraciones.
En este caso, el número de iteraciones mínimo donde debe haber mejora es de $numero\_estimadores / 10$. Por último, se utiliza el *callback* *record_evaluation* para guardar
los resultados del entrenamiento a lo largo de las iteraciones y evitar el cómputo de evaluar el modelo al final del entrenamiento (ya lo hace XGBoost internamente).


``` {#xgboost_code .python caption="Implementación del script de entrenamiento para Xgboost."}
@job(data_loader=UnifiedDataLoader(),
     autologging_backends=AutologgingBackend.XGBOOST)
def main(n_estimators: int, learning_rate: float,
         max_depth: int, gamma: float,
         subsample: float, min_child_weight: float):
    np.random.seed(SEED)

    X_train, X_val, y_train, y_val = \
        UnifiedDataLoader.load_data()
    train_data = xgb.DMatrix(X_train, label=y_train)
    val_data = xgb.DMatrix(X_val, label=y_val)
    params = dict(random_state=SEED,
                  learning_rate=learning_rate,
                  max_depth=max_depth, gamma=gamma,
                  subsample=subsample,
                  min_child_weight=min_child_weight,
                  num_class=len(np.unique(y_train)),
                  objective='multi:softmax')

    trial = Trial.get_current()
    evallist = [(val_data,'eval'),(train_data,'train')]
    eval_result = {}
    patience = max(10, n_estimators // 10)
    callbacks = [
        XGBoostPruningCallback(trial, 'eval-merror'),
        xgb.callback.early_stop(patience, verbose=False),
        xgb.callback.record_evaluation(eval_result)
    ]

    xgb.train(params, train_data,
              num_boost_round=n_estimators,
              evals=evallist,
              callbacks=callbacks,
              verbose_eval=False)

    accuracy = 1 - eval_result['eval']['merror'][-1]
    return {'val_accuracy': accuracy}

if __name__ == '__main__':
    main()
```

### Autoencoder V1

| Detalle                   | Valor |
|:-------------------------:|:-----:|
| Nombre del experimento    | Autoencoder V1 |
| Número de configuraciones | 100   |
| Optuna Sampler            | TPE  |
| Épocas de entrenamiento   | 200  |

Table: Información general sobre el experimento Autoencoder V1

Para los algoritmos basados en autoencoders, se han propuesto dos experimentos por separado.
El primero de ellos, consiste en un autoencoder *denoising* con probabilidad de descarte $p$ y con soporte
para *Tied-weights* (ver Tabla \ref{a1_hyper}). Además, tiene las siguientes características:

- La red consta de únicamente tres capas, la capa de entrada, la capa del código cuyo número
de neuronas viene dado por el parámetros *encoding_dim*, y la capa de salida.

- Permite dos funciones de activación distintas: *RELU* y *SELU*. *SELU* es un función de activación
moderna (2017), que junto con *Swish* y *ELU*, suele arrojar resultados mejores en comparación con RELU.
Aunque la mayoría de investigación al respecto está enfocada a problemas de clasificación de imágenes,
lo cual hace realmente difícil la comparativa entre ambas aplicadas a *autoencoders*.

- [!pca] y autoencoders (sobre todo lineales) tienen muchas similaridades, al fin y al cabo, ambos permiten proyectar
vectores a espacio de dimensión inferior. Los autoencoders por su parte, no pueden ofrecer algunas características interesantes
de [!PCA] como la ortonormalidad, es decir, vectores ortogonales y unitarios en la base del espacio del código.
En este trabajo se han implementado dos restricciones a nivel de capa para asegurar la ortonormalidad,
una restricción para ortogonalidad propia (ver Listing \ref{weight_orthogonality}),
y una restricción para el tamaño unitario de las componentes del espacio latente utilizando *UnitNorm* de *Keras*.
Existen además otras propiedades de [!pca] que se han adaptado a autoencoders [@ladjalPCAlikeAutoencoder2019],
como por ejemplo, forzar a que los componentes del espacio latente sean estadísticamente independientes.
Dichas características se salen del alcance de este trabajo.


| Parámetro | Distribución                          |
|-----------|---------------------------------------|
| encoding_dim | range(1, 20) |
| ps | uniform(0, 0.5) |
| lr | loguniform(0.001, 0.1) |
| activation | choice(['selu', 'relu']) |
| tied_weights | choice([false, true]) |
| unit_norm_constraint | choice([false, true]) |
| weight_orthogonality | choice([false, true]) |

Table: \label{a1_hyper} Espacio de hiperparámetros para el experimento Autoencoder V1


``` {#weight_orthogonality .python caption="Implementación del la restricción para ortogonalidad en las componentes del espacio latente en autoencoders. Fuente: https://towardsdatascience.com/build-the-right-autoencoder-tune-and-optimize-using-pca-principles-part-ii-24b9cca69bd6"}
class WeightsOrthogonalityConstraint(constraints.Constraint):
    def __init__(self, encoding_dim, weightage=1.0, axis=0):
        self.encoding_dim = encoding_dim
        self.weightage = weightage
        self.axis = axis

    def weights_orthogonality(self, w):
        if self.axis == 1:
            w = K.transpose(w)
        if self.encoding_dim > 1:
            m = K.dot(K.transpose(w), w) - K.eye(self.encoding_dim)
            return self.weightage * K.sqrt(K.sum(K.square(m)))
        else:
            m = K.sum(w ** 2) - 1.
            return m

    def __call__(self, w):
        return self.weights_orthogonality(w)
```

### Autoencoder V2

Para la segunda versión del autoencoder se han implementado dos características principales con respecto a la versión 1:

- El número de capas para el codificador y decodificador son mayores que 1. Es decir, el autoencoder V2
corresponde a un autoencoder *denoising* apilado. El número de capas a cada lado del código varía entre 2 a 4,
y el número de neuronas por capa entre 2 a 20. Tanto el número de capas como el de neuronas se controla con
el parámetro *encoding_dim* (ver Tabla \ref{a2_hyper}). Por ejemplo, si $encoding\_dim = [5, 5, 4]$ el autoencoder
tendrá la siguiente arquitectura: *Input + Dense(5) + Dense(5) + Dense(4) + Dense(5) + Dense(5) + Output*. Es decir, el vector
*encoding_dim* representa el codificador entero incluido el código. y como el autoencoder es simétrico, el decodificador
también esta definido con ese mismo vector.

- Se ha utilizado una política de entrenamiento con un esquema de actualización del ratio de aprendizaje. En concreto,
se ha utilizado OneCycle [@smithDisciplinedApproachNeural2018] para adaptar el ratio de aprendizaje a lo largo de las épocas hasta llegar ha un máximo definido
por el parámetro del experimento *lr* (ver Tabla \ref{a2_hyper}). El motivo principal por el que se ha decidido utilizar
una política de actualización del ratio de aprendizaje, es porque al aumentar la complejidad del autoencoder, el riesgo de
sobreajuste aumenta, con OneCycle* conseguimos hacer que el propio ratio de aprendizaje actué de regularizador a lo largo del entrenamiento
[@smithDisciplinedApproachNeural2018].


| Detalle                   | Valor |
|:-------------------------:|:-----:|
| Nombre del experimento    | Autoencoder V1 |
| Número de configuraciones | 90   |
| Optuna Sampler            | TPE  |
| Épocas de entrenamiento   | 200  |

Table: Información general sobre el experimento Autoencoder V2


| Parámetro | Distribución                          |
|-----------|---------------------------------------|
| encoding_dim | range(2, 20) $\times$ range(2, 5)  |
| ps | uniform(0, 0.5) |
| lr | loguniform(0.001, 0.1) |
| activation | choice(['selu', 'relu']) |
| tied_weights | choice([false, true]) |
| one_cycle | choice([false, true]) |
| unit_norm_constraint | choice([false, true]) |
| weight_orthogonality | choice([false, true]) |

Table: \label{a2_hyper} Espacio de hiperparámetros para el experimento Autoencoder V1


### Autoencoder Variacional

El tercer y último tipo de autoencoder con el que se ha experimentado ha sido el variacional.
En este caso, se ha implementado un VAE puro, es decir, sin capa de *Dropout*, *Tied-weights*, características
de PCA, etc. Además, se ha utilizado una arquitectura sencilla para evitar el sobreajuste que consiste en
5 capas, capa de entrada, capa de salida, la capa del código, y una capa para el codificador y otra para el decodificador
(ver Figura \ref{fig:vae_arch}).


![Arquitectura del autoencoder variacional implementado. Fuente propia](source/figures/vae_arch.png){#fig:vae_arch}


La arquitectura es siempre simétrica, es decir, las capas a un lado y a otro del código coinciden.
Los únicos parámetros que se ajustan mediante [!hpo] son: el número de neuronas en la capa del codificador y decodificador, el tamaño del código,
y si se hace uso o no de *OneCycle* para entrenar el modelo (ver detalles en Tabla \ref{vae_hyper}).


| Detalle                   | Valor |
|:-------------------------:|:-----:|
| Nombre del experimento    | Variational Autoencoder |
| Número de configuraciones | 50   |
| Optuna Sampler            | TPE  |
| Épocas de entrenamiento   | 200  |

Table: Información general sobre el experimento Autoencoder Variacional


| Parámetro | Distribución     |
|-----------|------------------|
| encoding_dim | range(2, 15)  |
| latent_dim | range(2, 5)  |
| activation | choice(['selu', 'relu']) |
| one_cycle | choice([false, true]) |

Table: \label{vae_hyper} Espacio de hiperparámetros para el experimento Autoencoder Variacional


#### Truco de la reparametrización

Como se ha descrito en *Fundamentos*, para poder entrenar sobre una variable aleatoria es necesario hacer el *truco de la reparametrización*.
Para ello, hay que definir una capa Lambda de Keras que permita ejecutar una función de Tensorflow o Pytorch arbitraria. En este caso,
se definen dos capas densas $\mu$ y $\sigma$ con número de neuronas igual al tamaño del código, y se utiliza el *Lambda* para transformar
una variable aleatoria $z$ en una combinación de $\mu$ y $\sigma$ con un ruido $\epsilon$ (ver Listing \ref{reparam_trick}). Recordemos
que el truco de la reparametrización hace básicamente lo siguiente:

$$
\mathbf{z}=\boldsymbol{\mu}+\boldsymbol{\sigma} \odot \boldsymbol{\epsilon}, \text { where } \boldsymbol{\epsilon} \sim \mathcal{N}(0, \boldsymbol{I})
$$
Para:
$$
\mathbf{z} \sim q_{\phi}\left(\mathbf{z} \mid \mathbf{x}^{(i)}\right)=\mathcal{N}\left(\mathbf{z} ; \boldsymbol{\mu}^{(i)}, \boldsymbol{\sigma}^{2(i)} \boldsymbol{I}\right) \\
$$


``` {#reparam_trick .python caption="Implementación del truco de la reparametrización para Keras. Fuente: Documentación oficial de Keras."}
import keras.backend as K

def sampling(args):
    """Reparameterization trick by sampling from an isotropic unit Gaussian.

    # Arguments
        args (tensor): mean and log of variance of Q(z|X)

    # Returns
        z (tensor): sampled latent vector
    """
    z_mean, z_log_var = args
    batch = K.shape(z_mean)[0]
    dim = K.int_shape(z_mean)[1]
    # by default, random_normal has mean = 0 and std = 1.0
    epsilon = K.random_normal(shape=(batch, dim))
    return z_mean + K.exp(0.5 * z_log_var) * epsilon
```

#### Función de coste

Por otro lado, hay que cambiar la función de coste para este tipo de autoencoder, la cuál debe incluir el término de divergencia KL (Kullback–Leibler).
Para ello, se hace uso de una función de coste personalizada para Keras (ver Listing \ref{cost_function_vae}).

``` {#cost_function_vae .python caption="Función de coste para VAE. Fuente: Documentación oficial de Keras."}
import keras.backend as K

def create_loss(input_dim, inputs, outputs, mu, sigma):
    # VAE loss = mse_loss or xent_loss + kl_loss
    reconstruction_loss = mse(inputs, outputs) * input_dim
    kl_loss = 1 + sigma - K.square(mu) - K.exp(sigma)
    kl_loss = K.sum(kl_loss, axis=-1)
    kl_loss *= -0.5
    return K.mean(reconstruction_loss + kl_loss)
```

Básicamente se define la función de coste de un autoencoder básico (MSE normalmente), y se le suma
$\mathbb{K} \mathbb{L}\left(q_{\theta}\left(z \mid x_{i}\right) \| p(z)\right)$.


### Construcción del modelo

Finalmente, la construcción del modelo se implementa de manera sencilla (ver Listing \ref{create_model_vae}):

1. Se define la capa de entrada
2. Se define la capa (o capas) del encoder
3. Se define $\mu$, $\sigma$ y $z$
4. Se crea el decodificador
5. Por último, se construye el autoencoder conectando todas las partes de la arquitectura y añadiendo
la función de coste personalizada.


``` {#create_model_vae .python caption="Construcción del autoencoder VAE."}
def create_model(
        input_size: int,
        encoding_dim: Union[List[int], int],
        latent_dim: int,
        lr: float,
        activation: str = 'relu'):

    np.random.seed(SEED)
    decoding_dim = [input_size] + encoding_dim[:-1]

    inputs = Input(shape=(input_size, ),
                   name='encoder_input')
    encoder = inputs

    for i, units in enumerate(encoding_dim):
        kwargs = {'input_shape': (input_size,)} if i == 0 else {}
        encoder = Dense(units, activation=activation, **kwargs)(encoder)

    mu = Dense(latent_dim, name='mu')(encoder)
    sigma = Dense(latent_dim, name='log_var')(encoder)
    z = Lambda(sampling,
               output_shape=(latent_dim,),
               name='z')([mu, sigma])
    encoder = Model(
        inputs,
        [mu, sigma, z],
        name='encoder') 
    latent_inputs = Input(
        shape=(latent_dim,),
        name='z_sampling')
    decoder = latent_inputs

    for i, units in enumerate(decoding_dim[::-1]):
        layer_activation = 'sigmoid' if i == len(encoding_dim) - 1 else activation
        decoder = Dense(
            units,
            activation=layer_activation)(decoder)

    decoder = Model(latent_inputs, decoder, name='decoder')
    outputs = decoder(encoder(inputs)[2])
    autoencoder = Model(inputs, outputs, name='vae_mlp')
    loss = create_loss(input_size, inputs, outputs, mu, sigma)
    autoencoder.add_loss(loss)
    autoencoder.compile(SGD(learning_rate=lr), loss='mse')
    return autoencoder, encoder, decoder
```

## Resultados

En esta sección se analizan los resultados obtenidos para los diferentes modelos.
En cada subsección aparecen recogidas las gráficas que relacionan los diferentes hiperparámetros
con la métrica de validación. Además, en la tabla \ref{results_table} se muestran los resultados de
el mejor modelo para cada algoritmo.

---------------------------------------------------------------------------------
  Algoritmo                    Parámetros                        Métrica
--------------       --------------------------------    -------------------------
   SVM                    C: 1e-4 \                       $0.64036 \pm 0.0043678$
                          degree: no aplica \
                          gamma: auto \
                          kernel: lineal \

  XGBoost                 gamma: 0 \                      $0.88519 \pm 0.0029017$
                          learning_rate: 0.42 \
                          max_depth: 5 \
                          min_child_weight: 0.4133 \
                          n_estimators: 4500 \
                          subsample: 0.9924 \

Autoencoder V1            activation: selu \              $0.69825 \pm 0.0041778$
                          encoding_dim: 10 \
                          learning_rate: 0.001 \
                          optimizer_name: Adam \
                          ps: 0.031 \
                          tied_weights: True \
                          unit_norm_constraint: False \
                          weight_orthogonality: False \

Autoencoder V2            activation: selu \             $0.56267 \pm 0.0045149$
                          encoding_dim: [9, 9, 7] \
                          learning_rate: 0.00338 \
                          optimizer_name: SGD \
                          ps: 0.002 \
                          ony_cycle: True \
                          tied_weights: True \
                          unit_norm_constraint: True \
                          weight_orthogonality: False \

VAE                       activation: selu \             $0.38315 \pm 0.0044247$
                          encoding_dim: 13 \
                          latent_dim: 3 \
                          learning_rate: 1e-04 \
                          optimizer_name: SGD \
                          ony_cycle: True
-----------------------------------------------------------------------

Table: \label{results_table} Resultados para los mejores modelos de cada tipo sobre el conjunto de test. Las métricas están redondeadas a 5 decimales
e incluyen intervalos a un 99% de confianza. Los intervalos de confianza se han calculado utilizando el *score* de *Wilson* 
[@newcombeIntervalEstimationDifference1998].


### SVM

En general, el rendimiento de [!svm] para este problema es pobre. Exceptuando una configuración sin transformación de datos (kernel lineal),
y con un parámetro de regularización $C$ muy bajo, el cual fuerza al clasificador a tener margen entre clases grande. En cuanto al parámetro
$C$, se ve claramente como los valores bajos ofrecen los mejores resultados. En cuanto al resto de parámetros, no se ve una tendencia clara
sobre si un *kernel* o *gamma* determinado ofrece mejores resultados que el resto. De hecho, la configuración con mejor rendimiento se podría
considerar un *outlier*. Ésto no implica que el modelo no sea correcto, significa que deberíamos probar un número más alto de configuraciones
para poder sacar conclusiones más exactas.

![SVM. C vs Precisión en validación](source/results/svm_analysis/c_vs_accuracy.png){#fig:svm_c width=75%}

![SVM. Kernel vs Precisión en validación](source/results/svm_analysis/kernel_accuracy.png){#fig:svm_kernel width=75%}

![SVM. Gamma vs Precisión en validación](source/results/svm_analysis/gamma_vs_accuracy.png){#fig:svm_gamma width=70%}

![SVM. Comparación de parámetros](source/results/svm_analysis/parallel_plot.png){#fig:svm_parallel}

### Xgboost

En cuanto a XGBoost, todos los modelos funcionan muy bien de manera general. Viendo los datos recogidos, se puede argumentar
que existe una correlación positiva entre el número de arboles del ensamblado (también llamado rondas) y la precisión en validación
(Figura \ref{fig:xgboost_num_trees}).
Por otro lado, también existe una correlación positiva entre *subsample* (ratio de columnas con las que se entrena cada árbol) y la
precisión (Figura \ref{fig:xgboost_subsample}). En cuanto a los parámetros del ratio de aprendizaje y *min_child_weight*,
se puede apreciar que valores muy bajos deterioran el rendimiento, mientras que un *gamma* de 0 suele ofrecer los mejores resultados.
(Figuras \ref{fig:xgboost_lr}, \ref{fig:xgboost_min_child_weight}, \ref{fig:xgboost_gamma})
El motivo por el que en el parámetro *gamma*, por ejemplo,
los puntos no están uniformemente distribuidos entre cada valor del espacio de hiperparámetros, es que al aplicar el algoritmo de optimización
probabilístico TPE, el espacio de hiperparámetros se explora siguiendo las regiones más prometedoras, en lugar de explorarse uniformemente.
Ésto mismo ocurre con el parámetro *max_depth* (Figura \ref{fig:xgboost_max_depth}), donde el valor de 5 ofrece los mejores resultados
y es por eso que hay más configuraciones con ese valor que con otras.

![Xgboost. Gamma vs Precisión en validación](source/results/xgboost_analysis/gamma_vs_accuracy.png){#fig:xgboost_gamma}

![Xgboost. Number of trees vs Precisión en validación](source/results/xgboost_analysis/newplot.png){#fig:xgboost_num_trees}

![Xgboost. Learning rate vs Precisión en validación](source/results/xgboost_analysis/learning_rate_vs_accuracy.png){#fig:xgboost_lr}

![Xgboost. Min child weight vs Precisión en validación](source/results/xgboost_analysis/min_child_weight_vs_accuracy.png){#fig:xgboost_min_child_weight}

![Xgboost. Max depth vs Precisión en validación](source/results/xgboost_analysis/max_depth_vs_accuracy.png){#fig:xgboost_max_depth}

![Xgboost. Subsample vs Precisión en validación](source/results/xgboost_analysis/subsample_vs_accuracy.png){#fig:xgboost_subsample}

![Xgboost. Comparación de parámetros](source/results/xgboost_analysis/parallel_plot.png){#fig:xgboost_parallel}


### Autoencoder v1

Para la primera versión de autoencoder, el cuál sorprendentemente tiene un rendimiento mejor que SVM,
podemos decir que las restricciones tanto de ortonormalidad no mejoran la precisión en validación.
Por otro lado, vemos que el nivel de ruido ($ps$) influye positivamente cuando se aplica ligeramente (Figura \ref{fig:a1_ps}).
El ratio de aprendizaje no sigue un patrón bien definido, pero el algoritmo de [!hpo] ha considerado como configuraciones más prometedoras
aquellas con un ratio de aprendizaje más bajo (Figura \ref{fig:a1_lr}).
Por otro lado, emplear la técnica de *Tied-weights* parece mejorar el rendimiento considerablemente (Figura \ref{fig:a1_tied_weights}).
Finalmente, la dimensión del código óptima se encuentra entre 10 y 12, que coincide prácticamente con la dimensión de los datos de entrada
(Figura \ref{fig:a1_encoding_dim}).

![Autoencoder v1. Dimensión del código vs Precisión en validación](source/results/autoencoder_v1_analysis/encoding_dim_vs_accuracy.png){#fig:a1_encoding_dim}

![Autoencoder v1. Tied-weights vs Precisión en validación](source/results/autoencoder_v1_analysis/tied_weights.png){#fig:a1_tied_weights}

![Autoencoder v1. Probabilidad de descarte (dropout) vs Precisión en validación](source/results/autoencoder_v1_analysis/ps_vs_accuracy.png){#fig:a1_ps}

![Autoencoder v1. Restricción de ortogonalidad vs Precisión en validación](source/results/autoencoder_v1_analysis/weight_orthogonality_vs_accuracy.png){#fig:a1_weight_ortho}

![Autoencoder v1. Restricción UnitNorm vs Precisión en validación](source/results/autoencoder_v1_analysis/unit_norm_vs_accuracy.png){#fig:a1_unit_norm}

![Autoencoder v1. Ratio de aprendizaje vs Precisión en validación](source/results/autoencoder_v1_analysis/learning_rate_vs_accuracy.png){#fig:a1_lr}

![Autoencoder v1. OneCycle vs Precisión en validación](source/results/autoencoder_v1_analysis/onecycle_vs_accuracy.png){#fig:a1_optimizer}

![Autoencoder v1. Comparación de parámetros](source/results/autoencoder_v1_analysis/parallel_plot.png){#fig:a1_parallel}


### Autoencoder v2

Para la segunda versión de autoencoder, la restricción de ortogonalidad no mejora el rendimiento (Figura \ref{fig:a2_weight_ortho}),
pero la restricción de pesos unitarios si
que mejora ligeramente (Figura \ref{fig:a2_unit_norm}). También, podemos ver que tanto Tied-weight  como OneCycle mejoran
considerablemente el rendimiento (Figuras \ref{fig:a2_tied_weights} \ref{fig:a2_one_cycle}).
Ésto puede ser debido a que al incrementar la complejidad de la arquitectura, ambas técnicas permitan mantener
el sobreajuste bajo mientras se aumenta el poder de predicción. Por otro lado, tanto el porcentaje de ruido como
el ratio de aprendizaje parecen ser óptimos en niveles muy bajos (Figuras \ref{fig:a2_ps} \ref{fig:a2_lr}).
Por último, se puede ver como tres capas por delante y por detrás de la capa del código es el número óptimo para esta arquitectura (Figura \ref{fig:a2_encoding_dim}).
A la luz de estos datos, podríamos argumentar que las arquitecturas menos profundas funcionan mejor para este problema en concreto (véase *Autoencoder V1*).

![Autoencoder v2. Dimensión del código vs Precisión en validación](source/results/autoencoder_v2_analysis/encoding_dim.png){#fig:a2_encoding_dim}

![Autoencoder v2. Probabilidad de descarte (dropout) vs Precisión en validación](source/results/autoencoder_v2_analysis/ps.png){#fig:a2_ps}

![Autoencoder v2. Pesos ortogonales vs Precisión en validación](source/results/autoencoder_v2_analysis/weight_orthogonality.png){#fig:a2_weight_ortho}

![Autoencoder v2. Restricción UnitNorm vs Precisión en validación](source/results/autoencoder_v2_analysis/unit_norm_constraint.png){#fig:a2_unit_norm}

![Autoencoder v2. Ratio de aprendizaje vs Precisión en validación](source/results/autoencoder_v2_analysis/learning_rate.png){#fig:a2_lr}

![Autoencoder v2. Tied-weights vs Precisión en validación](source/results/autoencoder_v2_analysis/tied_weights.png){#fig:a2_tied_weights}

![Autoencoder v2. One-cycle vs Precisión en validación](source/results/autoencoder_v2_analysis/one_cycle.png){#fig:a2_one_cycle}

![Autoencoder v2. Comparación de parámetros](source/results/autoencoder_v2_analysis/parallel_plot.png){#fig:a2_parallel}


### Autoencoder Variacional

Para la arquitectura VAE, vemos que el rendimiento es muy pobre. Dentro del rango de valores de la métrica para este modelo, vemos como un
ratio de aprendizaje bajo, y la aplicación de OneCycle favorecen el rendimiento (ver Figuras \ref{fig:vae_lr} \ref{fig:vae_one_cycle}).
Aún así, esta arquitectura solamente arroja unos resultados
ligeramente mejores que un clasificador aleatorio ^[Un clasificador aleatorio tendría una precisión del 25%]. Para el resto de parámetros
no podemos destacar ningún patrón en la precisión (ver Figuras \ref{fig:vae_encoding_dim} \ref{fig:vae_activation} \ref{fig:vae_latent_dim}).


![Autoencoder Variacional. Dimensión de la capa intermedia vs Precisión en validación](source/results/vae_analysis/encoding_dim.png){#fig:vae_encoding_dim}

![Autoencoder Variacional. Dimensión del espacio latente vs Precisión en validación](source/results/vae_analysis/latent_dim.png){#fig:vae_latent_dim}

![Autoencoder Variacional. Ratio de aprendizaje vs Precisión en validación](source/results/vae_analysis/learning_rate.png){#fig:vae_lr}

![Autoencoder Variacional. One-cycle vs Precisión en validación](source/results/vae_analysis/one_cycle.png){#fig:vae_one_cycle}

![Autoencoder Variacional. Activation vs Precisión en validación](source/results/vae_analysis/activation.png){#fig:vae_activation}

![Autoencoder Variacional. Comparación de parámetros](source/results/vae_analysis/parallel_plot.png){#fig:vae_parallel}
