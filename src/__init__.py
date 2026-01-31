import sys
from pathlib import Path

# Add project root path to syspath, to solve the import problem
sys.path.append(Path(__file__).parent.parent.resolve().as_posix())

__version__ = "0.2.0(dev)"
