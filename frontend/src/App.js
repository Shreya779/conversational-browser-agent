import React, { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';

import Header from './components/Header';
import StatusBar from './components/StatusBar';
import MessageList from './components/MessageList';
import ChatInput from './components/ChatInput';
import useWebSocket from './hooks/useWebSocket';

import './App.css';

function App() {
  const [sessionId] = useState(() => uuidv4());
  const {
    messages,
    connectionStatus,
    isAutomationRunning,
    sendMessage,
    stopAutomation
  } = useWebSocket(sessionId);

  const handleSendMessage = (content) => {
    sendMessage({
      type: 'user_message',
      content: content
    });
  };

  const handleStopAutomation = () => {
    stopAutomation();
  };

  // Add welcome message when component mounts
  useEffect(() => {
    // Only add welcome message if no messages exist
    if (messages.length === 0) {
      // Small delay to ensure WebSocket is connected
      setTimeout(() => {
        if (connectionStatus === 'Connected') {
          const welcomeMessage = {
            id: 'welcome',
            type: 'agent_message',
            content: "Hello! I'm a conversational browser control agent. I can help you send emails by controlling a real web browser. Try saying something like 'I need to send an email' to get started!",
            timestamp: Date.now()
          };
          // Note: We don't add this to the WebSocket messages since it's just UI
        }
      }, 1000);
    }
  }, [connectionStatus, messages.length]);

  return (
    <div className="App h-screen flex flex-col bg-gray-50">
      <Header />
      <StatusBar 
        connectionStatus={connectionStatus}
        isAutomationRunning={isAutomationRunning}
      />
      
      <div className="flex-1 flex flex-col min-h-0">
        <MessageList messages={messages} />
        <ChatInput
          onSendMessage={handleSendMessage}
          disabled={isAutomationRunning}
          isAutomationRunning={isAutomationRunning}
          onStopAutomation={handleStopAutomation}
        />
      </div>
      
      {/* Footer with additional info */}
      <footer className="bg-white border-t px-4 py-2">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <div>
            Session ID: <span className="font-mono">{sessionId.substring(0, 8)}...</span>
          </div>
          <div className="flex items-center space-x-4">
            <span>🔗 WebSocket: {connectionStatus}</span>
            <span>🤖 Browser Automation: {isAutomationRunning ? 'Active' : 'Idle'}</span>
          </div>
          <div>
            Real browser control • No APIs • Live screenshots
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
