# 📚 Text Summarization API with T5 Model

Welcome to the **Text Summarization API** project! This repository provides an end-to-end pipeline for training, deploying, and serving a text summarization model using **Hugging Face's T5 Transformer**. It also includes a user-friendly frontend to interact with the API. 🚀

---

## 📂 Project Structure

```plaintext
PythonProject [LLM]
├── .venv/                     # Virtual environment for dependencies
├── deployed_model/            # Directory for the deployed model (ONNX format)
├── Frontend/
│   ├── static/
│   │   ├── script.js          # Frontend interactivity
│   │   ├── style.css          # Styling for the web page
│   └── index.html             # Frontend HTML file
├── results/
│   ├── checkpoint-250/        # Intermediate training checkpoints
│   ├── checkpoint-375/        # Intermediate training checkpoints
│   └── summarization_model/   # Fine-tuned summarization model
├── tiny_summarization_model/
│   ├── Export.py              # Script to export the model to ONNX format
│   ├── Fastapi.py             # FastAPI-based backend server
│   ├── fine_tune.py           # Script for fine-tuning the model
│   └── Test.py                # Testing scripts for the API
```

---

## ✨ Features

- **Fine-tuning T5 Model**: Train a summarization model on custom data using `fine_tune.py`.
- **Export to ONNX**: Convert the trained model to ONNX format for optimized inference (`Export.py`).
- **FastAPI Backend**: RESTful API with endpoints for summarization and health checks.
- **Frontend Interface**: A simple and responsive web UI to interact with the API.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PyTorch
- Hugging Face Transformers
- FastAPI
- ONNX

### Installation

1. Clone the repository:
   ```bash
   https://github.com/Ashish032002/LLM_text_summarization.git
   cd text-summarization-api
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # For Linux/Mac
   .venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🐈️ How to Use

### 1⃣ Fine-tune the Model

Run the `fine_tune.py` script to train the T5 model on your dataset:
```bash
python tiny_summarization_model/fine_tune.py
```

### 2⃣ Export the Model

Convert the fine-tuned model to ONNX format for efficient inference:
```bash
python tiny_summarization_model/Export.py
```

### 3⃣ Start the API Server

Launch the FastAPI server:
```bash
python tiny_summarization_model/Fastapi.py
```

Visit `http://127.0.0.1:8000` to explore the API.

### 4⃣ Access the Frontend

Open `Frontend/index.html` in a browser to interact with the summarization API via a web interface.

---

## 🌐 API Endpoints

- **GET /**: Serve the frontend HTML.
- **GET /health**: Check the API's health status.
- **POST /summarize**: Submit text for summarization.
  - Request Body:
    ```json
    {
      "text": "Your text here...",
      "max_length": 150,
      "min_length": 40,
      "num_beams": 4
    }
    ```
  - Response:
    ```json
    {
      "summary": "Summarized text here...",
      "processing_time": 0.123
    }
    ```

---

## 🛠️ Technologies Used

- **Backend**: FastAPI, PyTorch, Hugging Face Transformers
- **Frontend**: HTML, CSS, JavaScript
- **Model Export**: ONNX

---

## 🗒 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 💡 Future Enhancements

- Add Docker support for easier deployment. 🐳
- Implement user authentication for the API.
- Improve frontend design with advanced styling frameworks.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request. 🙌

---

## 🌟 Acknowledgments

- Hugging Face for the T5 model and Transformers library.
- FastAPI for the lightweight and high-performance API framework.

---



