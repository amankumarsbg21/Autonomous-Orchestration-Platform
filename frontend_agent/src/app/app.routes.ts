import { Routes } from '@angular/router';
import { ChatComponent } from './component/chat/chat.component';

export const routes: Routes = [
    { 
    path: 'chat', 
    component: ChatComponent 
  },
  { 
    path: '', 
    redirectTo: '/chat', 
    pathMatch: 'full' // Redirects the root URL (localhost:4200/) to /chat
  },
  { 
    path: '**', 
    redirectTo: '/chat' // Catch-all for any unknown URLs
  }
];
