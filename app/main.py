from fastapi import FastAPI, File, UploadFile, HTTPException
import json
from app.balance_core import calculate_json_data

app = FastAPI(title="Balance Calculator")

@app.post("/calc")
async def calculate_balance(file: UploadFile = File(...)):
    # Проверка расширения файла
    if not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="Файл должен быть в формате JSON")
    
    # Чтение и парсинг файла
    try:
        # Чтение и парсинг файла
        content = await file.read()
        json_data = json.loads(content)     
        
        if not isinstance(json_data, dict) or 'days' not in json_data:
            raise HTTPException(status_code=400, detail="JSON должен содержать ключ 'numbers'")
        
        if not isinstance(json_data['days'], list):
            raise HTTPException(status_code=400, detail="'days' должен быть списком")
        
        # ВЫЗОВ ФУНКЦИИ: передаём распарсенный JSON → получаем готовый результат
        result_json = calculate_json_data(json_data)
    
        return result_json
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Некорректный формат JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки: {str(e)}")
    finally:
        await file.close()

@app.get("/")
async def root():
    return {"message": "Balance Calculator", "endpoint": "/calc"}