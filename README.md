# WebSenseAI Backend(server)
## Getting Started
This document contains certain information to get you acquainted with the backend of WebSenseAI
## Structure
The server is powered by Python Flask library. All the files and classes for the server resides under the folder `app`.
## Dependency Management: Poetry
The dependencies are managed by PyPoetry. Below are commonly used command for poetry:
- `$ poetry init` : Creates a virtual environment in the current directory.
- `$ poetry shell` : Activates the virtual environment, only works if the command is called in the current directory.
- `$ poetry add {dependency}` : Adds one or more depencies to the *pyproject.toml*, the upgrade of requirements.txt.
- `$ poetry install` : Installs or updates all the depedencies listed in *pyproject.toml*.
- `$ poetry lock` : Saves the versions of all the dependencies to prevent others to install incorrect versions.
- `$ poetry show` : Lists all the installed dependencies along with their version, equivalent of `pip freeze`.

**Notes**:

- Whenever a folder (directory) contains `pyproject.toml` file, poetry assumes that the directory must have a virtual environment

## Starting the server
1. Activate the virtual environment using `$ poetry shell`.
2. Start the server using `flask --app main run`
3. In your browser, navigate to `http://localhost:5000`.