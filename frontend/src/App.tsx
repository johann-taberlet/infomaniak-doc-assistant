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
    <div className="flex flex-col min-h-screen max-w-3xl mx-auto p-4 sm:p-2 bg-bg font-sans text-text leading-relaxed">
      <header className="text-center py-6">
        <h1 className="text-2xl sm:text-xl font-bold text-primary mb-1">kSuite Assistant</h1>
        <p className="text-text-muted text-sm">AI-powered help for kDrive, kMeet, and kChat</p>
      </header>

      <main className="flex-1 flex flex-col bg-bg-card rounded-xl shadow-md overflow-hidden">
        <div className="flex-1 overflow-y-auto p-6 sm:p-4 min-h-[400px] max-h-[60vh]">
          {messages.length === 0 && (
            <div className="text-center p-8">
              <p className="text-text-muted mb-6">Ask me anything about Infomaniak kSuite products!</p>
              <div className="flex flex-col gap-2">
                <button
                  onClick={() => handleSuggestionClick("How do I share a file in kDrive?")}
                  className="p-3 border border-border rounded-lg bg-bg text-left cursor-pointer transition-all hover:border-primary hover:bg-user-bg"
                >
                  How do I share a file in kDrive?
                </button>
                <button
                  onClick={() => handleSuggestionClick("How do I start a kMeet video call?")}
                  className="p-3 border border-border rounded-lg bg-bg text-left cursor-pointer transition-all hover:border-primary hover:bg-user-bg"
                >
                  How do I start a kMeet video call?
                </button>
                <button
                  onClick={() => handleSuggestionClick("How do I create a channel in kChat?")}
                  className="p-3 border border-border rounded-lg bg-bg text-left cursor-pointer transition-all hover:border-primary hover:bg-user-bg"
                >
                  How do I create a channel in kChat?
                </button>
              </div>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`mb-4 p-4 rounded-lg ${
                message.role === "user"
                  ? "bg-user-bg ml-8 sm:ml-4"
                  : "bg-assistant-bg border border-border mr-8 sm:mr-4"
              }`}
            >
              <div className="text-xs font-semibold text-text-muted mb-1 uppercase">
                {message.role === "user" ? "You" : "Assistant"}
              </div>
              <div className="whitespace-pre-wrap break-words">{getMessageContent(message)}</div>
            </div>
          ))}

          {isLoading && (
            <div className="mb-4 p-4 rounded-lg bg-assistant-bg border border-border mr-8 sm:mr-4">
              <div className="text-xs font-semibold text-text-muted mb-1 uppercase">Assistant</div>
              <div className="flex gap-1 py-2">
                <span className="w-2 h-2 bg-primary rounded-full animate-bounce-dot" />
                <span className="w-2 h-2 bg-primary rounded-full animate-bounce-dot" />
                <span className="w-2 h-2 bg-primary rounded-full animate-bounce-dot" />
              </div>
            </div>
          )}

          {error && (
            <div className="p-4 bg-red-50 text-error rounded-lg mb-4">
              Error: {error.message || "Something went wrong"}
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="flex gap-2 p-4 border-t border-border">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about kDrive, kMeet, or kChat..."
            disabled={isLoading}
            className="flex-1 py-3 px-4 border border-border rounded-lg text-base outline-none transition-colors focus:border-primary disabled:bg-bg disabled:cursor-not-allowed"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="py-3 px-6 bg-primary text-white border-none rounded-lg text-base cursor-pointer transition-colors hover:bg-primary-dark disabled:bg-border disabled:cursor-not-allowed"
          >
            Send
          </button>
        </form>
      </main>

      <footer className="text-center p-4 text-text-muted text-xs">
        <p>Powered by RAG with Qdrant | Demo for Infomaniak</p>
      </footer>
    </div>
  );
}

export default App;
