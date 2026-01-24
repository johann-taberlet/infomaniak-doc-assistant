import { useChat } from "@ai-sdk/react";

function App() {
  const { messages, input, handleInputChange, handleSubmit, isLoading, error } =
    useChat({
      api: "/api/chat",
    });

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
                <button
                  onClick={() => {
                    const event = {
                      target: { value: "How do I share a file in kDrive?" },
                    } as React.ChangeEvent<HTMLInputElement>;
                    handleInputChange(event);
                  }}
                >
                  How do I share a file in kDrive?
                </button>
                <button
                  onClick={() => {
                    const event = {
                      target: { value: "How do I start a kMeet video call?" },
                    } as React.ChangeEvent<HTMLInputElement>;
                    handleInputChange(event);
                  }}
                >
                  How do I start a kMeet video call?
                </button>
                <button
                  onClick={() => {
                    const event = {
                      target: { value: "How do I create a channel in kChat?" },
                    } as React.ChangeEvent<HTMLInputElement>;
                    handleInputChange(event);
                  }}
                >
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
              <div className="message-content">{message.content}</div>
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
            onChange={handleInputChange}
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
