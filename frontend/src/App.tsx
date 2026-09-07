import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  async function askTutor() {
    if (!question.trim()) {
      return;
    }

    setLoading(true);
    setAnswer("");

    const url =
      "http://" +
      "127.0.0.1" +
      ":8000" +
      "/api/ai/tutor/chat";

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      });

      const data = await response.json();

      setAnswer(
        data.answer ||
          data.response ||
          data.explanation ||
          "No answer received."
      );
    } catch {
      setAnswer(
        "Unable to connect to the AI backend. Please make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Quantum AI Tutor</h1>
          <p>
            Learn quantum computing with an interactive AI assistant.
          </p>
        </div>
      </header>

      <main className="main">
        <section className="hero">
          <h2>Ask anything about Quantum Computing</h2>
          <p>
            Ask questions about qubits, gates, superposition,
            entanglement, quantum algorithms, and Qiskit.
          </p>
        </section>

        <section className="tutor-card">
          <label htmlFor="question">Your question</label>

          <textarea
            id="question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Example: What is a qubit?"
            rows={5}
          />

          <button
            onClick={askTutor}
            disabled={loading || !question.trim()}
          >
            {loading ? "Thinking..." : "Ask AI Tutor"}
          </button>
        </section>

        {answer && (
          <section className="answer-card">
            <h2>AI Tutor</h2>

            <div className="answer">
              <ReactMarkdown>{answer}</ReactMarkdown>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
