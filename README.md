# ARGC Python Demo
## Description
Welcome to the GitHub page for Will Wright's ARGC presentation on open source tools for geospatial viz! The demo will walk through how to use Python to create a Streamlit web application for visualizing home sales in Forsyth County.

## Package Installation
We will be using several packages for today's ARGC demonstration on open source tools in Python.

An easy way to install all the required packages is by using a Python distribution such as Anaconda or Miniconda. In this demo, we will utilize a conda environment to create a contained sandbox that is ready to use for the included Jupyter file.

If you don't have a Python distribution installed locally, please download and install one first. Next, open a terminal or command prompt and navigate to the directory where you cloned this repository. Then, create a new conda environment (which will automatically include all necessary packages) by using the following command:

`conda env create -f environment.yml`

This process may take 10-15 minutes to complete, depending on the speed of your network connection. Once the environment is created, you need to activate it. Use the following command in your terminal or command prompt:

`conda activate argc-demo`

With the environment activated, you can start a Jupyter server in the same terminal or command prompt window using either of the following commands:

`jupyter notebook` - or - `jupyter lab`

Keep in mind JupyterLab is a newer, more feature-rich IDE as compared to the older Jupyter Notebook. You can choose either!

You are now ready to code along 😍
