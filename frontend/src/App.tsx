import { useState } from "react";
import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport } from "ai";
import type { UIMessage } from "ai";

// Create transport with API endpoint
const transport = new DefaultChatTransport({
  api: "/api/chat",
});

function App() {
  const [input, setInput] = useState("");
  const { messages, sendMessage, status, error } = useChat({
    transport,
  });

  const isLoading = status === "streaming" || status === "submitted";

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    sendMessage({ text: input });
    setInput("");
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
  };

  // Extract text content from message parts
  const getMessageContent = (message: UIMessage): string => {
    return message.parts
      .filter((part): part is { type: "text"; text: string } => part.type === "text")
      .map((part) => part.text)
      .join("");
  };

  return (
    <div className="app">
      <header className="header">
        <h1>kSuite Assistant</h1>
        <p>AI-powered help for kDrive, kMeet, and kChat</p>
      </header>

      <main className="chat-container">
        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome">
              <p>Ask me anything about Infomaniak kSuite products!</p>
              <div className="suggestions">
                <button onClick={() => handleSuggestionClick("How do I share a file in kDrive?")}>
                  How do I share a file in kDrive?
                </button>
                <button onClick={() => handleSuggestionClick("How do I start a kMeet video call?")}>
                  How do I start a kMeet video call?
                </button>
                <button onClick={() => handleSuggestionClick("How do I create a channel in kChat?")}>
                  How do I create a channel in kChat?
                </button>
              </div>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.role === "user" ? "user" : "assistant"}`}
            >
              <div className="message-role">
                {message.role === "user" ? "You" : "Assistant"}
              </div>
              <div className="message-content">{getMessageContent(message)}</div>
            </div>
          ))}

          {isLoading && (
            <div className="message assistant">
              <div className="message-role">Assistant</div>
              <div className="message-content loading">
                <span className="dot"></span>
                <span className="dot"></span>
                <span className="dot"></span>
              </div>
            </div>
          )}

          {error && (
            <div className="error">
              Error: {error.message || "Something went wrong"}
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about kDrive, kMeet, or kChat..."
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading || !input.trim()}>
            Send
          </button>
        </form>
      </main>

      <footer className="footer">
        <p>
          Powered by RAG with Qdrant | Demo for Infomaniak
        </p>
      </footer>
    </div>
  );
}

export default App;
