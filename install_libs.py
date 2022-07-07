import subprocess
import bpy

py_exec = bpy.app.binary_path_python
# ensure pip is installed & update
subprocess.call([str(py_exec), "-m", "ensurepip", "--user"])
subprocess.call([str(py_exec), "-m", "pip", "install", "--upgrade", "pip"])
# install dependencies using pip
# dependencies such as 'numpy' could be added to the end of this command's list
subprocess.call([str(py_exec),"-m", "pip", "install", "--user", "Pillow"])
subprocess.call([str(py_exec),"-m", "pip", "install", "--user", "PyYAML"])