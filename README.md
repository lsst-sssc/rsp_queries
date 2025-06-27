# rsp_queries

Example SSSC github module, initially for getting interns started with 
github, making Solat System-focused queries with the Rubin Science 
Platform and introduction to unit tests (via `pytest`). Will grow into 
a more generally useful module over time.

## Installation

1. Checkout out the code to somewhere suitable e.g. `~/git/`:
   - `cd ~/git/`
   - `git clone https://github.com/lsst-sssc/rsp_queries`
2. Create a virtual enviroment using e.g. `conda create --name <myenv>` or `python -m venv <myenv>`
3. Activate with `conda active <myenv>` or `source <myenv>/bin/activate` (or `<myenv>/Scripts/activate` on Windows)
4. Install an editable (in-place) development version of rsp_queries. This will allow you to run the code from the source directory. If you just want the source code installed so edits in the source code are automatically installed:
```
pip install -e .
```
If you are going to be editing documentation or modifying unit tests, it is best to install the full development version:
```
pip install -e '.[dev]'
```
