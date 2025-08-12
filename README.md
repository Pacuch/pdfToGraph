## 📦 Prerequisites & Installation Guide

Follow the instructions below to install the necessary tools on **Windows**, **Linux**, or **macOS**.

---

### 1️⃣ Tesseract OCR

| Platform | Installation Instructions |
| -------- | ------------------------- |
| **Windows** | 1. Download the installer from [Tesseract OCR v5.5.0](https://github.com/tesseract-ocr/tesseract/releases/tag/5.5.0#:~:text=Assets) <br> 2. Run the installer and complete the setup. <br> 3. Add `C:\Program Files\Tesseract-OCR` to your system `PATH`. <br> 4. Verify with: <br> ```bash tesseract --version ``` |
| **Linux** (Debian/Ubuntu) | ```bash sudo apt update && sudo apt install tesseract-ocr ``` <br> Verify with: <br> ```bash tesseract --version ``` |
| **macOS** | Using Homebrew: <br> ```bash brew install tesseract ``` <br> Verify with: <br> ```bash tesseract --version ``` |

---

### 2️⃣ Poppler (for PDF processing)

| Platform | Installation Instructions |
| -------- | ------------------------- |
| **Windows** | 1. Download ZIP from [Poppler v24.08.0-0](https://github.com/oschwartz10612/poppler-windows/releases/tag/v24.08.0-0#:~:text=Assets) <br> 2. Unzip to a folder, e.g., `C:\poppler` <br> 3. Add `C:\poppler\bin` to your `PATH` <br> 4. Verify with: <br> ```bash pdftoppm -v ``` |
| **Linux** (Debian/Ubuntu) | ```bash sudo apt update && sudo apt install poppler-utils ``` <br> Verify with: <br> ```bash pdftoppm -v ``` |
| **macOS** | Using Homebrew: <br> ```bash brew install poppler ``` <br> Verify with: <br> ```bash pdftoppm -v ``` |

---

### 3️⃣ Ollama (AI Model Runner)

| Platform | Installation Instructions |
| -------- | ------------------------- |
| **Windows, macOS, Linux** | 1. Download installer from [Ollama Download](https://ollama.com/download) <br> 2. Run the installer and follow instructions <br> 3. After installation, open your terminal or CMD and run: <br> ```bash ollama run llama2:7b ``` <br> 4. Verify installed models: <br> ```bash ollama list ``` |

#### Additional Resources:
- Ollama GitHub: [https://github.com/ollama/ollama](https://github.com/ollama/ollama)  
- Model Library: [https://ollama.com/library](https://ollama.com/library)
- Model Leaderboard: [Model Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard#/)  
---

### ✅ Final Verification

After completing all installations, run these commands to verify everything works:

```bash
tesseract --version
pdftoppm -v
ollama list
