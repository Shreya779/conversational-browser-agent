import React from 'react';
import { Activity, Wifi, WifiOff, AlertCircle } from 'lucide-react';

const StatusBar = ({ connectionStatus, isAutomationRunning }) => {
  const getStatusIcon = () => {
    switch (connectionStatus) {
      case 'Connected':
        return <Wifi size={16} className="text-green-500" />;
      case 'Disconnected':
        return <WifiOff size={16} className="text-red-500" />;
      case 'Error':
        return <AlertCircle size={16} className="text-red-500" />;
      default:
        return <WifiOff size={16} className="text-gray-500" />;
    }
  };

  const getStatusColor = () => {
    switch (connectionStatus) {
      case 'Connected':
        return 'text-green-600';
      case 'Disconnected':
        return 'text-red-600';
      case 'Error':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="bg-gray-50 border-b px-4 py-2 flex items-center justify-between">
      <div className="flex items-center space-x-2">
        {getStatusIcon()}
        <span className={`text-sm font-medium ${getStatusColor()}`}>
          {connectionStatus}
        </span>
      </div>
      
      {isAutomationRunning && (
        <div className="flex items-center space-x-2">
          <Activity size={16} className="text-orange-500 animate-pulse" />
          <span className="text-sm font-medium text-orange-600">
            Browser Automation Active
          </span>
        </div>
      )}
    </div>
  );
};

export default StatusBar;
