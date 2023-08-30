# ARGC Demo // 09.06.23

Welcome to the GitHub page for Will Wright's ARGC presentation on open source tools for geospatial viz! The demo will walk through how to use Python to create a simple Streamlit web app for visualizing home sales in Forsyth County, GA. Follow the steps below for setting up a virtual environment after cloning this repo. You can also find helpful documentation links below.

## Create virtual environment

We will be using a variety of Python packages in the demonstration. To follow along, we recommend you create a virtual conda environment using the included `environmnet.yml` file in this repo as shown in the steps below. This creates a contained "sandbox" of tools ready-made for the included Jupyter and Python files.

1) If you don't have conda installed locally, do so using either the popular Anaconda (link <a href="https://www.anaconda.com/">here</a>) or lighweight Miniconda (link <a href="https://docs.conda.io/en/latest/miniconda.html">here</a>) Python distributions.
2) Clone this repo and navitage to it via terminal or command prompt.
3) Create a new conda environment (which will automatically include all necessary Python packages) by executing the following bash command:
`conda env create -f environment.yml` <em>Note: This process may take a few minutes to complete, depending on the speed of your network connection.</em> 

5) Once the environment is created, activate it by running the following command: `conda activate argc-demo`

6) Set up a new Jupyter kernel corresponding to the environment you just created. Unfortunately, conda no longer automatically sets up environments as Jupyter kernels, so you have to do this manually. Never fear, it's not hard. Simply run the following command:
`python -m ipykernel install --user --name argc-demo`

7) With the 'argc-demo' environment activated, you can start a Jupyter server in the same terminal or command prompt window using either of the following commands:
`jupyter notebook` - or - `jupyter lab` Keep in mind JupyterLab is a newer, more feature-rich IDE as compared to the older Jupyter Notebook. You can choose either for the demo!  

At this point, you're all set 🔥

## Documentation links
 - <a href="https://pandas.pydata.org/docs/index.html">Pandas (spatial data analysis)</a>
 - <a href="https://geopandas.org/en/stable/">Geopandas (geospatial data analysis)</a>
 - <a href="https://selenium-python.readthedocs.io/index.html">Selenium (web browswer automation)</a>
 - <a href="https://pydeck.gl/">Pydeck (mapping libarary)</a>
 - <a href="https://streamlit.io/">Streamlit (building web apps)</a>
