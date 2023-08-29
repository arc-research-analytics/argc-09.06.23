# ARGC Demo // 09.06.23

Welcome to the GitHub page for Will Wright's ARGC presentation on open source tools for geospatial viz! The demo will walk through how to use Python to create a simple Streamlit web app for visualizing home sales in Forsyth County, GA. Follow the steps below for setting up a virtual environment once you clone this repo. The README file also features helpful documentation links at the bottom.

## Install virtual environment

We will be using several packages for today's demonstration on open source tools in Python.

An easy way to install all the required packages is by using a Python distribution such as Anaconda or Miniconda. In this demo, we will utilize a conda environment to create a contained "sandbox" that is ready to use for the included Jupyter and Python files.

1) If you don't have a Python distribution installed locally, please download and install one first.
2) Next, open a terminal or command prompt and navigate to the directory where you cloned this repository.
3) Then, create a new conda environment (which will automatically include all necessary packages) by using the following command:

`conda env create -f environment.yml`

<em>Note:</em> This process may take a few minutes to complete, depending on the speed of your network connection. 

4) Once the environment is created, you need to activate it. Use the following command in your terminal or command prompt:

`conda activate argc-demo`

5) With the 'argc-demo' environment activated, you can start a Jupyter server in the same terminal or command prompt window using either of the following commands:

`jupyter notebook` - or - `jupyter lab`

Keep in mind JupyterLab is a newer, more feature-rich IDE as compared to the older Jupyter Notebook. You can choose either!

At this point, you're all set 🔥😍🖥️

## Documentation links
 - <a href="https://pandas.pydata.org/docs/index.html">Pandas (spatial data analysis)</a>
 - <a href="https://geopandas.org/en/stable/">Geopandas (geospatial data analysis)</a>
 - <a href="https://selenium-python.readthedocs.io/index.html">Selenium (web browswer automation)</a>
 - <a href="https://pydeck.gl/">pydeck (Python mapping libarary)</a>
 - <a href="https://streamlit.io/">Streamlit (building Python web apps)</a>
