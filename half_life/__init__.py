import sys

MEIPASS = sys._MEIPASS if hasattr(sys, '_MEIPASS') else None
RESOURCE_PATH = MEIPASS or '.'
