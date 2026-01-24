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
    <div className="h-full flex flex-col bg-ik-bg-page">
      {/* Header */}
      <header className="flex items-center justify-between bg-ik-bg-card px-6 py-3 border-b border-ik-border shadow-ik-sm shrink-0">
        <h1 className="text-xl font-semibold text-ik-primary tracking-tight">
          kSuite Assistant
        </h1>
        <span className="text-sm text-ik-text-muted">
          AI-powered help for kDrive, kMeet, and kChat
        </span>
      </header>

      {/* Main content */}
      <main className="flex-1 flex flex-col min-h-0 overflow-hidden">
        <div className="flex flex-col flex-1 w-full max-w-[900px] mx-auto p-6">
          {/* Chat container */}
          <div className="flex-1 bg-ik-bg-card rounded-ik-lg p-6 mb-4 overflow-y-auto shadow-ik-md border border-ik-border-light">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-ik-text-muted">
                {/* Gradient circle icon */}
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-ik-primary to-cyan-400 opacity-80 mb-3" />
                <p className="mb-6">Ask me anything about Infomaniak kSuite products!</p>

                {/* Suggestion buttons */}
                <div className="flex flex-col gap-3 w-full max-w-md">
                  {[
                    "How do I share a file in kDrive?",
                    "How do I start a kMeet video call?",
                    "How do I create a channel in kChat?",
                  ].map((suggestion) => (
                    <button
                      key={suggestion}
                      onClick={() => handleSuggestionClick(suggestion)}
                      className="px-4 py-3 text-left text-ik-text-secondary bg-ik-bg-tertiary border border-ik-border rounded-ik-md transition-all duration-200 hover:border-ik-primary hover:bg-ik-primary-light hover:text-ik-primary"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div className="space-y-5">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`animate-message-slide-in max-w-[85%] p-4 rounded-ik-lg ${
                      message.role === "user"
                        ? "ml-auto bg-ik-primary text-ik-text-inverse rounded-br-sm shadow-ik-primary"
                        : "mr-auto bg-ik-bg-secondary text-ik-text-primary border border-ik-border rounded-bl-sm"
                    }`}
                  >
                    <div className="leading-relaxed whitespace-pre-wrap">
                      {getMessageContent(message)}
                    </div>
                  </div>
                ))}

                {isLoading && (
                  <div className="animate-message-slide-in max-w-[85%] mr-auto p-4 rounded-ik-lg rounded-bl-sm bg-ik-bg-secondary border border-ik-border">
                    <div className="flex items-center gap-1 text-ik-text-muted italic">
                      <span>Thinking</span>
                      <span className="animate-thinking-dot">.</span>
                      <span className="animate-thinking-dot">.</span>
                      <span className="animate-thinking-dot">.</span>
                    </div>
                  </div>
                )}

                {error && (
                  <div className="p-4 bg-ik-error-bg text-ik-error border border-red-200 rounded-ik-md">
                    Error: {error.message || "Something went wrong"}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Input form */}
          <form
            onSubmit={handleSubmit}
            className="flex gap-3 bg-ik-bg-card p-3 rounded-ik-xl shadow-ik-md border border-ik-border-light shrink-0"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about kDrive, kMeet, or kChat..."
              disabled={isLoading}
              className="flex-1 px-5 py-3 bg-ik-bg-tertiary text-ik-text-primary border-2 border-transparent rounded-ik-lg text-base transition-all duration-200 placeholder:text-ik-text-muted focus:outline-none focus:border-ik-primary focus:bg-ik-bg-card focus:shadow-[0_0_0_3px_rgba(0,152,255,0.1)] disabled:bg-ik-bg-secondary disabled:cursor-not-allowed"
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="px-7 py-3 bg-ik-primary text-ik-text-inverse font-medium rounded-ik-lg text-base cursor-pointer transition-all duration-200 shadow-ik-primary hover:bg-ik-primary-hover hover:-translate-y-0.5 hover:shadow-[0_6px_16px_rgba(0,152,255,0.3)] active:translate-y-0 disabled:bg-ik-border disabled:text-ik-text-muted disabled:cursor-not-allowed disabled:shadow-none disabled:hover:translate-y-0"
            >
              Send
            </button>
          </form>
        </div>
      </main>

      {/* Footer */}
      <footer className="text-center py-3 text-ik-text-muted text-xs shrink-0">
        Powered by RAG with Qdrant | Demo for Infomaniak
      </footer>
    </div>
  );
}

export default App;
