# 📚  LLM Based Text Summarization Service 

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
