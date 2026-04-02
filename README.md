# ai-local-translator (AI.ing 智慧翻譯節點)

> 專為邊緣運算與微服務架構設計的輕量化地端 AI 翻譯系統。
> A scalable and decoupled AI translation microservice built with FastAPI and Ollama.

## 🏗️ 系統架構 (Architecture)

![Local AI Translator Microservices Architecture](./architecture.png)

本專案採用完整的**前後端分離與解耦微服務架構**，確保系統具備高度的靈活性與跨硬體移植性。

---

## 🌟 專案亮點 (Features)

* **微服務架構 (Microservices)**：前後端完全分離，後端 API 與 AI 推論引擎 (Ollama) 解耦，具備高度獨立擴展性。
* **零硬編碼 (Zero Hardcoding)**：嚴格遵守 12-Factor App 原則，模型名稱與連線設定完全由 `.env` 或系統環境變數動態注入。
* **自動化容器部署 (LLMOps)**：提供完整的 `docker-compose.yml`，內建 Init Container 實作模型開機自動下載 (Auto-pull)。
* **互動式 API 文件**：基於 FastAPI 自動生成 Swagger UI，方便前後端串接與測試。
* **純淨前端 (Vanilla JS)**：不依賴大型框架，實作輕量級非同步 (Async/Await) 資料流與 DOM 動態更新。

## 🛠️ 技術堆疊 (Tech Stack)

* **Backend**: Python 3.10, FastAPI, Pydantic, Uvicorn
* **AI Engine**: Ollama (預設使用 `qwen2.5:0.5b` 輕量模型)
* **Frontend**: HTML5, CSS3, Vanilla JavaScript
* **DevOps**: Docker, Docker Compose, python-dotenv

## 🚀 快速啟動 (Getting Started)

本專案提供兩種啟動方式，請根據您的部署環境進行選擇：

### 選項 A：本機開發模式 (適合硬體資源受限或已安裝 Ollama 者)

1.  **環境準備**：請確認本機已安裝 [Ollama](https://ollama.com/) 並啟動服務。
2.  **建立虛擬環境與安裝依賴**：
    ```bash
    python -m venv .venv
    
    # Windows 啟動: 
    .venv\Scripts\activate
    
    # Linux/Mac 啟動: 
    source .venv/bin/activate
    
    pip install -r requirements.txt
    ```
3.  **環境變數設定**：在專案根目錄建立 `.env` 檔案，並寫入以下設定：
    ```env
    MODEL_NAME=qwen2.5:0.5b
    OLLAMA_HOST=http://localhost:11434
    ```
4.  **啟動 FastAPI 伺服器**：
    ```bash
    uvicorn main:app --reload
    ```
5.  打開瀏覽器前往 `http://localhost:8000` 即可使用網頁服務。

### 選項 B：Docker 微服務模式 (適合純淨伺服器與生產環境部署)

本專案的 `docker-compose.yml` 將會自動啟動 API 伺服器、Ollama 推論伺服器，並透過 Init Container 自動下載指定的模型，達成一鍵自動化部署。

1.  **一鍵啟動 (使用預設模型 qwen2.5:0.5b)**：
    ```bash
    docker-compose up -d
    ```
2.  **動態切換模型 (由外部注入變數)**：
    ```bash
    MODEL_NAME=llama3 docker-compose up -d
    ```
3.  打開瀏覽器前往 `http://localhost:8000`。

## 📚 API 文件 (API Documentation)

伺服器啟動後，請前往以下網址查看由 FastAPI 自動生成的互動式 API 文件：
* **Swagger UI**: `http://localhost:8000/docs`
* **ReDoc**: `http://localhost:8000/redoc`

### 主要端點 (Endpoints)
* `GET /api/v1/config`：取得當前伺服器正在使用的 LLM 模型名稱。
* `POST /api/v1/translate`：接收文本與目標語言，回傳模型翻譯結果。

## 📄 授權條款 (License)

本專案採用 [MIT License](LICENSE) 授權。
