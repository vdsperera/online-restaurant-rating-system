import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Restaurant } from './restaurant';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  API_URL = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) { }

  public get_restaurants(): Observable<Restaurant[]> {
    return this.http.get<Restaurant[]>(`${this.API_URL}/restaurants/`);
  }

  public register_restaurant(restaurant: Restaurant):Observable<Restaurant>
  {
  	console.log(this.http.post<Restaurant>(`${this.API_URL}/restaurants/`, restaurant));
  	return this.http.post<Restaurant>(`${this.API_URL}/restaurants/`, restaurant);
  }

  public register_restaurant2(data):Observable<any>
  {
    //console.log(this.http.post(`${this.API_URL}/restaurants/`, data));
    return this.http.post(`${this.API_URL}/restaurants/`, data);
  }  
  
}
