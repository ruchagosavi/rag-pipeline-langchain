// // import React, { useState } from "react";
// // import { askQuestion } from "../services/api";

// // const Chatbox = () => {
// //   const [question, setQuestion] = useState("");
// //   const [answer, setAnswer] = useState("");
// //   const [loading, setLoading] = useState(false);
// //   const [error, setError] = useState("");

// //   const handleSubmit = async () => {
// //     if (!question.trim()) return;

// //     setLoading(true);
// //     setError("");
// //     setAnswer("");

// //     try {
// //       const data = await askQuestion(question);
// //       setAnswer(data.answer);
// //     } catch (err) {
// //       setError("Backend not responding");
// //     } finally {
// //       setLoading(false);
// //     }
// //   };

// //   return (
// //     <div className="card shadow p-4">
// //       <h3 className="text-center mb-3">RiskRadar AI</h3>

// //       <textarea
// //         className="form-control mb-3"
// //         rows="4"
// //         placeholder="Ask a risk-related question..."
// //         value={question}
// //         onChange={(e) => setQuestion(e.target.value)}
// //       />

// //       <button
// //         className="btn btn-success w-100"
// //         onClick={handleSubmit}
// //         disabled={loading}
// //       >
// //         {loading ? "Thinking..." : "Ask AI"}
// //       </button>

// //       {answer && (
// //         <div className="alert alert-success mt-4">
// //           <strong>Answer:</strong>
// //           <p className="mb-0">{answer}</p>
// //         </div>
// //       )}

// //       {error && (
// //         <div className="alert alert-danger mt-3">
// //           {error}
// //         </div>
// //       )}
// //     </div>
// //   );
// // };

// // export default Chatbox;
// import React, { useState } from "react";
// import { askQuestion } from "../services/api";

// const Chatbox = () => {
//   const [question, setQuestion] = useState("");
//   const [answer, setAnswer] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState("");

//   const handleSubmit = async () => {
//     if (!question.trim()) return;

//     setLoading(true);
//     setError("");
//     setAnswer("");

//     try {
//       const data = await askQuestion(question);
//       setAnswer(data.answer);
//     } catch (err) {
//       setError("Backend not responding");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div
//       className="card shadow p-4"
//       style={{
//         background: "linear-gradient(135deg, #f5f7fa, #c3cfe2)", // new background
//         borderRadius: "15px",
//       }}
//     >
//       <h3
//         className="text-center mb-3"
//         style={{
//           fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
//           color: "#2c3e50",
//           letterSpacing: "1px",
//           textShadow: "1px 1px 2px rgba(0,0,0,0.1)",
//         }}
//       >
//         RiskRadar AI
//       </h3>

//       <textarea
//         className="form-control mb-3"
//         rows="4"
//         placeholder="Ask a risk-related question..."
//         value={question}
//         onChange={(e) => setQuestion(e.target.value)}
//       />

//       <button
//         className="btn btn-success w-100"
//         onClick={handleSubmit}
//         disabled={loading}
//       >
//         {loading ? "Thinking..." : "Ask AI"}
//       </button>

//       {answer && (
//         <div className="alert alert-success mt-4">
//           <strong>Answer:</strong>
//           <p className="mb-0">{answer}</p>
//         </div>
//       )}

//       {error && (
//         <div className="alert alert-danger mt-3">
//           {error}
//         </div>
//       )}
//     </div>
//   );
// };

// export default Chatbox;

import React, { useState } from "react";
import { askQuestion } from "../services/api";

const Chatbox = () => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setError("");
    setAnswer([]);

    try {
      const data = await askQuestion(question);

      // Split answer by newlines or bullets to create array of points
      const points = data.answer
        .split(/\n|•|-/) // split by newline or bullet/dash
        .map((p) => p.trim())
        .filter((p) => p); // remove empty strings

      setAnswer(points);
    } catch (err) {
      setError("Backend not responding");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="card shadow p-4"
      style={{ backgroundColor: "#f0f4f8" }} // custom background color
    >
      <h3
        className="text-center mb-3"
        style={{
          fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
          color: "#2c3e50",
          fontWeight: "700",
        }}
      >
        RiskRadar AI
      </h3>

      <textarea
        className="form-control mb-3"
        rows="4"
        placeholder="Ask a risk-related question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button
        className="btn btn-success w-100"
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? "Thinking..." : "Ask AI"}
      </button>

      {answer.length > 0 && (
        <div className="alert alert-success mt-4">
          <strong>Answer:</strong>
          <ul className="mt-2">
            {answer.map((point, idx) => (
              <li key={idx} style={{ marginBottom: "0.5rem" }}>
                {point}
              </li>
            ))}
          </ul>
        </div>
      )}

      {error && (
        <div className="alert alert-danger mt-3">
          {error}
        </div>
      )}
    </div>
  );
};

export default Chatbox;
