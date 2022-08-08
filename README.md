# NFLPedict

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 10.1.7.

# How it works

## Python
Python is the language responsible for most of the backend functionality of the app. The program 'get_NFL_stats.py' obtains nfl stats from different websites through web scraping using the BeautifulSoup python library and saves the data to a csv file.  The file 'api.py' runs an API server using Flask and provides the data in the csv to the web server.

## Angular
HTML, CSS, and Typscript were used in an Angular environment to create mostly the front end functionality of the app.
Upon initialization, Angular's HttpClient module in 'api.service.ts' sends a GET request to the 'www.newsapi.org' API to obtain news articles for NFL teams that may help determine the outcome of a game.
The user will select a home team and an away team from the GUI and hit the "Predict Winner" button. This will trigger the HttpClient module to send a GET request to our API server (api.py) to retrieve stats for each selected team and select a winner based on the algorithm in the getAllNFLData() function in 'app.component.ts'. The predicted winner, percentage confidence, and news articles for each team will then be displayed.

## Run program to get data from websites
Run 'python get_NFL_stats.py' to web scrape the nfl data from different websites into a cvs file.

## Run API server
Run 'python apy.pi' for the API server.

## Run Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).

# Notes
