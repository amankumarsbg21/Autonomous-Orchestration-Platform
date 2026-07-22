import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ChatRequest, ChatResponse } from '../models/chat.model';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private readonly apiUrl = 'http://localhost:5000/api/chat';

  constructor(private http: HttpClient) {}

  sendMessage(message: string, threadId: string): Observable<ChatResponse> {
    const payload: ChatRequest = {
      message: message,
      thread_id: threadId
    };

    return this.http.post<ChatResponse>(this.apiUrl, payload);
  }
}