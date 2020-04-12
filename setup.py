import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ml-experiment',
    version="0.0.1",
    author="Antonio Molner Domenech",
    author_email="antonio.molner@correo.ugr.es",
    description="A tool for reproducible ML experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aguillenATC/TFG-AntonioMolner",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['ml-experiment=ml_experiment.scripts.run_experiment:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'docker>=4.1.0',
        'EasyProcess>=0.2.10',
        'mlflow',
        'gorilla>=0.3.0',
        'optuna>=1.1.0',
        'docstring-parser>=0.6',
        'pydantic>=1.4',
        'python-dotenv>=0.10.3',
        'ray>=0.8.2',
        'PyYAML>=5.1.2',
        'pytictoc>=1.5.0',
        'coloredlogs>=10.0',
        'py-cpuinfo>=5.0.0',
        'numpy>=1.17.4',
    ]
)
