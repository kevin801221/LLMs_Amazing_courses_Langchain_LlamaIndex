import json
import sys

def debug_json_file(json_file_path):
    """
    打印 JSON 文件的結構和內容
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"JSON 文件結構：")
        print(f"文件中的頂級鍵：{list(data.keys())}")
        
        for key, value in data.items():
            if isinstance(value, str):
                print(f"\n鍵 '{key}' 的值類型：字符串")
                print(f"值的長度：{len(value)}")
                print(f"值的前 100 個字符：{value[:100]}...")
            elif isinstance(value, dict):
                print(f"\n鍵 '{key}' 的值類型：字典")
                print(f"字典中的鍵：{list(value.keys())}")
            elif isinstance(value, list):
                print(f"\n鍵 '{key}' 的值類型：列表")
                print(f"列表長度：{len(value)}")
                if value and len(value) > 0:
                    print(f"第一個元素類型：{type(value[0]).__name__}")
            else:
                print(f"\n鍵 '{key}' 的值類型：{type(value).__name__}")
        
        return data
    except Exception as e:
        print(f"錯誤：{e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python debug_json.py <json文件路徑>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    debug_json_file(json_file_path)
