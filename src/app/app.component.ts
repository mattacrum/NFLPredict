import { Component } from '@angular/core';
import { FormControl } from "@angular/forms";
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

export interface Team {
  name: string;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],

})
export class AppComponent {
  title = 'app';

  selectedHomeTeam: string;
  selectedAwayTeam: string;
  winner: string;

  homeScore: number;
  awayScore: number;

  articles: JSON;
  homeNews : Array<any>;
  awayNews : Array<any>;

  percentageConfidence: string;

  nflData: JSON;

  constructor(private httpClient: HttpClient, private newsApi : ApiService) {
  }

  ngOnInit() {
    this.newsApi.getNews().subscribe(data => this.articles = data['articles'] as JSON);

  }

  teams: Team[] = [
    {name: "Arizona Cardinals"},
    {name: "Atlanta Falcons"},
    {name: "Buffalo Bills"},
    {name: "Baltimore Ravens"},
    {name: "Carolina Panthers"},
    {name: "Cincinnati Bengals"},
    {name: "Cleveland Browns"},
    {name: "Chicago Bears"},
    {name: "Dallas Cowboys"},
    {name: "Denver Broncos"},
    {name: "Detroit Lions"},
    {name: "Green Bay Packers"},
    {name: "Houston Texans"},
    {name: "Indianapolis Colts"},
    {name: "Kansas City Chiefs"},
    {name: "Los Angeles Chargers"},
    {name: "Los Angeles Rams"},
    {name: "Jacksonville Jaguars"},
    {name: "Miami Dolphins"},
    {name: "Minnesota Vikings"},
    {name: "New England Patriots"},
    {name: "New Orleans Saints"},
    {name: "New York Giants"},
    {name: "New York Jets"},
    {name: "Las Vegas Raiders"},
    {name: "Philadelphia Eagles"},
    {name: "San Francisco 49ers"},
    {name: "Seattle Seahawks"},
    {name: "Pittsburgh Steelers"},
    {name: "Tampa Bay Buccaneers"},
    {name: "Tennessee Titans"},
    {name: "Washington Football Team"}
  ];

  getAllNFLData(selectedHomeTeam, selectedAwayTeam) {
      document.body.style.backgroundColor = "#F2EE2B";
// Stat data from local API
      this.httpClient.get('http://127.0.0.1:5002/nfl_teams').subscribe(data => {
      this.nflData = data as JSON;

      var homeTeam;
      var awayTeam;

// Get data for selected teams
      for (var team in this.nflData)
      {
        if (selectedHomeTeam != selectedAwayTeam)
        {
          if (selectedHomeTeam == this.nflData[team]['team_name'])
          {
              homeTeam = this.nflData[team];
          }
          if (selectedAwayTeam == this.nflData[team]['team_name'])
          {
              awayTeam = this.nflData[team];
          }
        }
      }
// Get news articles for each selected team

      var homeNews = new Array();
      var awayNews = new Array();

      var home = selectedHomeTeam.split(" ", 3);
      var away = selectedAwayTeam.split(" ", 3);

      for ( var article in this.articles )
      {
        if (this.articles[article]['content'] != null)
        {
          if (this.articles[article]['content'].includes(home[home.length-1]))
          {
            homeNews.push(this.articles[article]);
          }
          if (this.articles[article]['content'].includes(away[away.length-1]))
          {
            awayNews.push(this.articles[article]);
          }
        }
      }
      this.homeNews = homeNews;
      this.awayNews = awayNews;
      console.log(homeNews)
// Change values from strings to floats
      for (var stat in homeTeam)
      {
        if(Number(homeTeam[stat]))
        {
          homeTeam[stat] = Number(homeTeam[stat])
        }
      }

      for (var stat in awayTeam)
      {
        if(Number(awayTeam[stat]))
        {
          awayTeam[stat] = Number(awayTeam[stat])
        }
      }

// Find winner    TODO: Adjust Algorithm
      this.homeScore = 0.5;
      this.awayScore = 0;

      for (stat in homeTeam)
      {
        if (stat != 'team_name')
        {
          if (stat == 'Opp_PointsPerGame')
          {
            if (awayTeam[stat] < homeTeam[stat])
            {
              this.awayScore = this.awayScore + 1;
            }
            else
            {
              this.homeScore = this.homeScore + 1;
            }
          }
          else
          {
            if (awayTeam[stat] > homeTeam[stat])
            {
              this.awayScore = this.awayScore + 1;
            }
            else
            {
              this.homeScore = this.homeScore + 1;
            }
          }
        }
      }
      console.log((homeTeam['PointsPerGame'] - awayTeam['Opp_PointsPerGame']))
      console.log((awayTeam['PointsPerGame'] - homeTeam['Opp_PointsPerGame']))
      if ((homeTeam['PointsPerGame'] - awayTeam['Opp_PointsPerGame']) >
          (awayTeam['PointsPerGame'] - homeTeam['Opp_PointsPerGame']))
      {
        this.homeScore = this.homeScore + 1;
      }
      else
      {
        this.awayScore = this.awayScore + 1;
      }
        console.log(this.homeScore)
        console.log(this.awayScore)
        if (this.homeScore >= this.awayScore)
        {
          this.winner = homeTeam['team_name'];
          this.percentageConfidence = ((this.homeScore-0.5) / 6 * 100 - 1).toFixed(2) + '% Confidence';
        }
        else
        {
          this.winner = awayTeam['team_name'];
          this.percentageConfidence = (this.awayScore / 6 * 100 - 1).toFixed(2) + '% Confindence';
        }

        console.log(this.winner);
      })
  }


}
