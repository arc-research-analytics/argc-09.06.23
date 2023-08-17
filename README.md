# ARGC - Q3 2023

## Installation
We will be using a number of packages for today's ARGC demonstration on open source tools in Python.

An easy way to install all required packages is to use a Python distribution such as Anaconda or Miniconda. In this demo, we will use a conda environment to build a contained sandbox that is ready to use for the included Jupyter notebook.

If you don't have a Python distribution downloaded locally, do so first. Then, open a terminal and navigate to the directory where you cloned this repo. Then, create a new conda enironment with all the necessary packages with the following shell command:

`conda env create -f environment.yml`

This may take 10-15 minutes to complete depending on the speed of your network connection.

Once created, you must activate the environment by using:

`conda activate argc-demo`

With this environment activated, you can spin up a Jupyter server on the same terminal window using either one of the following commands:

`jupyter notebook` - or - `jupyter lab`

Keep in mind JupyterLab is a newer, more feature-rich IDE as compared to the older Jupyter Notebook. Either can be used for the demo!

You are now ready to code along 😍
