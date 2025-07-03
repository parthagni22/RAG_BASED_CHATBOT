import React from 'react';
import { Zap } from 'lucide-react';

const TypingIndicator = () => (
  <div className="flex items-start gap-4 mb-6">
    <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center shadow-md">
      <Zap className="w-5 h-5 text-primary-foreground" />
    </div>
    <div className="bg-card border border-border rounded-2xl rounded-tl-md px-6 py-4 shadow-sm">
      <div className="flex items-center space-x-2">
        <span className="text-sm text-muted-foreground">Aggie is thinking</span>
        <div className="flex space-x-1">
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              className="w-2 h-2 bg-primary rounded-full animate-bounce"
              style={{ animationDelay: `${i * 0.2}s` }}
            />
          ))}
        </div>
      </div>
    </div>
  </div>
);

export default TypingIndicator;