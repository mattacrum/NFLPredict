# NFLPedict

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 10.1.7.

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

Prediction data:
Team Win/Loss record
Team Win/ Loss record vs Opponent
Number of starters injured
Percentage of offensive line healthy
Matchup statistics
Average score
Turnover margin
Field position
Weather

const axios = require('axios')
const cheerio = require('cheerio')

async function fetchHTML(url) {
const { data } = await axios.get(url)
return cheerio.load(data)
}
const $ = await fetchHTML("https://www.teamrankings.com/nfl/stat/turnover-margin-per-game")

console.log(`Site HTML: ${$.html()}\n\n`)
