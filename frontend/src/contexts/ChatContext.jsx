import React, { createContext, useState, useEffect } from 'react';
import { generateChatId } from '../utils';

export const ChatContext = createContext();

const STORAGE_KEY = 'aggie-navigator-chats';

export const ChatProvider = ({ children }) => {
  const [chats, setChats] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);
  const [isTyping, setIsTyping] = useState(false);

  // Load chats from localStorage on mount
  useEffect(() => {
    const savedChats = localStorage.getItem(STORAGE_KEY);
    if (savedChats) {
      try {
        const parsedChats = JSON.parse(savedChats);
        if (parsedChats.length > 0) {
          setChats(parsedChats);
          setCurrentChatId(parsedChats[0].id);
          return;
        }
      } catch (error) {
        console.error('Error loading chats from localStorage:', error);
      }
    }
    // Create first chat if none exist
    createNewChat();
  }, []);

  // Save chats to localStorage whenever chats change
  useEffect(() => {
    if (chats.length > 0) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(chats));
    }
  }, [chats]);

  const createNewChat = () => {
    const newChatId = generateChatId();
    const chatNumber = chats.length + 1;
    const newChat = {
      id: newChatId,
      name: `Chat ${chatNumber}`,
      messages: [],
      createdAt: Date.now(),
      updatedAt: Date.now()
    };

    setChats(prev => [...prev, newChat]);
    setCurrentChatId(newChatId);
  };

  const deleteChat = (chatId) => {
    if (chats.length <= 1) return;

    const updatedChats = chats.filter(chat => chat.id !== chatId);
    setChats(updatedChats);

    if (currentChatId === chatId) {
      setCurrentChatId(updatedChats[0]?.id || null);
    }
  };

  const renameChat = (chatId, newName) => {
    setChats(prev => prev.map(chat =>
      chat.id === chatId
        ? { ...chat, name: newName.trim() || chat.name, updatedAt: Date.now() }
        : chat
    ));
  };

  const addMessage = (message, type) => {
    const newMessage = {
      id: generateChatId(),
      message,
      type,
      timestamp: Date.now()
    };

    setChats(prev => prev.map(chat =>
      chat.id === currentChatId
        ? {
          ...chat,
          messages: [...chat.messages, newMessage],
          updatedAt: Date.now(),
          // Auto-rename chat based on first user message
          name: chat.messages.length === 0 && type === 'user'
            ? message.slice(0, 50) + (message.length > 50 ? '...' : '')
            : chat.name
        }
        : chat
    ));
  };

  const clearAllChats = () => {
    localStorage.removeItem(STORAGE_KEY);
    setChats([]);
    setCurrentChatId(null);
    createNewChat();
  };

  const exportChats = () => {
    const dataStr = JSON.stringify(chats, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `aggie-chats-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const importChats = (file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const importedChats = JSON.parse(e.target.result);
        if (Array.isArray(importedChats)) {
          setChats(importedChats);
          if (importedChats.length > 0) {
            setCurrentChatId(importedChats[0].id);
          }
        }
      } catch (error) {
        console.error('Error importing chats:', error);
        alert('Error importing chats. Please check the file format.');
      }
    };
    reader.readAsText(file);
  };

  const getCurrentChat = () => chats.find(chat => chat.id === currentChatId);
  const getCurrentMessages = () => getCurrentChat()?.messages || [];

  const contextValue = {
    chats,
    currentChatId,
    isTyping,
    setCurrentChatId,
    setIsTyping,
    createNewChat,
    deleteChat,
    renameChat,
    addMessage,
    clearAllChats,
    exportChats,
    importChats,
    getCurrentChat,
    getCurrentMessages
  };

  return (
    <ChatContext.Provider value={contextValue}>
      {children}
    </ChatContext.Provider>
  );
};