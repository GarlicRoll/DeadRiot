import cx_Freeze
import sys

executables = [cx_Freeze.Executable("DeadRiot.py")]
sys.argv.append("build")
cx_Freeze.setup(
    name="DeadRiot",
    options={"build.exe": {"packages":["pygame"]}},
    executables = executables)
