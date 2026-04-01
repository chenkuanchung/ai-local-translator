// --- 1. 定義：在網頁載入時，更新模型狀態的函式 ---
async function updateModelStatus() {
    const modelSpan = document.getElementById('current-model');
    try {
        // 發送 GET 請求取得配置資訊
        const response = await fetch('/api/v1/config');
        if (!response.ok) throw new Error('無法連線至設定 API');
        
        const data = await response.json();
        
        // 更新網頁 HTML
        modelSpan.textContent = data.model_name;
        // 可以視情況移除 loading 樣式 (如有)
    } catch (error) {
        console.error("取得模型資訊失敗:", error);
        modelSpan.textContent = "未知 (後端連線異常)";
        modelSpan.style.color = 'red'; // 顯示錯誤視覺
    }
}

// --- 2. 監聽事件：當網頁 DOM 結構載入完成時，立刻執行上述函式 ---
document.addEventListener('DOMContentLoaded', updateModelStatus);

// --- 3. 翻譯按鈕 ---
document.getElementById('translate-btn').addEventListener('click', async () => {
    const sourceText = document.getElementById('source-text').value;
    const targetLang = document.getElementById('target-lang').value;
    const resultText = document.getElementById('result-text');
    const loading = document.getElementById('loading');

    if (!sourceText.trim()) {
        alert("請輸入文字！");
        return;
    }

    loading.classList.remove('hidden');
    resultText.value = "";

    try {
        const response = await fetch('/api/v1/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: sourceText,
                target_language: targetLang
            })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const data = await response.json();
        resultText.value = data.translated_text;
    } catch (error) {
        resultText.value = "系統錯誤，請確認後端 API 是否正常運作。\n" + error.message;
    } finally {
        loading.classList.add('hidden');
    }
});