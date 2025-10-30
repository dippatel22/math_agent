import React, { useState, useCallback } from 'react';
import { Sparkles, Send } from 'lucide-react'; 
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css'; 


const API_BASE_URL = 'http://127.0.0.1:8000/api';

const ASSESSMENT_OPTIONS = [
    { value: 'CORRECT', label: ' Correct and Well-Grounded' },
    { value: 'INCORRECT', label: 'Incorrect/Factually Flawed' },
    { value: 'COMPLEX', label: ' Correct but Too Complex/Vague' },
    { value: 'OFF_TOPIC', label: ' Off-Topic or Guardrail Failure' },
];

const initialSolutionState = {
    mode: 'REJECTED',
    solution: '',
    confidence: 0,
    status: '',
};

const initialFeedbackState = {
    query: '',
    generated_solution: '',
    assessment: '',
    correction_text: '',
    route_mode: '',
    confidence_score: 0,
};

const MathRenderer = ({ content }) => (
    <div style={{ padding: '10px 0' }}>
        <ReactMarkdown
            children={content}
            remarkPlugins={[remarkMath]}
            rehypePlugins={[rehypeKatex]}
            // You can add a custom component for links if needed, but not strictly necessary here.
            components={{
                // Custom component to ensure Markdown headings render correctly
                h3: ({ node, ...props }) => <h3 style={{ fontSize: '18px', fontWeight: 'bold', marginTop: '15px', marginBottom: '8px', borderBottom: '1px solid #eee', paddingBottom: '4px' }} {...props} />,
                p: ({ node, ...props }) => <p style={{ marginBottom: '10px', lineHeight: '1.5' }} {...props} />,
                ol: ({ node, ...props }) => <ol style={{ paddingLeft: '20px', margin: '10px 0' }} {...props} />,
                ul: ({ node, ...props }) => <ul style={{ paddingLeft: '20px', margin: '10px 0' }} {...props} />,
            }}
        />
    </div>
);
// -----------------------------------

const styles = `
    .app-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 24px;
        background-color: #f7f9fc;
        min-height: 100vh;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
    }
    .header {
        background-color: #4a69bd;
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
    }
    .title {
        font-size: 24px;
        font-weight: 700;
        margin-left: 12px;
    }
    .question-form {
        display: flex;
        gap: 12px;
        margin-bottom: 24px;
    }
    .input-field {
        flex-grow: 1;
        padding: 12px;
        border: 1px solid #c8c8c8;
        border-radius: 8px;
        font-size: 16px;
        transition: border-color 0.2s;
    }
    .input-field:focus {
        border-color: #4a69bd;
        outline: none;
    }
    .solve-button {
        padding: 12px 24px;
        background-color: #1aae6f;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.2s, transform 0.1s;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .solve-button:hover:not(:disabled) {
        background-color: #159560;
        transform: translateY(-1px);
    }
    .solve-button:disabled {
        background-color: #9cd4ba;
        cursor: not-allowed;
    }
    .solution-card {
        background-color: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 24px;
    }
    .solution-title {
        font-size: 20px;
        font-weight: 600;
        color: #333;
        margin-bottom: 16px;
        border-bottom: 2px solid #eee;
        padding-bottom: 8px;
    }
    .solution-step {
        margin-bottom: 12px;
        line-height: 1.6;
    }
    .confidence-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 10px;
        margin-right: 8px;
    }
    .confidence-badge.kb {
        background-color: #e0f7fa;
        color: #00838f;
    }
    .confidence-badge.web {
        background-color: #fff3e0;
        color: #ff8f00;
    }
    .error-message {
        color: #d32f2f;
        background-color: #ffcdd2;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #ef9a9a;
        font-weight: 500;
    }
    .feedback-form-container {
        border-top: 3px solid #ccc;
        padding-top: 24px;
        margin-top: 24px;
        background-color: #fff;
        border-radius: 12px;
        padding: 24px;
    }
    .feedback-header {
        font-size: 20px;
        font-weight: 700;
        color: #e67e22;
        margin-bottom: 16px;
    }
    .form-group {
        margin-bottom: 16px;
    }
    .form-label {
        display: block;
        font-weight: 600;
        margin-bottom: 6px;
        color: #555;
    }
    .form-select, .form-textarea {
        width: 100%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 6px;
        font-size: 16px;
        box-sizing: border-box;
        transition: border-color 0.2s;
    }
    .form-textarea {
        resize: vertical;
        min-height: 100px;
    }
    .form-select:focus, .form-textarea:focus {
        border-color: #e67e22;
        outline: none;
    }
    .submit-button {
        padding: 12px 24px;
        background-color: #e67e22;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.2s;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .submit-button:hover {
        background-color: #d35400;
    }
`;

const App = () => {
    // ... (rest of the state and helper functions remain the same) ...

    React.useEffect(() => {
        if (!document.getElementById('app-styles')) {
            const styleTag = document.createElement('style');
            styleTag.id = 'app-styles';
            styleTag.textContent = styles;
            document.head.appendChild(styleTag);
        }
    }, []);

    const [question, setQuestion] = useState('What is the sum of the first 10 natural numbers?');
    const [solution, setSolution] = useState(initialSolutionState);
    const [feedback, setFeedback] = useState(initialFeedbackState);
    const [isLoading, setIsLoading] = useState(false);
    const [solutionError, setSolutionError] = useState(null);

    // Helper function to handle exponential backoff for API calls
    const fetchWithRetry = useCallback(async (url, options, maxRetries = 3) => {
        for (let i = 0; i < maxRetries; i++) {
            try {
                const response = await fetch(url, options);
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || `HTTP error! Status: ${response.status}`);
                }
                return await response.json();
            } catch (error) {
                if (i < maxRetries - 1) {
                    const delay = Math.pow(2, i) * 1000;
                    console.warn(`Request failed. Retrying in ${delay / 1000}s...`);
                    await new Promise(resolve => setTimeout(resolve, delay));
                } else {
                    throw error;
                }
            }
        }
    }, []);

    const handleGetSolution = useCallback(async (e) => {
        e.preventDefault();
        if (!question.trim()) return;

        setIsLoading(true);
        setSolution(initialSolutionState);
        setSolutionError(null);
        setFeedback(initialFeedbackState);

        try {
            const payload = { query: question.trim(), level: 'JEE', user_id: 'anon' };
            const data = await fetchWithRetry(`${API_BASE_URL}/solve`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            setSolution(data);
            setFeedback(prev => ({
                ...prev,
                query: question.trim(),
                generated_solution: String(data.solution),
                route_mode: data.mode,
                confidence_score: data.confidence,
            }));
        } catch (error) {
            console.error('Error fetching solution:', error);
            setSolutionError(`API Error: ${String(error.message || 'Check the Python backend logs.')}`);
        } finally {
            setIsLoading(false);
        }
    }, [question, fetchWithRetry]);

    const handleSubmitFeedback = useCallback(async (e) => {
        e.preventDefault();
        if (feedback.assessment === '') {
            document.getElementById('feedback-message-box').textContent = 'Please select an assessment before submitting feedback.';
            setTimeout(() => document.getElementById('feedback-message-box').textContent = '', 3000);
            return;
        }

        try {
            await fetchWithRetry(`${API_BASE_URL}/feedback`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(feedback),
            });
            document.getElementById('feedback-message-box').textContent = 'Feedback submitted successfully! Thanks for training the model.';
            setTimeout(() => document.getElementById('feedback-message-box').textContent = '', 3000);
            setFeedback(prev => ({ ...prev, assessment: '', correction_text: '' }));
        } catch (error) {
            console.error('Error submitting feedback:', error);
            document.getElementById('feedback-message-box').textContent = 'Failed to submit feedback. Check the backend server log for details.';
            setTimeout(() => document.getElementById('feedback-message-box').textContent = '', 3000);
        }
    }, [feedback, fetchWithRetry]);

    const handleFeedbackChange = useCallback((e) => {
        const { name, value } = e.target;
        setFeedback(prev => ({ ...prev, [name]: value }));
    }, []);

    return (
        <div className="app-container">
            <header className="header">
                <Sparkles size={28} />
                <h1 className="title">Math RAG Assistant & HIL Feedback</h1>
            </header>

            {/* QUESTION INPUT FORM */}
            <form onSubmit={handleGetSolution} className="question-form">
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Enter your Math question..."
                    className="input-field"
                    disabled={isLoading}
                />
                <button type="submit" className="solve-button" disabled={isLoading}>
                    {isLoading ? 'Solving...' : 'Get Solution'}
                    {isLoading && <span style={{ marginLeft: '8px' }}>...</span>}
                </button>
            </form>

            {/* LOADING / ERROR DISPLAY */}
            {isLoading && <p className="solution-card solution-step">...Generating solution. Please wait...</p>}
            {solutionError && <div className="error-message">Connection Error: {String(solutionError)}</div>}

            {/* SOLUTION DISPLAY CARD */}
            {solution.solution && !isLoading && !solutionError && (
                <div className="solution-card">
                    <h2 className="solution-title">
                        Solution Generated by {solution.mode.replace('_', ' ')} Agent
                    </h2>
                    <div className="solution-step">
                        <span className={`confidence-badge ${solution.mode === 'KB_RESPONSE' ? 'kb' : 'web'}`}>
                            Mode: {solution.mode}
                        </span>
                        {solution.mode === 'KB_RESPONSE' && (
                            <span className="confidence-badge kb">
                                KB Confidence: {solution.confidence.toFixed(4)}
                            </span>
                        )}
                    </div>
                    {/* CRITICAL FIX HERE: Use MathRenderer instead of <pre> */}
                    <MathRenderer content={String(solution.solution)} />
                    {/* The previous code: 
                    <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit', margin: 0, padding: '10px 0' }}>
                        {String(solution.solution)}
                    </pre>
                    */}
                </div>
            )}

            {/* HUMAN FEEDBACK (HIL) FORM */}
            {solution.solution && !isLoading && !solutionError && (
                <div className="feedback-form-container">
                    <h3 className="feedback-header">
                        Human Verification Loop (HIL)
                    </h3>
                    <p>Help us improve the model by validating the answer above:</p>

                    <div style={{minHeight: '20px', color: '#4a69bd', fontWeight: 'bold', marginBottom: '10px'}} id="feedback-message-box"></div>

                    <form onSubmit={handleSubmitFeedback}>
                        <div className="form-group">
                            <label htmlFor="assessment" className="form-label">1. Assessment (Required)</label>
                            <select
                                id="assessment"
                                name="assessment"
                                value={feedback.assessment}
                                onChange={handleFeedbackChange}
                                className="form-select"
                                required
                            >
                                <option value="">-- Select Verification Status --</option>
                                {ASSESSMENT_OPTIONS.map(opt => (
                                    <option key={opt.value} value={opt.value}>
                                        {opt.label}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="form-group">
                            <label htmlFor="correction_text" className="form-label">
                                2. Correction/Ground Truth (If INCORRECT or COMPLEX)
                            </label>
                            <textarea
                                id="correction_text"
                                name="correction_text"
                                value={feedback.correction_text || ''}
                                onChange={handleFeedbackChange}
                                placeholder="Provide the correct step-by-step solution or point out the factual error..."
                                className="form-textarea"
                            />
                        </div>

                        <button type="submit" className="submit-button">
                            <Send size={20} />
                            Submit HIL Data
                        </button>
                    </form>
                </div>
            )}
        </div>
    );
};

export default App;
