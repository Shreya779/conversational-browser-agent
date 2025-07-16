import React from 'react';
import { Bot, User, Monitor, Camera, CheckCircle, XCircle, AlertCircle } from 'lucide-react';

const Message = ({ message }) => {
  const renderContent = () => {
    switch (message.type) {
      case 'user_message':
        return (
          <div className="flex items-start space-x-3 mb-4">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
              <User size={16} className="text-white" />
            </div>
            <div className="flex-1 bg-blue-50 rounded-lg p-3">
              <p className="text-gray-800">{message.content}</p>
            </div>
          </div>
        );

      case 'agent_message':
        return (
          <div className="flex items-start space-x-3 mb-4">
            <div className="flex-shrink-0 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
              <Bot size={16} className="text-white" />
            </div>
            <div className="flex-1 bg-white border rounded-lg p-3 shadow-sm">
              <p className="text-gray-800">{message.content}</p>
            </div>
          </div>
        );

      case 'status':
        return (
          <div className="flex items-start space-x-3 mb-4">
            <div className="flex-shrink-0 w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center">
              <Monitor size={16} className="text-white" />
            </div>
            <div className="flex-1 bg-orange-50 rounded-lg p-3 border-l-4 border-orange-400">
              <p className="text-orange-800 font-medium">{message.message}</p>
            </div>
          </div>
        );

      case 'action':
        return (
          <div className="mb-6">
            <div className="flex items-start space-x-3 mb-3">
              <div className="flex-shrink-0 w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                {message.success ? (
                  <CheckCircle size={16} className="text-white" />
                ) : (
                  <XCircle size={16} className="text-white" />
                )}
              </div>
              <div className={`flex-1 rounded-lg p-3 border-l-4 ${
                message.success 
                  ? 'bg-green-50 border-green-400' 
                  : 'bg-red-50 border-red-400'
              }`}>
                <p className={`font-medium ${
                  message.success ? 'text-green-800' : 'text-red-800'
                }`}>
                  {message.message}
                </p>
                
                {message.email_data && (
                  <div className="mt-2 p-2 bg-white rounded border text-sm">
                    <p><strong>To:</strong> {message.email_data.to}</p>
                    <p><strong>Subject:</strong> {message.email_data.subject}</p>
                    <p><strong>Body:</strong> {message.email_data.body}</p>
                  </div>
                )}
              </div>
            </div>
            
            {message.screenshot && (
              <div className="ml-11">
                <div className="bg-gray-100 rounded-lg p-3 border">
                  <div className="flex items-center space-x-2 mb-2">
                    <Camera size={16} className="text-gray-600" />
                    <span className="text-sm font-medium text-gray-700">
                      Browser Screenshot
                    </span>
                  </div>
                  <img
                    src={`data:image/png;base64,${message.screenshot}`}
                    alt="Browser screenshot"
                    className="w-full rounded border shadow-sm max-w-2xl"
                    style={{ maxHeight: '400px', objectFit: 'contain' }}
                  />
                </div>
              </div>
            )}
          </div>
        );

      case 'completion':
        return (
          <div className="mb-6">
            <div className="flex items-start space-x-3 mb-3">
              <div className="flex-shrink-0 w-8 h-8 bg-green-600 rounded-full flex items-center justify-center">
                <CheckCircle size={16} className="text-white" />
              </div>
              <div className="flex-1 bg-green-50 rounded-lg p-4 border-l-4 border-green-500">
                <p className="text-green-800 font-semibold">{message.message}</p>
              </div>
            </div>
            
            {message.screenshot && (
              <div className="ml-11">
                <div className="bg-gray-100 rounded-lg p-3 border">
                  <div className="flex items-center space-x-2 mb-2">
                    <Camera size={16} className="text-gray-600" />
                    <span className="text-sm font-medium text-gray-700">
                      Final Result
                    </span>
                  </div>
                  <img
                    src={`data:image/png;base64,${message.screenshot}`}
                    alt="Final browser screenshot"
                    className="w-full rounded border shadow-sm max-w-2xl"
                    style={{ maxHeight: '400px', objectFit: 'contain' }}
                  />
                </div>
              </div>
            )}
          </div>
        );

      case 'error':
        return (
          <div className="mb-6">
            <div className="flex items-start space-x-3 mb-3">
              <div className="flex-shrink-0 w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
                <AlertCircle size={16} className="text-white" />
              </div>
              <div className="flex-1 bg-red-50 rounded-lg p-3 border-l-4 border-red-400">
                <p className="text-red-800 font-medium">{message.message}</p>
              </div>
            </div>
            
            {message.screenshot && (
              <div className="ml-11">
                <div className="bg-gray-100 rounded-lg p-3 border">
                  <div className="flex items-center space-x-2 mb-2">
                    <Camera size={16} className="text-gray-600" />
                    <span className="text-sm font-medium text-gray-700">
                      Error State Screenshot
                    </span>
                  </div>
                  <img
                    src={`data:image/png;base64,${message.screenshot}`}
                    alt="Error state screenshot"
                    className="w-full rounded border shadow-sm max-w-2xl"
                    style={{ maxHeight: '400px', objectFit: 'contain' }}
                  />
                </div>
              </div>
            )}
          </div>
        );

      default:
        return (
          <div className="flex items-start space-x-3 mb-4">
            <div className="flex-shrink-0 w-8 h-8 bg-gray-500 rounded-full flex items-center justify-center">
              <Bot size={16} className="text-white" />
            </div>
            <div className="flex-1 bg-gray-50 rounded-lg p-3">
              <p className="text-gray-800">{JSON.stringify(message)}</p>
            </div>
          </div>
        );
    }
  };

  return renderContent();
};

export default Message;
