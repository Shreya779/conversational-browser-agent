import React, { useEffect, useRef } from 'react';
import Message from './Message';

const MessageList = ({ messages }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center max-w-md">
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl">🤖</span>
          </div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            Welcome to Browser Control Agent
          </h2>
          <p className="text-gray-600 mb-4">
            I can control web browsers through natural language. I'll demonstrate by helping you send emails through Gmail's web interface.
          </p>
          <div className="bg-blue-50 rounded-lg p-4 text-left">
            <p className="text-sm text-blue-800 font-medium mb-2">Try saying:</p>
            <ul className="text-sm text-blue-700 space-y-1">
              <li>• "I need to send an email"</li>
              <li>• "Send a leave application to my manager"</li>
              <li>• "Email my team about tomorrow's meeting"</li>
            </ul>
          </div>
          <div className="mt-4 p-3 bg-yellow-50 rounded-lg border border-yellow-200">
            <p className="text-xs text-yellow-800">
              <strong>Security Note:</strong> Only use test Gmail accounts for this demonstration.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((message) => (
        <Message key={message.id} message={message} />
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
