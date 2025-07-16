import { useState, useEffect, useRef, useCallback } from 'react';

const useWebSocket = (sessionId) => {
  const [messages, setMessages] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('Disconnected');
  const [isAutomationRunning, setIsAutomationRunning] = useState(false);
  const ws = useRef(null);

  const connect = useCallback(() => {
    if (!sessionId) return;

    const wsUrl = `ws://localhost:8000/api/ws/${sessionId}`;
    ws.current = new WebSocket(wsUrl);

    ws.current.onopen = () => {
      setConnectionStatus('Connected');
      console.log('WebSocket connected');
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('Received message:', data);

      // Add message to chat
      const newMessage = {
        id: Date.now() + Math.random(),
        timestamp: Date.now(),
        ...data
      };

      setMessages(prev => [...prev, newMessage]);

      // Update automation status
      if (data.type === 'status' || data.type === 'action') {
        setIsAutomationRunning(true);
      } else if (data.type === 'completion' || data.type === 'error') {
        setIsAutomationRunning(false);
      }
    };

    ws.current.onclose = () => {
      setConnectionStatus('Disconnected');
      setIsAutomationRunning(false);
      console.log('WebSocket disconnected');
    };

    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      setConnectionStatus('Error');
    };
  }, [sessionId]);

  const disconnect = useCallback(() => {
    if (ws.current) {
      ws.current.close();
    }
  }, []);

  const sendMessage = useCallback((message) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
      
      // Add user message to chat immediately
      if (message.type === 'user_message') {
        const userMessage = {
          id: Date.now() + Math.random(),
          type: 'user_message',
          content: message.content,
          timestamp: Date.now()
        };
        setMessages(prev => [...prev, userMessage]);
      }
    }
  }, []);

  const stopAutomation = useCallback(() => {
    sendMessage({ type: 'stop_automation' });
    setIsAutomationRunning(false);
  }, [sendMessage]);

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return {
    messages,
    connectionStatus,
    isAutomationRunning,
    sendMessage,
    stopAutomation,
    connect,
    disconnect
  };
};

export default useWebSocket;
