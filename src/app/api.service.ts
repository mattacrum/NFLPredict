import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  API_KEY = '18427b3925f74384aad650eedbb2b716';

  constructor(private http: HttpClient) { }
// Return nfl news from news api
  getNews(){
    var today = new Date();
    var lastWeek = new Date();

    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    var temp = today.getDate() - 7;
    lastWeek.setDate(temp);
    var _today = yyyy + '-' + mm + '-' + dd;

    var dd = String(lastWeek.getDate()).padStart(2, '0');
    var mm = String(lastWeek.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = lastWeek.getFullYear();

    var _lastWeek = yyyy + '-' + mm + '-' + dd;

    return this.http.get('https://newsapi.org/v2/everything?id=nfl-news&q=nfl&from='+_lastWeek+'&to='+_today+'&sortBy=popularity&apiKey='+this.API_KEY);
  }

}
