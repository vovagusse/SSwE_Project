import sys
import os
from pathlib import Path
p = os.path.abspath('../..')
sys.path.insert(0, p)
# sys.path.insert(0, str(Path('..', 'src').resolve()))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Магазин программных средств'
copyright = '2025, Алымов А.О., Левданская Н.А., Ковалёв Н.Д., Гончаров А.А.'
author = 'Алымов А.О., Левданская Н.А., Ковалёв Н.Д., Гончаров А.А.'
release = 'хз'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc"
]

templates_path = ['_templates']
exclude_patterns = []

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
