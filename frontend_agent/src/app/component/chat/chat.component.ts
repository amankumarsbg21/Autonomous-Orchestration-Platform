import { CommonModule } from '@angular/common';
import { AfterViewChecked, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { UIConversationMessage } from '../../models/chat.model';
import { ChatService } from '../../services/chat.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css'
})
export class ChatComponent implements OnInit, AfterViewChecked  {
  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;

  messages: UIConversationMessage[] = [];
  userMessage: string = '';
  threadId: string = '';
  isLoading: boolean = false;

  constructor(private chatService: ChatService) {}

  ngOnInit(): void {
    // Generate or restore a session thread_id
    this.threadId = this.getOrCreateThreadId();
    
    // Initial welcome message
    this.messages.push({
      sender: 'agent',
      text: 'Hello! I am your AI assistant. How can I help you today?',
      timestamp: new Date()
    });
  }

  ngAfterViewChecked(): void {
    this.scrollToBottom();
  }

  sendMessage(): void {
    const trimmedMessage = this.userMessage.trim();
    if (!trimmedMessage || this.isLoading) return;

    // 1. Append User Message
    this.messages.push({
      sender: 'user',
      text: trimmedMessage,
      timestamp: new Date()
    });

    const currentInput = trimmedMessage;
    this.userMessage = '';
    this.isLoading = true;

    // 2. Call Flask Backend Service
    this.chatService.sendMessage(currentInput, this.threadId).subscribe({
      next: (response) => {
        this.messages.push({
          sender: 'agent',
          text: response.response,
          timestamp: new Date()
        });
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Chat API Error:', err);
        this.messages.push({
          sender: 'agent',
          text: 'Sorry, something went wrong processing your request. Please try again.',
          timestamp: new Date()
        });
        this.isLoading = false;
      }
    });
  }

  startNewSession(): void {
    this.threadId = 'session_' + Math.random().toString(36).substring(2, 9);
    localStorage.setItem('chat_thread_id', this.threadId);
    this.messages = [{
      sender: 'agent',
      text: 'New chat session started. What would you like to explore?',
      timestamp: new Date()
    }];
  }

  private getOrCreateThreadId(): string {
    let savedId = localStorage.getItem('chat_thread_id');
    if (!savedId) {
      savedId = 'session_' + Math.random().toString(36).substring(2, 9);
      localStorage.setItem('chat_thread_id', savedId);
    }
    return savedId;
  }

  private scrollToBottom(): void {
    try {
      this.scrollContainer.nativeElement.scrollTop = this.scrollContainer.nativeElement.scrollHeight;
    } catch (err) {}
  }


}


