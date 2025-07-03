import React from 'react';
import { User, Zap, Copy, ThumbsUp, ThumbsDown } from 'lucide-react';
import { MessageFormatter } from '../../utils';

const Message = ({ message, type, timestamp }) => {
  const handleCopy = () => {
    navigator.clipboard.writeText(message);
  };

  if (type === 'user') {
    return (
      <div className="flex items-start gap-4 mb-6 justify-end">
        <div className="max-w-[80%]">
          <div className="bg-primary rounded-2xl rounded-tr-md px-6 py-4 shadow-md">
            <div className="text-primary-foreground font-medium">{message}</div>
            {timestamp && (
              <div className="text-primary-foreground/70 text-xs mt-2">
                {MessageFormatter.formatMessageTime(timestamp)}
              </div>
            )}
          </div>
        </div>
        <div className="w-10 h-10 bg-muted rounded-xl flex items-center justify-center shadow-sm">
          <User className="w-5 h-5 text-muted-foreground" />
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-start gap-4 mb-6">
      <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center shadow-md">
        <Zap className="w-5 h-5 text-primary-foreground" />
      </div>
      <div className="max-w-[85%] flex-1">
        <div className="bg-card border border-border rounded-2xl rounded-tl-md px-6 py-4 shadow-sm">
          <div
            className="text-foreground prose prose-sm max-w-none"
            dangerouslySetInnerHTML={{ __html: MessageFormatter.formatLLMResponse(message) }}
          />

          {/* Message Actions */}
          <div className="flex items-center justify-between mt-4 pt-3 border-t border-border">
            <div className="flex items-center space-x-2">
              <button
                onClick={handleCopy}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs text-muted-foreground hover:text-foreground bg-muted/50 hover:bg-muted rounded-lg transition-colors"
              >
                <Copy className="w-3 h-3" />
                Copy
              </button>
              <button className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs text-muted-foreground hover:text-green-600 bg-muted/50 hover:bg-green-50 dark:hover:bg-green-900/20 rounded-lg transition-colors">
                <ThumbsUp className="w-3 h-3" />
                Helpful
              </button>
              <button className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs text-muted-foreground hover:text-red-600 bg-muted/50 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors">
                <ThumbsDown className="w-3 h-3" />
                Not helpful
              </button>
            </div>
            {timestamp && (
              <div className="text-xs text-muted-foreground">
                {MessageFormatter.formatMessageTime(timestamp)}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Message;