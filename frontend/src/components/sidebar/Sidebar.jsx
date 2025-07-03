import React from 'react';
import {
  Book,
  Menu,
  Sun,
  Moon,
  Plus,
  Settings,
  HelpCircle,
  ChevronLeft,
  ChevronRight,
  Download,
  Upload,
  Trash2
} from 'lucide-react';
import { useTheme } from '../../hooks/useTheme.js';
import { useChat } from '../../hooks/useChat.js';
import ChatTab from './ChatTab.jsx';

const Sidebar = ({ isExpanded, onToggle }) => {
  const { isDark, toggleTheme, mounted } = useTheme();
  const {
    chats,
    currentChatId,
    setCurrentChatId,
    createNewChat,
    deleteChat,
    renameChat,
    clearAllChats,
    exportChats,
    importChats
  } = useChat();

  const handleImportChats = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = (e) => {
      const file = e.target.files[0];
      if (file) {
        importChats(file);
      }
    };
    input.click();
  };

  const handleClearAllChats = () => {
    if (window.confirm('Are you sure you want to delete all chats? This action cannot be undone.')) {
      clearAllChats();
    }
  };

  if (!mounted) {
    return (
      <aside className={`${isExpanded ? 'w-80' : 'w-16'} transition-all duration-300 bg-card border-r border-border flex flex-col`}>
        <div className="animate-pulse p-4">
          <div className="h-8 bg-muted rounded"></div>
        </div>
      </aside>
    );
  }

  return (
    <aside className={`${isExpanded ? 'w-80' : 'w-16'} transition-all duration-300 bg-card border-r border-border flex flex-col shadow-lg`}>
      {/* Header */}
      <div className={`flex items-center ${isExpanded ? 'justify-between p-4' : 'justify-center p-3'} border-b border-border`}>
        {isExpanded ? (
          <>
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center shadow-md">
                <Book className="w-5 h-5 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-lg font-bold text-foreground">Aggie Navigator</h1>
                <p className="text-xs text-muted-foreground">Course Assistant</p>
              </div>
            </div>
            <button
              onClick={onToggle}
              className="p-2 rounded-lg hover:bg-muted transition-colors"
              title="Collapse sidebar"
            >
              <ChevronLeft className="w-4 h-4 text-muted-foreground" />
            </button>
          </>
        ) : (
          <div className="flex flex-col items-center space-y-2">
            <button
              onClick={onToggle}
              className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center shadow-md hover:shadow-lg transition-all"
              title="Expand sidebar"
            >
              <Book className="w-5 h-5 text-primary-foreground" />
            </button>
          </div>
        )}
      </div>

      {/* New Chat Button */}
      <div className={`${isExpanded ? 'p-4' : 'p-2'}`}>
        <button
          onClick={createNewChat}
          className={`${isExpanded
              ? 'w-full flex items-center gap-3 p-3'
              : 'w-12 h-12 flex items-center justify-center mx-auto'
            } bg-primary text-primary-foreground rounded-xl hover:bg-primary/90 transition-colors shadow-md hover:shadow-lg`}
          title="New Chat"
        >
          <Plus className="w-5 h-5" />
          {isExpanded && <span className="font-medium">New Chat</span>}
        </button>
      </div>

      {/* Chat List */}
      <div className="flex-1 overflow-y-auto pb-4">
        {isExpanded && chats.length > 0 && (
          <div className="px-4 mb-2 flex items-center justify-between">
            <h3 className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
              Recent Chats ({chats.length})
            </h3>
            <div className="flex items-center space-x-1">
              <button
                onClick={exportChats}
                className="p-1 hover:bg-muted rounded transition-colors"
                title="Export chats"
              >
                <Download className="w-3 h-3 text-muted-foreground" />
              </button>
              <button
                onClick={handleImportChats}
                className="p-1 hover:bg-muted rounded transition-colors"
                title="Import chats"
              >
                <Upload className="w-3 h-3 text-muted-foreground" />
              </button>
              <button
                onClick={handleClearAllChats}
                className="p-1 hover:bg-destructive hover:text-destructive-foreground rounded transition-colors"
                title="Clear all chats"
              >
                <Trash2 className="w-3 h-3 text-muted-foreground" />
              </button>
            </div>
          </div>
        )}

        <div className={`${isExpanded ? 'space-y-1' : 'space-y-2 px-2'}`}>
          {chats.map((chat, index) => (
            <ChatTab
              key={chat.id}
              chat={chat}
              isActive={currentChatId === chat.id}
              onSelect={setCurrentChatId}
              onDelete={deleteChat}
              onRename={renameChat}
              canDelete={chats.length > 1}
              isExpanded={isExpanded}
              index={index}
            />
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className={`border-t border-border ${isExpanded ? 'p-4 space-y-2' : 'p-2 space-y-3'}`}>
        {isExpanded ? (
          <>
            <button className="w-full flex items-center gap-3 p-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg transition-colors">
              <Settings className="w-4 h-4" />
              <span className="text-sm">Settings</span>
            </button>
            <button className="w-full flex items-center gap-3 p-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg transition-colors">
              <HelpCircle className="w-4 h-4" />
              <span className="text-sm">Help & Support</span>
            </button>
            <button
              onClick={toggleTheme}
              className="w-full flex items-center gap-3 p-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg transition-colors"
              title={`Switch to ${isDark ? 'light' : 'dark'} mode`}
            >
              {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
              <span className="text-sm">{isDark ? 'Light Mode' : 'Dark Mode'}</span>
            </button>
          </>
        ) : (
          <div className="flex flex-col items-center space-y-3">
            <button
              className="w-10 h-10 flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg transition-colors"
              title="Settings"
            >
              <Settings className="w-4 h-4" />
            </button>
            <button
              className="w-10 h-10 flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg transition-colors"
              title="Help & Support"
            >
              <HelpCircle className="w-4 h-4" />
            </button>
            <button
              onClick={toggleTheme}
              className="w-10 h-10 flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg transition-colors"
              title={`Switch to ${isDark ? 'light' : 'dark'} mode`}
            >
              {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>
          </div>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;