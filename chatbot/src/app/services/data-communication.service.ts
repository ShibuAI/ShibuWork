import { Injectable, signal } from '@angular/core';
import { effect } from '@angular/core';
import { FileValidationResponse, ValidationException } from '../shared/models/file-data.model';

@Injectable({
  providedIn: 'root'
})
export class DataCommunicationService {
  // Using signals for reactive state management
  private exceptionClickedSignal = signal<ValidationException | null>(null);
  private fileProcessedSignal = signal<FileValidationResponse | null>(null);

  // Public readonly signals
  exceptionClicked = this.exceptionClickedSignal.asReadonly();
  fileProcessed = this.fileProcessedSignal.asReadonly();

  notifyExceptionClicked(exception: ValidationException): void {
    this.exceptionClickedSignal.set(exception);
  }

  notifyFileProcessed(response: FileValidationResponse): void {
    this.fileProcessedSignal.set(response);
  }

  clearExceptionClicked(): void {
    this.exceptionClickedSignal.set(null);
  }
}
