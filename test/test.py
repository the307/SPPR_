import requests
import json
import subprocess
import sys
from pathlib import Path

def export_to_excel(
    *,
    script_name: str = "json_to_excel_balance.py",
) -> None:
    """Конвертирует `output.json` в Excel через `json_to_excel_balance.py`.

    Скрипт сам читает `data_output.json` (если есть) иначе `output.json`,
    и сохраняет файл вида `balance_<date>[_auto].xlsx`.
    """
    script_path = Path(__file__).resolve().parent / script_name
    if not script_path.exists():
        raise FileNotFoundError(f"Не найден скрипт для экспорта в Excel: {script_path}")
    subprocess.run([sys.executable, str(script_path)], check=True, cwd=str(script_path.parent))


url = "http://localhost:8000/calc"

with open('data_input.json', 'rb') as f:
    files = {'file': ('data_input.json', f, 'application/json')}
    response = requests.post(url, files=files)


result = response.json()
test_dir = Path(__file__).resolve().parent
with open(test_dir / "data_output.json", 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

export_to_excel()
