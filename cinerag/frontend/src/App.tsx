import { useState, useRef, useEffect } from 'react'
import './App.css'

interface Message {
  role: 'user' | 'agent'
  text: string
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'agent', text: 'Luzes, câmera, perguntas. Sou o CineRAG — seu especialista em cinema. Sobre qual filme, diretor ou roteiro você quer saber?' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function sendMessage() {
    if (!input.trim() || loading) return
    const question = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', text: question }])
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      })
      const data = await res.json()
      setMessages(prev => [...prev, { role: 'agent', text: data.answer }])
    } catch {
      setMessages(prev => [...prev, { role: 'agent', text: 'Erro ao conectar com o backend.' }])
    } finally {
      setLoading(false)
    }
  }

  function handleKey(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <span className="logo-icon">🎬</span>
          <span className="logo-text">CineRAG</span>
        </div>
        <p className="tagline">Agente de IA especialista em cinema</p>
      </header>

      <main className="chat">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <span className="bubble">{msg.text}</span>
          </div>
        ))}
        {loading && (
          <div className="message agent">
            <span className="bubble typing">
              <span /><span /><span />
            </span>
          </div>
        )}
        <div ref={bottomRef} />
      </main>

      <footer className="input-area">
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Pergunte sobre filmes, diretores, roteiros..."
          rows={1}
        />
        <button onClick={sendMessage} disabled={loading || !input.trim()}>
          ↑
        </button>
      </footer>
    </div>
  )
}

export default App