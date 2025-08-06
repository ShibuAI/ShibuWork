export interface FileValidationResponse {
  isValid: boolean;
  data?: any[];
  exceptions?: ValidationException[];
  summary?: string;
}

export interface ValidationException {
  id: string;
  row: number;
  column: string;
  message: string;
  severity: 'error' | 'warning';
  details?: string;
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'system' | 'error' | 'success';
  message: string;
  timestamp: Date;
  relatedExceptionId?: string;
}

export interface GridData {
  columns: string[];
  rows: any[];
  totalRecords: number;
}

export interface PaginationConfig {
  page: number;
  pageSize: number;
  totalRecords: number;
}