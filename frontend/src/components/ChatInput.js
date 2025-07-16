import React, { useState } from 'react';
import { Send, Square } from 'lucide-react';

const ChatInput = ({ onSendMessage, disabled, isAutomationRunning, onStopAutomation }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="border-t bg-white p-4">
      <form onSubmit={handleSubmit} className="flex items-end space-x-3">
        <div className="flex-1">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={
              disabled 
                ? "Automation in progress..."
                : "Type your message... (e.g., 'I need to send an email')"
            }
            disabled={disabled}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            rows="1"
            style={{ minHeight: '44px', maxHeight: '120px' }}
          />
        </div>
        
        {isAutomationRunning ? (
          <button
            type="button"
            onClick={onStopAutomation}
            className="bg-red-500 hover:bg-red-600 text-white p-2 rounded-lg transition-colors flex items-center justify-center"
            style={{ minWidth: '44px', height: '44px' }}
          >
            <Square size={20} />
          </button>
        ) : (
          <button
            type="submit"
            disabled={disabled || !input.trim()}
            className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white p-2 rounded-lg transition-colors flex items-center justify-center"
            style={{ minWidth: '44px', height: '44px' }}
          >
            <Send size={20} />
          </button>
        )}
      </form>
      
      {isAutomationRunning && (
        <div className="mt-2 text-sm text-orange-600 text-center">
          🤖 Browser automation in progress... Click stop button to cancel
        </div>
      )}
    </div>
  );
};

export default ChatInput;
