import g4f
from g4f.gui import run_gui

g4f.debug.logging = True  # Enable debug logging
g4f.debug.version_check = False  # Disable automatic version checking
g4f.debug.version = "0.3.1.7"

from g4f.api import run_api

run_api()