
# 檔案: vqa_dpo_processing.py
# 說明: 此程式處理 VQA 資料集以進行 DPO（直接偏好優化），並將其格式化以供模型訓練使用。

import pandas as pd
from datasets import Dataset, DatasetDict
import os
import requests
from pathlib import Path

def download_file(url: str, dest_path: Path) -> None:
    '''
    從給定的 URL 下載檔案並將其儲存至指定路徑。
    
    參數:
    - url (str): 要下載的檔案的 URL。
    - dest_path (Path): 要儲存檔案的本地路徑。
    '''
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)
        print(f"檔案下載至 {dest_path}")
    else:
        print(f"下載失敗, URL: {url}. 狀態碼: {response.status_code}")

def load_and_process_vqa_dpo(csv_path: Path, train_df: pd.DataFrame, test_df: pd.DataFrame) -> DatasetDict:
    '''
    處理 VQA 資料集以進行 DPO（直接偏好優化）。
    從 CSV 檔案中加入 rejected 標籤並將其格式化供模型訓練。

    參數:
    - csv_path (Path): 包含 rejected 標籤的 CSV 檔案路徑。
      CSV 檔案應包含 'rejected' 欄位，值為 0（選擇）或 1（拒絕）。
    - train_df (pd.DataFrame): 包含訓練資料的 DataFrame。
      預期欄位: ['image', 'question', 'answer']
    - test_df (pd.DataFrame): 包含測試資料的 DataFrame。
      預期欄位: ['image', 'question', 'answer']

    回傳:
    - DatasetDict: Hugging Face 格式的 DatasetDict 物件，包含訓練與測試資料。
    '''
    
    # 從 CSV 檔案中載入 rejected 標籤
    df_rejected = pd.read_csv(csv_path)
    
    # 確保 rejected 欄位正確地加入到訓練和測試資料集
    train_df['rejected'] = df_rejected['rejected'][:len(train_df)]
    test_df['rejected'] = df_rejected['rejected'][len(train_df):]

    # 將原始答案列（answer）作為被選擇的答案（chosen）
    train_df['chosen'] = train_df['answer']
    test_df['chosen'] = test_df['answer']

    # 僅保留所需欄位
    train_df = train_df[['image', 'question', 'chosen', 'rejected']]
    test_df = test_df[['image', 'question', 'chosen', 'rejected']]

    # 將 DataFrame 轉換為 Hugging Face 的 Dataset 格式
    train_dataset = Dataset.from_pandas(train_df)
    test_dataset = Dataset.from_pandas(test_df)

    # 回傳 DatasetDict 物件
    return DatasetDict({'train': train_dataset, 'test': test_dataset})

def save_dataset(dataset_dict: DatasetDict, output_path: Path) -> None:
    '''
    將 DatasetDict 儲存至磁碟。

    參數:
    - dataset_dict (DatasetDict): 要儲存的資料集，包含訓練與測試資料。
    - output_path (Path): 要儲存資料集的路徑。
    '''
    dataset_dict.save_to_disk(output_path)
    print(f"資料集已儲存至 {output_path}")

if __name__ == "__main__":
    # 使用相對路徑下載檔案
    csv_url = "https://example.com/DPO_VQA_RAD.csv"  # 替換為實際 URL
    local_csv_path = Path('data/DPO_VQA_RAD.csv')

    # 如果檔案尚未下載，則下載 CSV 檔案
    if not local_csv_path.exists():
        download_file(csv_url, local_csv_path)
    
    # 使用實際資料替換此處的 DataFrame
    train_df = pd.DataFrame({'image': [], 'question': [], 'answer': []})  # 替換為實際資料
    test_df = pd.DataFrame({'image': [], 'question': [], 'answer': []})   # 替換為實際資料
    
    # 處理資料集以進行 DPO
    dpo_dataset = load_and_process_vqa_dpo(local_csv_path, train_df, test_df)
    
    # 儲存處理後的資料集
    save_dataset(dpo_dataset, Path('output/formatted_DPO_VQA_RAD'))
