import sys

MEIPASS = sys._MEIPASS if hasattr(sys, '_MEIPASS') else None
RESOURCE_PATH = MEIPASS or '.'

__author__ = 'Noel Kaczmarek'
__copyright__ = '© 2021 Noel Kaczmarek'
__credits__ = ['Noel Kaczmarek']
__license__ = 'GNU GPLv3'
__version__ = '1.1.0'
__maintainer__ = 'Noel Kaczmarek'
__email__ = 'noel@kaczmarek.eu'
__status__ = 'Production'
