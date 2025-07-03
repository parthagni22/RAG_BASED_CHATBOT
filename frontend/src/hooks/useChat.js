import { useContext } from 'react';
import { ChatContext } from '../contexts/ChatContext.jsx';

export function useChat() {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within ChatProvider');
  }
  return context;
}