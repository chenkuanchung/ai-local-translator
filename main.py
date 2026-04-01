import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import ollama 
from dotenv import load_dotenv  # 新增這行

# 載入 .env 檔案中的變數到系統環境中
load_dotenv() 

# 讀取環境變數 (此時完全由外部或 .env 決定，程式內不再需要寫死預設值)
TARGET_MODEL = os.getenv("MODEL_NAME", "qwen2.5:0.5b")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
ollama_client = ollama.Client(host=OLLAMA_HOST) # 建立共用的 Client

app = FastAPI(title="LocalTrans API")

# 1. 設定 CORS (允許前端網頁跨域呼叫 API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. 定義資料規格
class TranslationRequest(BaseModel):
    text: str
    target_language: str

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    model_used: str

class ConfigResponse(BaseModel):
    model_name: str

# 3. 翻譯 API 端點
@app.post("/api/v1/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    prompt = f"請將以下這段文字翻譯成 {request.target_language}。只需輸出翻譯結果，不要有任何其他解釋：\n{request.text}"
    try:
        response = ollama_client.chat(model=TARGET_MODEL, messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        return TranslationResponse(
            original_text=request.text,
            translated_text=response['message']['content'].strip(),
            model_used=TARGET_MODEL
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型推論失敗 ({TARGET_MODEL}): {str(e)}")

@app.get("/api/v1/config", response_model=ConfigResponse)
async def get_config():
    """
    讓前端在網頁載入時呼叫，取得目前後端的環境變數設定 (例如模型名稱)。
    """
    return ConfigResponse(model_name=TARGET_MODEL)

# 4. 託管前端靜態網頁 (必須放在最後面)
app.mount("/", StaticFiles(directory="static", html=True), name="static")