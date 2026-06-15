# 🤖 AI Customer Support Bot — Visual Builders

[![Python Version](https://img.shields.io/badge/Python-3.14%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Llama 3.3](https://img.shields.io/badge/LLM-Llama%203.3%20(70B)-orange?logo=meta&logoColor=white)](https://meta.ai/)
[![Groq API](https://img.shields.io/badge/Inference-Groq%20Cloud-00F?logo=groq&logoColor=white)](https://groq.com/)

An intelligent, context-aware chatbot customized for **Visual Builders** (a digital solutions and AI automation agency). Built using the advanced **Llama 3.3 (70B parameter) model** accessed via the high-speed **Groq Cloud API**, the bot leverages a local structured knowledge base (`bot-context.json`) to deliver friendly, professional, real-time responses to customer queries about services, pricing, and FAQs.

---

## 🌟 Key Features

*   **Real-time Streaming Response:** Renders response chunks token-by-token on the UI using Streamlit's streaming capabilities, ensuring an interactive and responsive chat experience.
*   **Dynamic Business Context:** Loads company information (identity, growth metrics, services, pricing tiers, and FAQs) directly from a local database file (`bot-context.json`) and injects it into the LLM system prompt.
*   **Intelligent Conversational Agent:** Configured with a dedicated persona to represent Visual Builders professionally, provide accurate support, and fall back to email contact (`buildersvisual@gmail.com`) for complex inquiries.
*   **Sleek Interface:** Modern chat UI utilizing Streamlit's native chat input and message components.

---

## 📐 System Architecture

The architecture is divided into three layers:
1.  **Frontend (Streamlit):** Captures user queries, renders chat histories, and streams token completions.
2.  **Backend Logic (Python):** Orchestrates context loading from `bot-context.json`, wraps conversation history, and handles API streams.
3.  **AI Engine (Groq Cloud API):** Runs inference on the Llama 3.3 model.

### Architecture Representation

![System Architecture Diagram](architecture.png)
*Figure: High-Level Architecture Diagram*

---

## 📂 Repository Structure

```directory
AI-Customer-Suppot-Bot-SystemDesign/
├── python-streamlit-code/            # Main application directory
│   ├── app.py                        # Streamlit UI & Page layout
│   ├── bot_logic.py                  # SupportBot class & Groq API client
│   ├── bot-context.json              # Local business knowledge base
│   └── requirements.txt              # Application dependencies
├── README.md                         # Project documentation for GitHub
├── Project_Documentation.md          # Full detailed system documentation
├── Project_Documentation.pdf         # Compiled PDF documentation
├── architecture.png                  # High-level architecture diagram
├── architecture_high_fidelity.png    # Enterprise integration architecture diagram
└── architecture_low_fidelity.png     # Component wireframe sketch
```

---

## 🚀 Getting Started

Follow these steps to run the application locally on your machine:

### Prerequisites
*   Python 3.10 or higher
*   A Groq Cloud API Key (get one from the [Groq Console](https://console.groq.com/))

### Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/[YOUR_USERNAME]/AI-Customer-Support-Bot.git
    cd AI-Customer-Support-Bot
    ```

2.  **Navigate into the Code Directory:**
    ```bash
    cd python-streamlit-code
    ```

3.  **Create and Activate a Virtual Environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure Environment Variables:**
    Create a `.env` file in the `python-streamlit-code/` directory and add your API key:
    ```env
    GROQ_API_KEY=gsk_your_groq_api_key_here
    ```

6.  **Run the Server:**
    ```bash
    streamlit run app.py
    ```
    This will launch the application and open it automatically in your default browser at `http://localhost:8501`.

---

## 💻 Code Overview

The bot logic is encapsulated in the `SupportBot` class, which constructs the system prompt dynamically from the knowledge base:

```python
# python-streamlit-code/bot_logic.py (abbreviated)
class SupportBot:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.context = self.load_context()
        self.system_prompt = f"""
        You are a helpful customer support bot for Visual Builders...
        Company Details: {json.dumps(self.context)}
        """

    def stream_response(self, user_query, chat_history):
        # Calls Groq completions API with stream=True
        # Yields tokens chunk-by-chunk
```

Streamlit reads this stream and updates the interface in real-time:

```python
# python-streamlit-code/app.py (abbreviated)
with st.chat_message("assistant"):
    placeholder = st.empty()
    full_response = ""
    for chunk in bot.stream_response(prompt, history):
        full_response += chunk
        placeholder.markdown(full_response + "▌")
    placeholder.markdown(full_response)
```

---

## 🔮 Future Roadmap

*   **RAG Integration:** Connect to vector databases for dynamic document querying.
*   **Human Handoff:** Seamless support handoff to slack alerts or ticketing systems.
*   **Analytics Dashboard:** Monitor customer sentiment and chatbot response quality.
*   **Multi-channel:** Deploy endpoints to Slack, Discord, or WhatsApp.
