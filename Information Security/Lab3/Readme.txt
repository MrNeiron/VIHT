������ �� �����: https://www.youtube.com/watch?v=P5woBSmbs3I
������ �� ������: https://pythonworld.ru/osnovy/program-compilation-with-cx-freeze.html

��� ������ ��� ����� ���������� wheel, ����� ��������� ������ Windows

pip install wheel

����� ���������, ��� ���� 

http://www.lfd.uci.edu/~gohlke/pythonlibs/#cx_freeze

� ��������� ������ ��� ������ cx_Freeze - ������ �� ���������� ������� � ������ Python.

������ ���� ������ ����� ����������� - �� ����� ���������� .whl. ��� �� ��� ����������?

����� ������ - ���������� ��������� ���� � ������ ����� D, ����� ����� ��������� ���� �� ����. ����� �������� � ��������� ������ Windows, � �������� �������

pip install D:\cx_Freeze-5.0.1-cp36-cp36m-win32.whl

������ ����� ����� whl ���������� ��� �������.

��� ������� ��������� cx_Freeze �� ��� ���������.

������ � �������� � ���������� ������� ����� �������������� �������� ���� "setup.py", � ����� ����������

from cx_Freeze import setup, Executable

setup(
    name = "Freelance",
    version = "1.0",
    description = "Freelance Parser",
    executables = [Executable("free.py")]
)

����� ������ free.py ����� �������� ��� ������ ������� �� ������ ������� �� ������������.

������� � ��������� ������ � ������� � ����� �������� ����� ������� 

python.exe setup.py build

� ����� �������� ����� ������� build, � �������, ����� ���� ����������� ��� ������ ��������� �� ���������� ������������ exe-���� free.exe
