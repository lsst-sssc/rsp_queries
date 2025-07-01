# rsp_queries

Example SSSC github module, initially for getting interns started with 
github, making Solat System-focused queries with the Rubin Science 
Platform (RSP) and introduction to unit tests (via `pytest`). Will grow into 
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

## External TAP access

While it is strongly recommended to run queries in the Notebook aspect within the RSP, there can be use cases where the user wants to access Rubin data from outside the RSP. The procedure for doing this is as follows:

### Create token

(This only needs to be done once per user)

1. Obtain an access token from the RSP (tokens generated prior to DP1 are no longer valid/were wiped) by clicking on `Security tokens` under your login name in the top right as shown in the screenshot below:
![Screenshot of the Rubin Science Platform showing the location of the Security tokens entry in the top right of the screen under the users' name](/docs/rsp_frontpage_scrnshot.png)
2. Click on the `Create Token` button, provide a name for your token such as `rsp_READ` and make sure to tick the `read:image` and `read:tap` options, leave the `Expires` option at `Never` and then click `Create`
![Screenshot of the token creation dialog box showing the read:image and read:tap options are selected](/docs/rsp_create_token.png)
3. Make a copy of the generated token (should begin with `gt-`) and store it in a safe place as there is no way to see it again (you would need to delete and recreate it again if you lose it)
4. _Make sure that you don't commit the token to any git repositories..._

### Use the token

In order to use the token to access the RSP externally, two environment variables need to be set before launching the IPython shell or Jupyter notebook. For `bash` shells (Linux, MacOS X, Cygwin etc):
```
export ACCESS_TOKEN="<your token from above>"
export EXTERNAL_INSTANCE_URL="https://data.lsst.cloud/"
```
and for PowerShell (Windows):
```
$env:ACCESS_TOKEN="<your token from above>"
$env:EXTERNAL_INSTANCE_URL="https://data.lsst.cloud/"
```

(`EXTERNAL_INSTANCE_URL` sets the prefix for all the TAP services in `lsst.rsp` and is prefered to the RSP documentation instructions to set `EXTERNAL_TAP_URL` as that was only for the TAP service and this would need to be repeated (but wasn't documented) for SSOTAP, ObsLocTAP etc; with `EXTERNAL_INSTANCE_URL`, only one variable needs to be set. This is less applicable now with DP1 compared to DP0.2/0.3)
