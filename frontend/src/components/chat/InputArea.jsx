import React, { useState, useRef, useEffect } from 'react';
import { Send, Paperclip, Mic, Smile } from 'lucide-react';

const InputArea = ({ onSendMessage, disabled }) => {
  const [message, setMessage] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const textareaRef = useRef(null);

  const handleSubmit = () => {
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }
  };

  useEffect(() => {
    adjustTextareaHeight();
  }, [message]);

  return (
    <div className="flex-shrink-0 bg-background border-t border-border px-6 py-6">
      <div className="max-w-4xl mx-auto">
        <div className={`bg-card border-2 rounded-2xl shadow-lg transition-all duration-200 ${
          isFocused ? 'border-primary shadow-xl' : 'border-border'
        }`}>
          <div className="flex items-end p-4 gap-3">
            {/* Action Buttons Left */}
            <div className="flex items-center space-x-1">
              <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg transition-colors">
                <Paperclip className="w-5 h-5" />
              </button>
            </div>

            {/* Text Input */}
            <div className="flex-1 relative">
              <textarea
                ref={textareaRef}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                onFocus={() => setIsFocused(true)}
                onBlur={() => setIsFocused(false)}
                placeholder="Ask about courses, prerequisites, or degree requirements..."
                className="w-full resize-none border-0 bg-transparent text-foreground placeholder-muted-foreground focus:outline-none text-sm leading-6 max-h-32"
                rows={1}
                disabled={disabled}
              />
            </div>

            {/* Action Buttons Right */}
            <div className="flex items-center space-x-1">
              <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg transition-colors">
                <Smile className="w-5 h-5" />
              </button>
              <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg transition-colors">
                <Mic className="w-5 h-5" />
              </button>
              <button
                onClick={handleSubmit}
                disabled={disabled || !message.trim()}
                className={`p-2.5 rounded-xl transition-all duration-200 ${
                  message.trim() && !disabled
                    ? 'bg-primary text-primary-foreground shadow-md hover:shadow-lg hover:scale-105'
                    : 'bg-muted text-muted-foreground cursor-not-allowed'
                }`}
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        {/* Helper Text */}
        <div className="flex items-center justify-between mt-3 px-2">
          <span className="text-xs text-muted-foreground">
            Press Enter to send • Shift+Enter for new line
          </span>
          <span className="text-xs text-muted-foreground">
            {message.length}/2000
          </span>
        </div>
      </div>
    </div>
  );
};

export default InputArea;