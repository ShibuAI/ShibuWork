import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { FileValidationResponse } from '../shared/models/file-data.model';

@Injectable({
  providedIn: 'root'
})
export class FileProcessorService {
  private readonly http = inject(HttpClient);
  private readonly API_BASE = 'http://localhost:3000/api';

  validateFile(file: File): Observable<FileValidationResponse> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post<FileValidationResponse>(`${this.API_BASE}/validate_file`, formData)
      .pipe(
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An unexpected error occurred';
    
    if (error.error instanceof ErrorEvent) {
      errorMessage = `Client Error: ${error.error.message}`;
    } else {
      errorMessage = `Server Error: ${error.status} - ${error.message}`;
    }
    
    return throwError(() => errorMessage);
  }
}
