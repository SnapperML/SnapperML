import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='snapper-ml',
    version=os.environ.get('PROJECT_VERSION', '0.1.0'),
    author="Antonio Molner Domenech",
    author_email="antonio.molner@correo.ugr.es",
    description="A framework for reproducible machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SnapperML/SnapperML",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['snapper-ml=snapper_ml.scripts.run_experiment:app'],
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
        'typer>=0.1.1',
        'pystache',
        'shellingham',
        'colorama',
        'numpy'
    ],
    dependency_links=['https://github.com/SnapperML/knockknock.git@master#egg=knockknock']
)
