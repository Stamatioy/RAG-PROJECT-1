import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello! Ask me something about Ancient Greece.",
    },
  ]);

  function handleSubmit(event) {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion) {
      return;
    }

    setMessages((currentMessages) => [
      ...currentMessages,
      {
        role: "user",
        content: trimmedQuestion,
      },
    ]);

    setQuestion("");
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

              <p>{message.content}</p>
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
          />

          <button type="submit">
            Send
          </button>
        </form>
      </section>
    </main>
  );
}

export default App;