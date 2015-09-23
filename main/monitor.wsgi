import sys
import os
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path: sys.path.insert(0, current_dir) 
from flask_web import app as application
