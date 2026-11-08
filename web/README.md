# Verzameling
Create lists for your collections. 
 
## Requirements
- Python 3.14
- [uv](https://docs.astral.sh/uv/) (installed at `~/.local/bin/uv`)

Dependencies are defined in `pyproject.toml`.

## Getting started
Run `start.bash`. It creates the `.venv` (using `uv sync`) with Python 3.14,
installs the dependencies and starts Gunicorn.

To add a dependency: `uv add <package>`.

## Deploy using a git hook
Check https://www.denick.org/post/08deploy/

Some extras I use on this project:
- Write the release version to the page footer
- Write the release version to the page footer and include a hyperlink to github
- Reload Gunicorn restart after the deploy

Check the hook [setup/git-hooks](setup/git-hooks)
