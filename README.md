![Logo](https://github.com/mayabenowitz/neuralcraft/blob/master/src/apps/logo3.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<br><br />
Hello fellow Pioneers!
<br><br />

Welcome to the research repository of the Neuralcraft project! Here you will find the code for our [Streamlit](https://www.streamlit.io/) app. The app is a **living breathing blueprint for the project**, designed to walk the reader through the project's objectives and vision through data, design, and immersive storytelling. Readers have the freedom to explore current wireframes, prototypes, datasets, interactive visualizations, game documents, data modeling, technical writing, blog articles, video content, etc. Everything related to the evolution of this project is stored and versioned here!

<br><br />
For a HIGH level overview of the project check out our [pitch deck](https://github.com/mayabenowitz/neuralcraft/blob/master/reports/neuralcraft-2020-09-20.pdf).

<br><br />
## Pioneer Progress

### Week 2: 

 * #### Objective: Tell an interactive data story of the problem Neuralcraft intends to solve. Design a few pages of the app to act as community building tool that raises awareness of deeply troubling macroeconomic trends in education.
 * #### Intended Outcomes: Recruit developers and creatives to join the cause. Organize a movement-first business!
 * #### Completed Tasks: Loaded and cleaned another dataset, wrote code to handle new data for interactive visualizations, polished app front-end, added a logo, wireframed out some ideas.


![Data App](https://github.com/mayabenowitz/neuralcraft/blob/master/reports/week-2.png)
![Data App](https://github.com/mayabenowitz/neuralcraft/blob/master/reports/week-2.5.png)
![Data App](https://github.com/mayabenowitz/neuralcraft/blob/master/reports/week-2.8.png)

<br><br/>
Repository Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
        │          
        ├── apps
        │    └── app.py    <- Streamlit application
        │        
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------
