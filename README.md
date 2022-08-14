# This project is a test automation for WEHAGO mobile application.

To run the project a user has to install [Poetry](https://python-poetry.org/).

---

## Before RUN

<ul>
    <li><strong>JAVA</strong> installed.</li>
    <li><strong>npm</strong> and <strong>nodejs</strong> installed.</li>
    <li>Run <strong>Appium Desktop</strong> server.</li>
    <li>Run <strong>android emulator</strong> (<code>emulator -avd {emaltor name}</code> or <strong>Virtual Device Manager</strong> from Android Studio).</li>
</ul>


## Run

<ol>
    <li><code>poetry shell</code> - activate virtual environment.</li>
    <li><code>poetry install</code> - install dependencies.</li>
    <li><code>poetry run alluredir</code> - crerate allure report directory</li>
    <li><code>poetry build</code> - build the project.</li>
    <li><code>poetry run pytest --alluredir="../Allure" /tests/test-mobile-automation.py</code> - run the tests.
    <br> (Or run from IDE run configuration with additional arguments: <code>--alluredir="../Allure"</code>).</li>
    <li><code>deactivate</code> - to deactivate virtual environment.</li>
</ol>

## Allure report server

Run <code>allure serve {path to project}/Allure</code> to activate allure report server.