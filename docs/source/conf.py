# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information



project = 'Сервис онлайн оплпты программных средств'
copyright = '2025, Алымов А.О., Левданская Н.А., Ковалёв Н.Д., Гончаров А.А.'
author = 'Алымов А.О., Левданская Н.А., Ковалёв Н.Д., Гончаров А.А.'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage"
]

templates_path = ['_templates']
exclude_patterns = []

language = 'ru_RU'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
