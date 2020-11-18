import { Component } from '@angular/core';
import { FormControl } from "@angular/forms";
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

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

  nflData: JSON;

  constructor(private httpClient: HttpClient) {
  }

  ngOnInit() {
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

      console.log(homeTeam);
      console.log(awayTeam);

// Find winner    TODO: Adjust Algorithm
      this.homeScore = 0;
      this.awayScore = 0;

      for (stat in homeTeam)
        if (stat == 'opp_td_drive')
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
        console.log(this.homeScore)
        console.log(this.awayScore)
        if (this.homeScore >= this.awayScore)
          this.winner = homeTeam['team_name'];
        else
          this.winner = awayTeam['team_name'];
        console.log(this.winner);
      })
  }
}
