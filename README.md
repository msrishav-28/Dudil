# Dudil

**Dudil** is an emotion-aware chatbot that analyzes user input using a pre-trained emotion classification model and responds empathetically through Google’s Gemini AI. The application is designed to create contextual, emotionally intelligent conversations through a clean Streamlit-based interface.

---

## Features

* **Emotion Detection**: Classifies text into emotions such as joy, love, sadness, anger, fear, and surprise.
* **Empathetic AI Responses**: Dynamically adapts responses based on emotional state.
* **Conversation History**: Persists chats across sessions with support for browsing and management.
* **Confidence & Intensity Scoring**: Provides insight into how strongly emotions are detected.
* **Streamlit UI**: Modern web interface with expanders, metrics, and chat components.

---

## Tech Stack

* **Frontend**: Streamlit
* **Emotion Model**: Hugging Face Transformers (DistilBERT/DistilRoBERTa variants)
* **Conversational Model**: Google Gemini API
* **Storage**: JSON-based chat history
* **Language**: Python 3.7+

---

## Prerequisites

* Python 3.7 or higher
* Internet connection (for model/API)
* Google Gemini API Key

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/dudil.git
   cd dudil
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file:

   ```env
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODEL=gemini-pro
   DISTILBERT_MODEL=j-hartmann/emotion-english-distilroberta-base
   ```

4. **Obtain Gemini API Key**

   * Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   * Generate a key and add it to `.env`

---

## Usage

1. **Run the application**

   ```bash
   streamlit run app.py
   ```

2. **Interact**

   * Go to `http://localhost:8501`
   * Enter your message
   * View real-time emotion analysis and contextual replies

---

## How It Works

1. User input is analyzed using an emotion classification model.
2. The detected emotion and intensity are used to construct a contextual prompt.
3. Gemini AI generates a response tailored to the emotional context.
4. Results are displayed with emotion metrics and stored in history.

---

## Supported Emotions

| Emotion  | Intensity | Description                   |
| -------- | --------- | ----------------------------- |
| Joy      | 5/5       | Happiness and positive tone   |
| Love     | 5/5       | Affection and care            |
| Surprise | 4/5       | Sudden or unexpected reaction |
| Anger    | 2/5       | Frustration or irritation     |
| Fear     | 2/5       | Anxiety, nervousness          |
| Sadness  | 1/5       | Melancholy, disappointment    |

---

## Environment Variables

| Key                | Description                               |
| ------------------ | ----------------------------------------- |
| `GEMINI_API_KEY`   | Required for accessing the Gemini API     |
| `GEMINI_MODEL`     | Gemini model name (e.g., `gemini-pro`)    |
| `DISTILBERT_MODEL` | Hugging Face emotion classification model |

---

## Model Configuration

* **Temperature**: 0.7
* **Top-p**: 0.8
* **Top-k**: 40
* **Max Tokens**: 1024

---

## Chat Features

* Create and manage new conversations
* View and delete previous chats
* Clear all chat history
* Auto-save on session exit

---

## Troubleshooting

### Model Loading

* Ensure stable internet for downloading models
* Check disk space (\~500MB required)

### API Connection

* Verify that your API key is valid
* Ensure you have quota and correct permissions

### Chat History

* Ensure `chat_history.json` is writable
* Corrupted files are backed up automatically

---

## Contributing

1. Fork this repository
2. Create your branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to your branch: `git push origin feature/my-feature`
5. Open a pull request

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Credits

* [Hugging Face](https://huggingface.co/)
* [Google AI](https://ai.google/)
* [Streamlit](https://streamlit.io/)
* [j-hartmann](https://huggingface.co/j-hartmann) – Emotion Model

