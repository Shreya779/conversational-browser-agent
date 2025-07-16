import React from 'react';
import { Bot, Globe, Camera, Zap } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white border-b shadow-sm">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <Bot size={24} className="text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                Conversational Browser Control Agent
              </h1>
              <p className="text-sm text-gray-600">
                AI that controls browsers through natural language
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4 text-sm text-gray-600">
            <div className="flex items-center space-x-1">
              <Globe size={16} />
              <span>Real Browser</span>
            </div>
            <div className="flex items-center space-x-1">
              <Camera size={16} />
              <span>Live Screenshots</span>
            </div>
            <div className="flex items-center space-x-1">
              <Zap size={16} />
              <span>NO APIs</span>
            </div>
          </div>
        </div>
        
        <div className="mt-3 flex flex-wrap gap-2">
          <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium">
            ✅ Playwright Browser Automation
          </span>
          <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
            💬 Natural Language Interface
          </span>
          <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded-full text-xs font-medium">
            📸 Screenshots in Chat
          </span>
          <span className="px-2 py-1 bg-red-100 text-red-800 rounded-full text-xs font-medium">
            ❌ NO Gmail API
          </span>
        </div>
      </div>
    </header>
  );
};

export default Header;
