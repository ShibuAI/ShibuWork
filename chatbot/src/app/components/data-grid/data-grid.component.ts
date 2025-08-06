import { Component, signal, computed, inject, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FileValidationResponse, GridData, PaginationConfig, ValidationException } from '../../shared/models/file-data.model';
import { DataCommunicationService } from '../../services/data-communication.service';
@Component({
  selector: 'app-data-grid',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './data-grid.component.html',
  styleUrl: './data-grid.component.css'
})
export class DataGridComponent {
  // Signals for reactive state
  currentView = signal<'data' | 'exceptions'>('data');
  gridData = signal<GridData | null>(null);
  exceptions = signal<ValidationException[]>([]);
  pagination = signal<PaginationConfig>({
    page: 1,
    pageSize: 10,
    totalRecords: 0
  });

  // Computed signals for derived state
  totalPages = computed(() => 
    Math.ceil(this.pagination().totalRecords / this.pagination().pageSize)
  );

  paginatedData = computed(() => {
    const data = this.gridData();
    if (!data) return [];
    
    const pag = this.pagination();
    const start = (pag.page - 1) * pag.pageSize;
    const end = start + pag.pageSize;
    return data.rows.slice(start, end);
  });

  paginatedExceptions = computed(() => {
    const pag = this.pagination();
    const start = (pag.page - 1) * pag.pageSize;
    const end = start + pag.pageSize;
    return this.exceptions().slice(start, end);
  });

  // Dependency injection
  private communicationService = inject(DataCommunicationService);

  constructor() {
    // Effect to watch for file processing updates
    effect(() => {
      const response = this.communicationService.fileProcessed();
      if (response) {
        this.processFileResponse(response);
      }
    });
  }

  switchView(view: 'data' | 'exceptions'): void {
    this.currentView.set(view);
    this.pagination.update(pag => ({ ...pag, page: 1 })); // Reset pagination
  }

  processFileResponse(response: FileValidationResponse): void {
    if (response.data) {
      const columns = response.data.length > 0 ? Object.keys(response.data[0]) : [];
      this.gridData.set({
        columns,
        rows: response.data,
        totalRecords: response.data.length
      });
      this.pagination.update(pag => ({ ...pag, totalRecords: response.data!.length }));
    }

    this.exceptions.set(response.exceptions || []);
    
    // Switch to exceptions view if there are validation issues
    if (response.exceptions && response.exceptions.length > 0 && !response.isValid) {
      this.currentView.set('exceptions');
    }
  }

  selectException(exception: ValidationException): void {
    this.communicationService.notifyExceptionClicked(exception);
  }

  goToPage(page: number): void {
    const totalPages = this.totalPages();
    if (page >= 1 && page <= totalPages) {
      this.pagination.update(pag => ({ ...pag, page }));
    }
  }
}