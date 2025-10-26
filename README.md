# fantasy-bball-espn-api

## usage
* set `constants.ESPN_LEAGUE_ID` to your ESPN League ID
  * this must be a public league
* set `constants.YEAR` to the value representing the current season
  * `2025` is the 2024-2025 season
* set `constants.MY_TEAM` to your team name appended with the its abbreviation in parentheses, ex. "Big Baller Brand (BBb)"
 * set `MY_ESPN_S2` and `SWID`. help: https://github.com/cwendt94/espn-api/discussions/150

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

## library usage notes

* [black](https://pypi.org/project/black/) for formatting
  ```
  $ black .
  ```
* [flake8](https://pypi.org/project/flake8/) for linting
  ```
  $ flake8 --ignore=E501 -v .
  ```
  * [E501](https://www.flake8rules.com/rules/E501.html)
* [ruff](https://pypi.org/project/ruff/) for linting
  ```
  $ ruff check
  ```
* [coverage](https://pypi.org/project/coverage/) for code coverage
  ```
  $ coverage run -m unittest
  $ coverage report -m
  ```

## reference(s)
* [style](https://peps.python.org/pep-0008)
