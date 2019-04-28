from cx_Freeze import setup, Executable
import os
import shutil as sh

exeFile = "GUI_DB.py"
databaseFile = "AliasDatabases.txt"

setup(
    name = "Freelance",
    version = "1.0",
    description = "Freelance Parser",
    executables = [Executable(exeFile)]
)

sh.copy(databaseFile, os.path.join("build", os.listdir("build")[0], databaseFile))
            