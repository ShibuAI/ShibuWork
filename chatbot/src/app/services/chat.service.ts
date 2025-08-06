import { Injectable, signal, computed, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { ChatMessage } from '../shared/models/file-data.model';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private readonly http = inject(HttpClient);
  private readonly API_BASE = 'http://localhost:3000/api';
  
  // Using Angular 19 signals
  private messagesSignal = signal<ChatMessage[]>([]);
private newMessageNotificationSubject = new Subject<void>();
  // Computed signals for derived state
  messages = computed(() => this.messagesSignal());
  messageCount = computed(() => this.messagesSignal().length);
  lastMessage = computed(() => {
    const messages = this.messagesSignal();
    return messages[messages.length - 1] || null;
  });
 // Observable for new message notifications
  newMessageNotification$ = this.newMessageNotificationSubject.asObservable();
  getMessages(): ChatMessage[] {
    return this.messagesSignal();
  }

  addMessage(message: Omit<ChatMessage, 'id' | 'timestamp'>): void {
    const newMessage: ChatMessage = {
      ...message,
      id: this.generateId(),
      timestamp: new Date()
    };

    this.messagesSignal.update(messages => [...messages, newMessage]);
  }

  addSystemMessage(message: string, type: 'success' | 'error' = 'success'): void {
    this.addMessage({
      type: type === 'success' ? 'system' : 'error',
      message
    });
  }

  sendUserMessage(message: string): Observable<any> {
    // Add user message
    this.addMessage({
      type: 'user',
      message
    });

    // Simulate AI response (replace with actual API call)
    return new Observable(observer => {
      setTimeout(() => {
        this.addMessage({
          type: 'system',
          message: this.generateAIResponse(message)
        });
        observer.next({ success: true });
        observer.complete();
      }, 1000);
    });
  }

  clearMessages(): void {
    this.messagesSignal.set([]);
  }

  private generateId(): string {
    return Math.random().toString(36).substr(2, 9);
  }

  private generateAIResponse(userMessage: string): string {
    const message = userMessage.toLowerCase();
    
    if (message.includes('error') || message.includes('invalid')) {
      return 'I can help you understand the validation errors. The most common issues are missing required columns, invalid data formats, or duplicate entries.';
    } else if (message.includes('file') || message.includes('upload')) {
      return 'File processing involves validating structure, checking data types, and ensuring required fields are present. Would you like me to explain any specific validation rules?';
    } else {
      return 'I\'m here to help with file processing questions. You can ask about validation errors, data formats, or any issues you\'re experiencing.';
    }
  }
}