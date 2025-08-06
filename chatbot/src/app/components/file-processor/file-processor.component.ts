import { Component, signal, inject, DestroyRef, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FileValidationResponse } from '../../shared/models/file-data.model';
import { FileProcessorService } from '../../services/file-processor.service';
import { ChatService } from '../../services/chat.service';
import { DataCommunicationService } from '../../services/data-communication.service';

@Component({
 selector: 'app-file-processor',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './file-processor.component.html',
  styleUrl: './file-processor.component.css'
})
export class FileProcessorComponent  {
   @ViewChild('fileInput', { static: true }) fileInput!: ElementRef<HTMLInputElement>;

  // Angular 19 signals for reactive state
  selectedFile = signal<File | null>(null);
  isProcessing = signal(false);
  isDragOver = signal(false);
  validationResult = signal<FileValidationResponse | null>(null);

  // Dependency injection
  private fileProcessorService = inject(FileProcessorService);
  private chatService = inject(ChatService);
  private communicationService = inject(DataCommunicationService);
  private destroyRef = inject(DestroyRef);

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    this.isDragOver.set(true);
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    this.isDragOver.set(false);
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    this.isDragOver.set(false);
    
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.selectedFile.set(files[0]);
    }
  }

  onFileSelected(event: any): void {
    const files = event.target.files;
    if (files && files.length > 0) {
      this.selectedFile.set(files[0]);
    }
  }

  processFile(): void {
    const file = this.selectedFile();
    if (!file) return;

    this.isProcessing.set(true);
    this.validationResult.set(null);

    this.chatService.addSystemMessage(`Processing file: ${file.name}...`);

    this.fileProcessorService.validateFile(file)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          this.validationResult.set(response);
          this.isProcessing.set(false);
          
          if (response.isValid) {
            this.chatService.addSystemMessage(
              `✅ File processed successfully! Found ${response.data?.length || 0} valid records.`,
              'success'
            );
          } else {
            this.chatService.addSystemMessage(
              `⚠️ File processed with ${response.exceptions?.length || 0} validation issues.`,
              'error'
            );
          }

          this.communicationService.notifyFileProcessed(response);
        },
        error: (error) => {
          this.isProcessing.set(false);
          this.chatService.addSystemMessage(`❌ Error processing file: ${error}`, 'error');
        }
      });
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

   triggerFileInput(): void {
    console.log('Triggering file input');  // Debug log
    if (this.fileInput && this.fileInput.nativeElement) {
      this.fileInput.nativeElement.click();
    } else {
      console.error('File input element not found');
    }
  }
}
