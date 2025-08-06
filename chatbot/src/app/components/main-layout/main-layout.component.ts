import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FileProcessorComponent } from '../file-processor/file-processor.component';
import { DataGridComponent } from '../data-grid/data-grid.component';
import { ChatbotComponent } from '../chatbot/chatbot.component';
import { ChatService } from '../../services/chat.service';

@Component({
  selector: 'app-main-layout',
  standalone: true,
  imports: [
    CommonModule,
    FileProcessorComponent,
    DataGridComponent,
    ChatbotComponent
  ],
  templateUrl: './main-layout.component.html',
  styleUrl: './main-layout.component.css'
})
export class MainLayoutComponent {

  private chatService = inject(ChatService);

  // Signal for chatbot state
  isChatbotOpen = signal(false);
  hasNewMessages = signal(false);

  constructor() {
    // Listen for new message notifications
    this.chatService.newMessageNotification$.subscribe(() => {
      if (!this.isChatbotOpen()) {
        this.hasNewMessages.set(true);
      }
    });
  }

  toggleChatbot(): void {
    this.isChatbotOpen.update(isOpen => !isOpen);
    
    // Clear new message indicator when opening
    if (this.isChatbotOpen()) {
      this.hasNewMessages.set(false);
    }
  }
}
