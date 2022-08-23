# This project is a test automation for WEHAGO mobile application.

To run the project a user has to install [Poetry](https://python-poetry.org/).

---

## Before RUN

1. **JAVA** installed.
2. **npm** and **nodejs** installed.
3. Run **[Appium Desktop](https://github.com/appium/appium-desktop)** server.
4. Install **[Allure Framwork](https://github.com/allure-framework/allure2)**. It can be installed using **[scoop](https://scoop.sh/)** package manager.
5. Run **android emulator** (`emulator -avd {emaltor name}` or **Virtual Device Manager** from Android Studio).


## Run


- `poetry shell` - activate virtual environment.
- `poetry install` - install dependencies.
- `poetry run pytest --alluredir="../allure-report" /tests/test-mobile-automation.py` - run the tests. Or run from IDE run configuration with additional arguments: `--alluredir="../allure-report"`. 
- `deactivate` - to deactivate virtual environment.


## Allure report server

Run `allure serve {path to project}/allure-report` to activate allure report server.