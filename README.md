
# NextflowForge: A Beginner-Friendly Nextflow Workflow Generator

Welcome to **NextflowForge**, an intuitive web-based tool designed to help you create Nextflow workflows without needing any prior experience. This app guides you step-by-step through setting up parameters, defining processes, and configuring environments for bioinformatics and other computational workflows.

## 📖 Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Setting Up the Environment](#setting-up-the-environment)
4. [Running the Application](#running-the-application)
5. [Contributing](#contributing)
6. [Issues](#issues)

## 📝 Introduction
NextflowForge is a Streamlit-based application that simplifies the process of creating Nextflow workflows. You can configure workflow parameters, define processes, manage environments, and set output configurations with just a few clicks.

## 🚀 Getting Started
To get the NextflowForge app running on your local machine, follow the steps below. These instructions are designed for absolute beginners, so no prior experience is needed!

### Prerequisites
- Make sure you have [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) installed on your system. If not, follow the instructions on the Conda website to install it.

## 🛠 Setting Up the Environment

To ensure that you have all the necessary packages and dependencies, we will use a `conda` environment. Follow the steps below:

### Step 1: Create a Conda Environment
Open your terminal (or Anaconda Prompt on Windows) and navigate to the directory where your project files are located. Use the following command to create a new Conda environment:

```bash
conda env create -f environment.yaml
```

This command will read the `environment.yaml` file and set up a new environment named `nextflowforge` with all the required dependencies.

### Step 2: Activate the Environment
Once the environment is created, activate it using the following command:

```bash
conda activate nextflowforge
```

### Step 3: Install Additional Dependencies (if needed)
If you need to install any additional Python packages, you can do so using:

```bash
pip install <package-name>
```

## 🎮 Running the Application

Now that the environment is set up, you can run the NextflowForge app using Streamlit:

1. Make sure you are in the correct directory where the `NextflowForge.py` file is located.
2. Run the following command:

```bash
streamlit run NextflowForge.py
```

3. A new browser window should open automatically. If not, open your web browser and navigate to the address displayed in the terminal (typically `http://localhost:8501`).

## 🤝 Contributing
If you want to contribute to the project, feel free to fork the repository and submit a pull request. Contributions, suggestions, and improvements are always welcome!

## 🐞 Issues
If you encounter any problems or have questions, please [raise an issue](https://github.com/your-repository-name/issues) in the GitHub repository. We are here to help!

Happy workflow building! ⚙️
