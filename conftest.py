import sys
import os

# Add root directory to sys.path so src module can be resolved during testing
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
