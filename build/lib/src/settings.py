"""Global settings for whole project

This file will store the configuration shared and used by project.
Variable defined here could be upload to configuration centre like apollo for distribution 
"""
import os


BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


os.makedirs(os.path.join(BASE, 'data'), exist_ok=True)
DB_PATH = os.path.join(BASE, 'data/', 'snapshot.rdb')

