from cx_Freeze import setup, Executable

setup(
    name = "PasswordGenerator",
    version = "1.0",
    description = "Lab1",
    executables = [Executable("PasswordGenerator.py")]
)
