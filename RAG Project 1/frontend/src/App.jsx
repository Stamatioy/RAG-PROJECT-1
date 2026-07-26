import { useState } from "react";
import "./App.css";

const API_URL = "http://localhost:8000/chat";

function App() {
  const [question, setQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello! Ask me something about Ancient Greece.",
      sources: [],
    },
  ]);

  async function handleSubmit(event) {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || isLoading) {
      return;
    }

    const userMessage = {
      role: "user",
      content: trimmedQuestion,
      sources: [],
    };

    const assistantMessage = {
      role: "assistant",
      content: "",
      sources: [],
    };

    setMessages((currentMessages) => [
      ...currentMessages,
      userMessage,
      assistantMessage,
    ]);

    setQuestion("");
    setIsLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: trimmedQuestion,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);

        throw new Error(
          errorData?.message || `Request failed with status ${response.status}`
        );
      }

      if (!response.body) {
        throw new Error("The server returned no response stream.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();

        if (done) {
          break;
        }

        buffer += decoder.decode(value, {
          stream: true,
        });

        const events = buffer.split("\n\n");

        buffer = events.pop() || "";

        for (const eventText of events) {
          const dataLine = eventText
            .split("\n")
            .find((line) => line.startsWith("data: "));

          if (!dataLine) {
            continue;
          }

          const eventData = dataLine.slice(6).trim();

          if (eventData === "[DONE]") {
            continue;
          }

          let payload;

          try {
            payload = JSON.parse(eventData);
          } catch {
            console.error("Could not parse SSE event:", eventData);
            continue;
          }

          if (payload.type === "token") {
            setMessages((currentMessages) => {
              const updatedMessages = [...currentMessages];
              const lastMessageIndex = updatedMessages.length - 1;

              updatedMessages[lastMessageIndex] = {
                ...updatedMessages[lastMessageIndex],
                content:
                  updatedMessages[lastMessageIndex].content + payload.content,
              };

              return updatedMessages;
            });
          }

          if (payload.type === "sources") {
            setMessages((currentMessages) => {
              const updatedMessages = [...currentMessages];
              const lastMessageIndex = updatedMessages.length - 1;

              updatedMessages[lastMessageIndex] = {
                ...updatedMessages[lastMessageIndex],
                sources: payload.content,
              };

              return updatedMessages;
            });
          }

          if (payload.type === "error") {
            throw new Error(payload.content);
          }
        }
      }
    } catch (error) {
      console.error(error);

      setMessages((currentMessages) => {
        const updatedMessages = [...currentMessages];
        const lastMessageIndex = updatedMessages.length - 1;

        updatedMessages[lastMessageIndex] = {
          ...updatedMessages[lastMessageIndex],
          content: `Error: ${error.message}`,
        };

        return updatedMessages;
      });
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="app">
      <section className="chat-container">
        <header className="chat-header">
          <h1>Ancient Greece RAG</h1>
          <p>Ask questions using the local knowledge base</p>
        </header>

        <div className="message-list">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message message-${message.role}`}
            >
              <span className="message-role">
                {message.role === "user" ? "You" : "Assistant"}
              </span>

              <p>
                {message.content ||
                  (isLoading &&
                  index === messages.length - 1
                    ? "Thinking..."
                    : "")}
              </p>

              {message.sources?.length > 0 && (
                <div className="sources">
                  <strong>Sources</strong>

                  {message.sources.map((source, sourceIndex) => (
                    <a
                      key={`${source.url}-${sourceIndex}`}
                      href={source.url}
                      target="_blank"
                      rel="noreferrer"
                      className="source-link"
                    >
                      {source.source}
                      {source.section ? ` — ${source.section}` : ""}
                    </a>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        <form className="chat-form" onSubmit={handleSubmit}>
          <input
            type="text"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask a question..."
            aria-label="Question"
            disabled={isLoading}
          />

          <button
            type="submit"
            disabled={isLoading || !question.trim()}
          >
            {isLoading ? "Generating..." : "Send"}
          </button>
        </form>
      </section>
    </main>
  );
}

export default App;