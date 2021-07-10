# Project --------------------------------------------------------------

project = "Hamlet Python Executor"
copyright = "2021 Hamlet"
author = "Hamlet"

# General --------------------------------------------------------------

master_doc = "index"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx_click"
]
autodoc_typehints = "description"
intersphinx_mapping = {"python": ("https://docs.python.org/3/", None)}
