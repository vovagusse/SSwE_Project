# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
# from pathlib import Path
# p = os.path.abspath('../..')
sys.path.insert(0, os.path.abspath("../../"))                     #Those two lines do
sys.path.insert(0, os.path.abspath("../../software_shop_webapp")) #Some Fucking Magic


project = 'Сервис онлайн оплаты ПС'
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


'''Установленные темы:
furo [pip install furo]
sphinx_rtd_theme [pip install sphinx-rtd-theme]
alabaster [скачана по умолчанию вместе с Sphinx]
sphinx_book_theme [pip install sphinx-book-theme]
'''
html_theme = 'sphinx_book_theme'
html_static_path = ['_static']