import React, { useRef, useEffect } from 'react';
// FIXED: Import from hooks, not contexts
import { useChat } from '../../hooks/useChat.js';
import Message from './Message.jsx';
import TypingIndicator from './TypingIndicator.jsx';
import WelcomeMessage from './WelcomeMessage.jsx';

const ChatContainer = ({ onQuickAction }) => {
  const { getCurrentMessages, isTyping } = useChat();
  const messages = getCurrentMessages();
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  return (
    <div className="flex-1 overflow-y-auto bg-background">
      <div className="min-h-full px-6 py-8">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center min-h-full">
            <WelcomeMessage onQuickAction={onQuickAction} />
          </div>
        ) : (
          <div className="max-w-4xl mx-auto">
            {messages.map((msg) => (
              <Message
                key={msg.id}
                message={msg.message}
                type={msg.type}
                timestamp={msg.timestamp}
              />
            ))}
            {isTyping && <TypingIndicator />}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ChatContainer;