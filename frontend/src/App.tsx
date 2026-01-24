import { useState } from "react";
import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport } from "ai";
import type { UIMessage } from "ai";
import { ThemeToggle } from "./components/ThemeToggle";
import { JsonRendererDemo } from "./lib/JsonRendererDemo";

// Toggle to show component demo instead of chat
const SHOW_DEMO = false;

// Create transport with API endpoint
const transport = new DefaultChatTransport({
  api: "/api/chat",
});

function App() {
  const [input, setInput] = useState("");
  const { messages, sendMessage, status, error } = useChat({
    transport,
  });

  // Render demo mode for testing components
  if (SHOW_DEMO) {
    return <JsonRendererDemo />;
  }

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
    <div className="h-full flex flex-col bg-[var(--ik-bg-page)]">
      {/* Header */}
      <header className="flex items-center justify-between bg-[var(--ik-bg-card)] px-6 py-3 border-b border-[var(--ik-border)] shadow-[var(--ik-shadow-sm)] shrink-0">
        <h1 className="text-xl font-semibold text-[var(--ik-primary)] tracking-tight">
          kSuite Assistant
        </h1>
        <div className="flex items-center gap-4">
          <span className="text-sm text-[var(--ik-text-muted)] hidden sm:inline">
            AI-powered help for kDrive, kMeet, and kChat
          </span>
          <ThemeToggle />
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 flex flex-col items-center min-h-0 overflow-hidden p-6">
        <div className="flex flex-col flex-1 w-full max-w-[900px] min-h-0">
          {/* Chat container */}
          <div className="flex-1 bg-[var(--ik-bg-card)] rounded-[var(--ik-radius-lg)] p-6 mb-4 overflow-y-auto shadow-[var(--ik-shadow-md)] border border-[var(--ik-border-light)]">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-[var(--ik-text-muted)]">
                {/* Gradient circle icon */}
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[var(--ik-primary)] to-cyan-400 opacity-80 mb-3" />
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
                      className="px-4 py-3 text-left text-[var(--ik-text-secondary)] bg-[var(--ik-bg-tertiary)] border border-[var(--ik-border)] rounded-[var(--ik-radius-md)] transition-all duration-200 hover:border-[var(--ik-primary)] hover:bg-[var(--ik-primary-light)] hover:text-[var(--ik-primary)]"
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
                    className={`animate-message-slide-in max-w-[85%] p-4 ${
                      message.role === "user"
                        ? "ml-auto bg-[var(--ik-user-message-bg)] text-[var(--ik-user-message-text)] rounded-[var(--ik-radius-lg)] rounded-br-[4px] shadow-[var(--ik-shadow-primary)]"
                        : "mr-auto bg-[var(--ik-bg-secondary)] text-[var(--ik-text-primary)] border border-[var(--ik-border)] rounded-[var(--ik-radius-lg)] rounded-bl-[4px]"
                    }`}
                  >
                    <div className="leading-relaxed whitespace-pre-wrap">
                      {getMessageContent(message)}
                    </div>
                  </div>
                ))}

                {isLoading && (
                  <div className="animate-message-slide-in max-w-[85%] mr-auto p-4 rounded-[var(--ik-radius-lg)] rounded-bl-[4px] bg-[var(--ik-bg-secondary)] border border-[var(--ik-border)]">
                    <div className="flex items-center gap-1 text-[var(--ik-text-muted)] italic">
                      <span>Thinking</span>
                      <span className="animate-thinking-dot">.</span>
                      <span className="animate-thinking-dot">.</span>
                      <span className="animate-thinking-dot">.</span>
                    </div>
                  </div>
                )}

                {error && (
                  <div className="p-4 bg-[var(--ik-error-bg)] text-[var(--ik-error)] border border-red-200 rounded-[var(--ik-radius-md)]">
                    Error: {error.message || "Something went wrong"}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Input form */}
          <form
            onSubmit={handleSubmit}
            className="flex gap-3 bg-[var(--ik-bg-card)] p-3 rounded-[var(--ik-radius-xl)] shadow-[var(--ik-shadow-md)] border border-[var(--ik-border-light)] shrink-0"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about kDrive, kMeet, or kChat..."
              disabled={isLoading}
              className="flex-1 px-5 py-3 bg-[var(--ik-bg-tertiary)] text-[var(--ik-text-primary)] border-2 border-transparent rounded-[var(--ik-radius-lg)] text-base transition-all duration-200 placeholder:text-[var(--ik-text-muted)] focus:outline-none focus:border-[var(--ik-primary)] focus:bg-[var(--ik-bg-card)] disabled:bg-[var(--ik-bg-secondary)] disabled:cursor-not-allowed"
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="px-7 py-3 bg-[var(--ik-primary)] text-[var(--ik-text-inverse)] font-medium rounded-[var(--ik-radius-lg)] text-base cursor-pointer transition-all duration-200 shadow-[var(--ik-shadow-primary)] hover:bg-[var(--ik-primary-hover)] hover:-translate-y-0.5 active:translate-y-0 disabled:bg-[var(--ik-border)] disabled:text-[var(--ik-text-muted)] disabled:cursor-not-allowed disabled:shadow-none disabled:hover:translate-y-0"
            >
              Send
            </button>
          </form>
        </div>
      </main>

      {/* Footer */}
      <footer className="text-center py-3 text-[var(--ik-text-muted)] text-xs shrink-0">
        Powered by RAG with Qdrant | Demo for Infomaniak
      </footer>
    </div>
  );
}

export default App;
