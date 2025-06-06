# Data Processing Project – Formula 1

## Prerequisites

- Python 3.x installed

## Installation

### 1. Download and extract the `F1_wc.zip` archive

- Download the archive to the **Desktop** OR the **Documents** folder  
- Right-click the archive > **Extract All**

> ⚠️ Make sure to choose **Desktop** or **Documents** as the extraction location if you are a beginner and cannot adapt the next steps to the repertory you chose.

You should end up with a folder named `F1_wc` directly on the Desktop or at the root of the Documents folder, containing all project files and subfolders.

### 2. Navigate to the project root

Open **Git Bash** or **cmd**:

```bash
cd Desktop/Groupe55_PTD  # if extracted on the Desktop
cd Documents/Groupe55_PTD # if extracted in the Documents folder
```

### 3. Create the virtual environment

From the project root, run:

```bash
python -m venv env
```

### 4. Activate the virtual environment

```bash
source env/Scripts/activate  # for Git Bash on Windows
source env/bin/activate      # for Mac/Linux
.\env\Scripts\activate       # for Windows (cmd or PowerShell)
```

### 5. Install the dependencies

Install the required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Running the Graphical Interface

Once the installation is complete, launch the GUI from the project root:

```bash
python -m src
```

The user interface will open. It is intuitive to use.

## Deleting the Virtual Environment

If needed, delete the virtual environment:

**On Windows (cmd/PowerShell):**
```bash
rmdir /s /q env
```

**On Git Bash (Windows), Mac, or Linux:**
```bash
rm -rf env
```

This will completely remove the `env/` folder and its contents.
