# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "xnoapi"
copyright = "2025, xnoproject"
author = "xnoproject"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_rtd_theme",
    "sphinx.ext.todo",
    "sphinx.ext.githubpages",
]

todo_include_todos = True

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "navigation_depth": 4,
}
html_static_path = ["_static"]


def setup(app):
    app.add_js_file("no_autocollapse.js")


import os
import sys

sys.path.insert(0, os.path.abspath(".."))


# -- Options for LaTeX/PDF output --------------------------------------------
# https://www.sphinx-doc.org/en/master/latex.html

# Dùng xelatex để hỗ trợ Unicode (tiếng Việt)
latex_engine = "xelatex"

latex_elements = {
    "babel": r"\usepackage[vietnamese]{babel}",  # giữ nguyên babel
    "preamble": r"""
\usepackage{fontspec}

% Font chính
\setmainfont{Times New Roman}
\setsansfont{Arial}
\setmonofont{Courier New}

% Font emoji (Windows: Segoe UI Emoji, Linux: Noto Color Emoji, macOS: Apple Color Emoji)
\newfontfamily\emoji{Segoe UI Emoji}
\newcommand{\emoj}[1]{{\emoji #1}}
""",
}
