import { useState } from 'react';
import { sendMessageToAPI } from '../utils';
import { useChat } from './useChat.js';  // ← From local hooks directory

export const useApiMessage = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const { addMessage, setIsTyping } = useChat();

  const sendMessage = async (message) => {
    setIsLoading(true);
    setError(null);
    addMessage(message, 'user');
    setIsTyping(true);

    try {
      const data = await sendMessageToAPI(message);
      addMessage(data.message, 'bot');
    } catch (err) {
      console.error('Error fetching LLM response:', err);
      setError(err.message);
      addMessage('Sorry, I encountered an error. Please try again.', 'bot');
    } finally {
      setIsLoading(false);
      setIsTyping(false);
    }
  };

  return { sendMessage, isLoading, error };
};