import subprocess
import sys
from pathlib import Path

py_exec = str(sys.executable)
# Get lib directory
lib = Path(py_exec).parent.parent / "lib"
# Ensure pip is installed
subprocess.call([py_exec, "-m", "ensurepip", "--user" ])
# Update pip (not mandatory)
subprocess.call([py_exec, "-m", "pip", "install", "--upgrade", "pip" ])
# Install packages
subprocess.call([py_exec,"-m", "pip", "install", f"--target={str(lib)}", "Pillow"])
subprocess.call([py_exec,"-m", "pip", "install", f"--target={str(lib)}", "PyYAML"])