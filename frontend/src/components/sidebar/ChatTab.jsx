import React, { useState } from 'react';
import { MessageCircle, Trash2, Edit2, Check, X } from 'lucide-react';

const ChatTab = ({ chat, isActive, onSelect, onDelete, onRename, canDelete, isExpanded, index }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editName, setEditName] = useState(chat.name);

  const handleDelete = (e) => {
    e.stopPropagation();
    if (window.confirm('Delete this chat?')) {
      onDelete(chat.id);
    }
  };

  const handleRename = (e) => {
    e.stopPropagation();
    setIsEditing(true);
    setEditName(chat.name);
  };

  const handleSaveRename = (e) => {
    e.stopPropagation();
    if (editName.trim()) {
      onRename(chat.id, editName.trim());
    }
    setIsEditing(false);
  };

  const handleCancelRename = (e) => {
    e.stopPropagation();
    setEditName(chat.name);
    setIsEditing(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSaveRename(e);
    } else if (e.key === 'Escape') {
      handleCancelRename(e);
    }
  };

  // For collapsed view, show only first 4 chats as small dots
  if (!isExpanded) {
    if (index >= 4) return null;

    return (
      <div
        onClick={() => onSelect(chat.id)}
        className={`w-10 h-10 mx-auto rounded-lg cursor-pointer transition-all duration-200 flex items-center justify-center ${isActive
          ? 'bg-primary shadow-md'
          : 'bg-muted hover:bg-muted/80'
          }`}
        title={chat.name}
      >
        <MessageCircle className={`w-4 h-4 ${isActive ? 'text-primary-foreground' : 'text-muted-foreground'
          }`} />
      </div>
    );
  }

  // Expanded view
  return (
    <div
      onClick={() => !isEditing && onSelect(chat.id)}
      className={`group flex items-center gap-3 p-3 mx-2 rounded-xl cursor-pointer transition-all duration-200 ${isActive
        ? 'bg-primary text-primary-foreground shadow-md'
        : 'hover:bg-muted text-foreground hover:shadow-sm'
        }`}
    >
      <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${isActive ? 'bg-primary-foreground/20' : 'bg-muted'
        }`}>
        <MessageCircle className={`w-4 h-4 ${isActive ? 'text-primary-foreground' : 'text-muted-foreground'
          }`} />
      </div>

      <div className="flex-1 min-w-0">
        {isEditing ? (
          <div className="flex items-center gap-2">
            <input
              type="text"
              value={editName}
              onChange={(e) => setEditName(e.target.value)}
              onKeyDown={handleKeyDown}
              className="flex-1 px-2 py-1 text-sm bg-background border border-border rounded focus:outline-none focus:ring-1 focus:ring-primary"
              autoFocus
              onClick={(e) => e.stopPropagation()}
            />
            <button
              onClick={handleSaveRename}
              className="p-1 hover:bg-green-500 hover:text-white rounded transition-colors"
            >
              <Check className="w-3 h-3" />
            </button>
            <button
              onClick={handleCancelRename}
              className="p-1 hover:bg-red-500 hover:text-white rounded transition-colors"
            >
              <X className="w-3 h-3" />
            </button>
          </div>
        ) : (
          <div className="flex items-center justify-between">
            <span className="font-medium truncate text-sm">
              {chat.name}
            </span>
            {chat.messages.length > 0 && (
              <span className={`text-xs ml-2 ${isActive ? 'text-primary-foreground/70' : 'text-muted-foreground'
                }`}>
                {chat.messages.length}
              </span>
            )}
          </div>
        )}

        {!isEditing && chat.messages.length > 0 && (
          <p className={`text-xs truncate mt-1 ${isActive ? 'text-primary-foreground/70' : 'text-muted-foreground'
            }`}>
            {chat.messages[chat.messages.length - 1].message}
          </p>
        )}
      </div>

      {!isEditing && (
        <div className="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            onClick={handleRename}
            className={`p-1.5 rounded-md transition-colors ${isActive
              ? 'hover:bg-primary-foreground/20'
              : 'hover:bg-accent hover:text-accent-foreground'
              }`}
            title="Rename chat"
          >
            <Edit2 className="w-3.5 h-3.5" />
          </button>
          {canDelete && (
            <button
              onClick={handleDelete}
              className={`p-1.5 rounded-md transition-colors ${isActive
                ? 'hover:bg-primary-foreground/20'
                : 'hover:bg-destructive hover:text-destructive-foreground'
                }`}
              title="Delete chat"
            >
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default ChatTab;