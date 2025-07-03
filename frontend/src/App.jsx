import React, { useState } from 'react';
import { ThemeProvider, ChatProvider } from './contexts';
import { Sidebar } from './components/sidebar';
import { ChatContainer, InputArea } from './components/chat';
import { useApiMessage } from './hooks';
import { QUICK_ACTIONS } from './constants';

const AggieNavigator = () => {
  const [sidebarExpanded, setSidebarExpanded] = useState(true);
  const { sendMessage } = useApiMessage();

  const handleQuickAction = (actionTitle) => {
    const action = QUICK_ACTIONS.find(a => a.title === actionTitle);
    const message = action ? action.message : actionTitle;
    sendMessage(message);
  };

  return (
    <div className="h-screen flex bg-background text-foreground">
      <Sidebar
        isExpanded={sidebarExpanded}
        onToggle={() => setSidebarExpanded(!sidebarExpanded)}
      />

      <main className="flex-1 flex flex-col min-h-0 relative">
        {/* Main Chat Area */}
        <ChatContainer onQuickAction={handleQuickAction} />

        {/* Input Area */}
        <InputArea onSendMessage={sendMessage} disabled={false} />
      </main>
    </div>
  );
};

const App = () => {
  return (
    <ThemeProvider>
      <ChatProvider>
        <AggieNavigator />
      </ChatProvider>
    </ThemeProvider>
  );
};

export default App;