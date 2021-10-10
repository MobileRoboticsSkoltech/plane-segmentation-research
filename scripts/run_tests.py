import subprocess
import os
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
TESTS = ROOT / "tests"

python_path = os.getenv("PYTHONPATH")

if python_path is None:
    os.environ["PYTHONPATH"] = str(ROOT)
else:
    os.environ["PYTHONPATH"] += ";" + str(ROOT)

subprocess.check_call(["python", "-m", "py.test", "-vv", "-s", TESTS])
