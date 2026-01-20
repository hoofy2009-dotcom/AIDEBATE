import React, { useState, useEffect, useRef } from 'react'
import { Send, Bot, User, Play, Square } from 'lucide-react'
import { getBackendURL } from './config'

// Define types for our messages
interface Message {
  role: string
  name?: string
  content: string
  timestamp?: number
}

interface TypingStatus {
  agent: string
  status: boolean
}

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isConnected, setIsConnected] = useState(false)
  const [typingAgents, setTypingAgents] = useState<Set<string>>(new Set())
  const [rounds, setRounds] = useState(3) // 默认3轮
  const [currentRound, setCurrentRound] = useState(0) // 当前轮数
  const [isDebating, setIsDebating] = useState(false) // 是否正在辩论中
  const [summarizer, setSummarizer] = useState('deepseek-chat') // 总结者
  const [enableWebSearch, setEnableWebSearch] = useState(false) // 联网搜索开关
  
  const wsRef = useRef<WebSocket | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  
  // 可用的 AI 选项
  const availableAIs = [
    { id: 'deepseek-chat', name: 'DeepSeek', emoji: '🔷' },
    { id: 'qwen-turbo', name: 'Qwen (千问)', emoji: '🟣' },
    { id: 'doubao-pro-32k', name: 'Doubao (豆包)', emoji: '🟢' }
  ]

  useEffect(() => {
    // Scroll to bottom when messages change
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, typingAgents])

  const connectWebSocket = () => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return

    const backendURL = getBackendURL()
    const ws = new WebSocket(`${backendURL}/ws/debate`)
    
    ws.onopen = () => {
      console.log('Connected to WebSocket')
      setIsConnected(true)
      // Add system message
      setMessages(prev => [...prev, {
        role: 'system',
        content: 'Connected to AI Debate Platform. Start a topic to see agents debate!'
      }])
    }

    ws.onmessage = (event) => {
      const payload = JSON.parse(event.data)
      handleStreamMessage(payload)
    }

    ws.onclose = () => {
      console.log('Disconnected')
      setIsConnected(false)
      setMessages(prev => [...prev, {
        role: 'system',
        content: 'Disconnected from server.'
      }])
    }

    ws.onerror = (err) => {
      console.error('WebSocket error:', err)
    }

    wsRef.current = ws
  }

  useEffect(() => {
    connectWebSocket()
    return () => {
      wsRef.current?.close()
    }
  }, [])

  // Handle streaming updates
  const handleStreamMessage = (payload: any) => {
    if (payload.type === 'round_start') {
      setCurrentRound(payload.round)
      setIsDebating(true)
    } else if (payload.type === 'round_end') {
      // Round ended
    } else if (payload.type === 'debate_complete') {
      setIsDebating(false)
      setCurrentRound(0)
    } else if (payload.type === 'stream_start') {
      const msg = payload.data
      setMessages(prev => [...prev, { ...msg, isStreaming: true }])
    } else if (payload.type === 'stream_delta') {
      const { agent, delta } = payload
      setMessages(prev => {
        // Find last message from this agent
        const lastMsgIndex = prev.length - 1
        if (lastMsgIndex === -1) return prev
        const lastMsg = prev[lastMsgIndex]
        
        // Simple check: make sure we are updating the correct agent message. 
        // Since we process sequentially, the last message should be the one streaming.
        if (lastMsg.role === 'assistant' && lastMsg.name === agent) {
           const newMessages = [...prev]
           newMessages[lastMsgIndex] = {
             ...lastMsg,
             content: lastMsg.content + delta
           }
           return newMessages
        }
        return prev
      })
    } else if (payload.type === 'stream_end') {
       // Optional: Mark as finished styling
    } else if (payload.type === 'message') {
        const msg = payload.data
        setMessages(prev => [...prev, msg])
    } else if (payload.type === 'typing') {
        const { agent, status } = payload as TypingStatus
        setTypingAgents(prev => {
          const newSet = new Set(prev)
          if (status) {
            newSet.add(agent)
          } else {
            newSet.delete(agent)
          }
          return newSet
        })
    }
  }

  const sendMessage = () => {
    if (!inputValue.trim() || !wsRef.current) return

    const selectedAgents: string[] = [] 
    // 前端传空数组，让后端根据 API Key 自动决定
    
    const payload = {
      content: inputValue,
      timestamp: Date.now() / 1000,
      agents: selectedAgents,
      rounds: rounds, // 传递轮数到后端
      summarizer: summarizer, // 传递总结者到后端
      enable_web_search: enableWebSearch // 传递联网搜索开关
    }
    
    wsRef.current.send(JSON.stringify(payload))
    setInputValue('')
    setIsDebating(true)
  }
  
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-gray-100">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 p-4 flex items-center justify-between">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <Bot className="text-blue-400" />
          AI Debate Platform
        </h1>
        <div className="flex items-center gap-4">
          {/* 显示当前轮数 */}
          {isDebating && currentRound > 0 && (
            <div className="text-sm bg-blue-600 px-3 py-1 rounded-full font-semibold animate-pulse">
              第 {currentRound} 轮辩论
            </div>
          )}
          <div className="flex items-center gap-2 text-sm">
            <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></span>
            {isConnected ? 'Online' : 'Offline'}
          </div>
        </div>
      </header>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => {
          const isUser = msg.role === 'user'
          const isSystem = msg.role === 'system'
          
          if (isSystem) {
             return (
               <div key={index} className="flex justify-center text-xs text-gray-500 my-2">
                 {msg.content}
               </div>
             )
          }
          
          // 检查是否是总结消息
          const isSummary = msg.name?.includes('总结')

          return (
            <div key={index} className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[80%] rounded-lg p-3 ${
                isUser 
                  ? 'bg-blue-600 text-white' 
                  : isSummary
                  ? 'bg-gradient-to-r from-yellow-900 to-orange-900 text-gray-100 border-2 border-yellow-600'
                  : 'bg-gray-700 text-gray-200 border border-gray-600'
              }`}>
                {!isUser && (
                  <div className={`flex items-center gap-2 mb-1 text-xs font-bold ${
                    isSummary ? 'text-yellow-300' : 'text-blue-300'
                  }`}>
                    <Bot size={14} />
                    {msg.name || "AI"}
                    {isSummary && <span className="ml-1">📊</span>}
                  </div>
                )}
                <div className="whitespace-pre-wrap">{msg.content}</div>
              </div>
            </div>
          )
        })}
        
        {/* Typing Indicators */}
        {Array.from(typingAgents).map(agent => (
           <div key={agent} className="flex justify-start">
              <div className="bg-gray-700 text-gray-400 border border-gray-600 rounded-lg p-3 text-sm flex items-center gap-2">
                 <Bot size={14} />
                 <span className="font-bold">{agent}</span> is typing...
              </div>
           </div>
        ))}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-gray-800 p-4 border-t border-gray-700">
        {/* 配置选项行 */}
        <div className="mb-3 flex items-center gap-6 text-sm">
          {/* 轮数选择器 */}
          <div className="flex items-center gap-2">
            <label className="text-gray-400">辩论轮数:</label>
            <div className="flex gap-2">
              {[1, 2, 3, 4, 5].map(num => (
                <button
                  key={num}
                  onClick={() => setRounds(num)}
                  disabled={isDebating}
                  className={`px-3 py-1 rounded-lg transition-colors ${
                    rounds === num 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  } ${isDebating ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  {num}轮
                </button>
              ))}
            </div>
          </div>
          
          {/* 总结者选择器 */}
          <div className="flex items-center gap-2">
            <label className="text-gray-400">总结者:</label>
            <select
              value={summarizer}
              onChange={(e) => setSummarizer(e.target.value)}
              disabled={isDebating}
              className={`bg-gray-700 text-gray-200 px-3 py-1 rounded-lg border border-gray-600 focus:outline-none focus:border-blue-500 ${
                isDebating ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-600 cursor-pointer'
              }`}
            >
              {availableAIs.map(ai => (
                <option key={ai.id} value={ai.id}>
                  {ai.emoji} {ai.name}
                </option>
              ))}
            </select>
          </div>
          
          {/* 联网搜索开关 */}
          <div className="flex items-center gap-2">
            <label className="text-gray-400 flex items-center gap-1">
              <span>🌐</span>
              <span>联网搜索:</span>
            </label>
            <button
              onClick={() => setEnableWebSearch(!enableWebSearch)}
              disabled={isDebating}
              className={`px-3 py-1 rounded-lg border-2 transition-all ${
                enableWebSearch 
                  ? 'bg-green-600 border-green-500 text-white' 
                  : 'bg-gray-700 border-gray-600 text-gray-300'
              } ${isDebating ? 'opacity-50 cursor-not-allowed' : 'hover:opacity-80 cursor-pointer'}`}
            >
              {enableWebSearch ? '✓ 已开启' : '✗ 已关闭'}
            </button>
          </div>
        </div>
        
        <div className="flex gap-2">
          <input
            type="text"
            className="flex-1 bg-gray-900 border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 text-white"
            placeholder="Enter a topic for the AI agents to debate..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isDebating}
          />
          <button 
            onClick={sendMessage}
            disabled={!isConnected || !inputValue.trim() || isDebating}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white px-4 py-2 rounded-lg flex items-center gap-2"
          >
            <Send size={18} />
            Send
          </button>
        </div>
        <div className="text-xs text-gray-500 mt-2 text-center">
            Active Agents: DeepSeek, Qwen (千问), Doubao (豆包)
        </div>
      </div>
    </div>
  )
}

export default App
