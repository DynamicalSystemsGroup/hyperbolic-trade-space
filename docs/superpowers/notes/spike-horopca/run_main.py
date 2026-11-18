"""Run the authors' ``main.py`` (their own CLI) under the shim: python run_main.py <clone> [main.py args]."""
import runpy, sys
clone = sys.argv[1]
sys.path.insert(0, clone)
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import compat; compat.install()
sys.argv = [clone + "/main.py"] + sys.argv[2:]
runpy.run_path(clone + "/main.py", run_name="__main__")
