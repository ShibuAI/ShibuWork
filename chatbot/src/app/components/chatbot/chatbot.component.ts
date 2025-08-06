import { Component, signal, computed, inject, effect, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../../services/chat.service';
import { DataCommunicationService } from '../../services/data-communication.service';
import { ValidationException } from '../../shared/models/file-data.model';
@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrl: './chatbot.component.css'
})
export class ChatbotComponent implements AfterViewChecked {
  @ViewChild('messagesContainer') messagesContainer!: ElementRef;
  
  // Signals for reactive state
  currentMessage = signal('');
  isTyping = signal(false);
  shouldScrollToBottom = signal(false);

  // Injected services
  private chatService = inject(ChatService);
  private communicationService = inject(DataCommunicationService);

  // Computed signals from chat service
  messages = this.chatService.messages;

  constructor() {
    // Effect to watch for exception clicks from grid
    effect(() => {
      const exception = this.communicationService.exceptionClicked();
      if (exception) {
        this.handleExceptionClicked(exception);
        // Clear the exception after handling
        setTimeout(() => this.communicationService.clearExceptionClicked(), 100);
      }
    });

    // Effect to scroll when messages change
    effect(() => {
      // Access messages to make this effect reactive
      this.messages();
      // Schedule scroll after view update
      this.shouldScrollToBottom.set(true);
    });

    // Add welcome message
    this.chatService.addSystemMessage(
      'Hello! I\'m your AI assistant. I can help you understand file processing results, validation errors, and answer questions about your data.'
    );
  }

  ngAfterViewChecked(): void {
    if (this.shouldScrollToBottom()) {
      this.scrollToBottom();
      this.shouldScrollToBottom.set(false);
    }
  }

  sendMessage(): void {
    const message = this.currentMessage().trim();
    if (!message || this.isTyping()) return;

    this.isTyping.set(true);
    this.currentMessage.set('');

    this.chatService.sendUserMessage(message)
      .subscribe({
        next: () => {
          this.isTyping.set(false);
        },
        error: () => {
          this.isTyping.set(false);
          this.chatService.addSystemMessage('Sorry, I encountered an error. Please try again.', 'error');
        }
      });
  }

  clearChat(): void {
    this.chatService.clearMessages();
    this.chatService.addSystemMessage(
      'Chat cleared. How can I help you with your file processing?'
    );
  }

  handleExceptionClicked(exception: ValidationException): void {
    const message = `Exception details: Row ${exception.row}, Column "${exception.column}" - ${exception.message}`;
    this.chatService.addMessage({
      type: 'system',
      message: `🔍 ${message}`,
      relatedExceptionId: exception.id
    });

    // Generate contextual response
    setTimeout(() => {
      const response = this.generateExceptionResponse(exception);
      this.chatService.addSystemMessage(response);
    }, 500);
  }

  getMessageTypeLabel(type: string): string {
    switch (type) {
      case 'user': return 'You';
      case 'system': return 'Assistant';
      case 'error': return 'Error';
      default: return 'System';
    }
  }

  formatTime(date: Date): string {
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  }

  private scrollToBottom(): void {
    try {
      const container = this.messagesContainer.nativeElement;
      container.scrollTop = container.scrollHeight;
    } catch (err) {
      console.error('Error scrolling to bottom:', err);
    }
  }

  private generateExceptionResponse(exception: ValidationException): string {
    const responses = {
      error: [
        `This is a critical validation error that needs to be fixed before processing can continue.`,
        `To resolve this issue, please check the data format in row ${exception.row} for column "${exception.column}".`,
        `This error indicates a data quality issue that must be addressed.`
      ],
      warning: [
        `This is a warning that might affect data quality but won't stop processing.`,
        `You may want to review row ${exception.row} in column "${exception.column}" for potential improvements.`,
        `This warning suggests a data formatting inconsistency.`
      ]
    };

    const severityResponses = responses[exception.severity] || responses.error;
    const randomResponse = severityResponses[Math.floor(Math.random() * severityResponses.length)];
    
    return `${randomResponse} ${exception.details ? 'Additional details: ' + exception.details : ''}`;
  }
}