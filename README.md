# ARGC Demo

## Description

Welcome to the GitHub page for Will Wright's ARGC presentation on open source tools for geospatial viz! The demo will walk through how to use Python to create a Streamlit web application for visualizing home sales in Forsyth County.

## Install virtual environment

We will be using several packages for today's demonstration on open source tools in Python.

An easy way to install all the required packages is by using a Python distribution such as Anaconda or Miniconda. In this demo, we will utilize a conda environment to create a contained "sandbox" that is ready to use for the included Jupyter file.

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

You are now ready to code along 😍

## Documentation links
 - <a href="https://pandas.pydata.org/docs/index.html" target="_blank">Pandas</a>
 - <a href="https://www.w3schools.com/" target="_blank">Visit W3Schools!</a>
 - Geopandas (geospatial data analysis)
 - Selenium (web browswer automation)
 - Streamlit (building Python web apps)
 - pydeck (Python mapping libarary)
