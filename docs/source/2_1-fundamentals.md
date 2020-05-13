# Fundamentos


## Reproducibilidad


https://arxiv.org/pdf/1709.01154.pdf


While the
studies provide useful reports of their results, they lack information on access to
the dataset in the form and order as used in the original study (as against raw data),
the software environment used, randomization control and the implementation
of proposed techniques. In order to increase the chances of being reproduced,
researchers should ensure that details about and/or access to information about
these factors are provided in their reports.


Independent verification of published claims for the purpose of credibility confirmation, extension
and building a ‘body of knowledge’ is a standard scientific practice [13]. Machine learning methods
based research are not excluded from this strict scientific research requirement. However, it may
sometimes be hard or even impossible to replicate computational studies of this nature [12]. This is
why the minimum standard expected of any computational study is for it to be reproducible [11].
In order for a study to be reproduced, an independent researcher will need at least full information
and artefacts of the experiment - datasets, experiment parameters, similar software and hardware
environment etc., as used in the original study. However, the experience in studies today shows a lack
of sufficient information that can enable an independent researcher reproduce majority of the studies
successfully.



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
