# fantasy-bball-espn-api

## usage
* set `constants.ESPN_LEAGUE_ID` to your ESPN League ID
  * this must be a public league
* set `constants.YEAR` to the value representing the current season
  * `2025` is the 2024-2025 season

## setup
* [basic setup steps](https://github.com/keepitsimpledev/dev-env/blob/main/python/README.md)
* [pipenv](https://pipenv.pypa.io/) usage reminder (using `black` as an example):
  ```
  $ pip -V # can be used to check virtual env
  $ pipenv shell
  $ pip -V # confirm virtual env has changed
  $ black ./..
  $ pipenv exit
  ```
* in VS code, select path to virtual environment as python interpreter (in the bottom right)
  * example: /home/`<CURRENT_USER>`/.local/share/virtualenvs/fantasy-bball-espn-api-h4zGGGrD/bin/python

## notes
linters used:
* [flake8](https://pypi.org/project/flake8/)
* [ruff](https://pypi.org/project/ruff/)

## reference(s)
* [style](https://peps.python.org/pep-0008)
