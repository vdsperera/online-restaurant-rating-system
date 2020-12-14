import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler,
         HttpEvent, HttpErrorResponse} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators'


@Injectable({
  providedIn: 'root'
})
export class IntercepterService {

  constructor() { }

  intercept(req: HttpRequest<any>, next: HttpHandler):Observable<HttpEvent<any>>
  {
  	console.log("PLC intercept");
  	return next.handle(req)
  	.pipe(catchError(this.handleError))
  }

  handleError(error : HttpErrorResponse)
  {
  	console.log("PLC Hanndle Error");
  	console.log(error.error.detail);
  	// window.alert(error.error.detail);
    return throwError(error);
  }

} 
