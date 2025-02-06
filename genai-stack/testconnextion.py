from neo4j import GraphDatabase

# 連接設定
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "kevin1221")    # 請先使用 Reset DBMS password 設定新密碼
DATABASE = "testing"

def test_movie_connection():
    try:
        driver = GraphDatabase.driver(URI, auth=AUTH)
        
        # 測試連接
        driver.verify_connectivity()
        print("✅ 連接成功")
        
        # 測試電影資料庫查詢
        with driver.session() as session:
            # 簡單查詢測試 - 獲取一部電影
            result = session.run("MATCH (m:Movie) RETURN m.title AS title LIMIT 1")
            movie = result.single()
            if movie:
                print(f"✅ 查詢成功：找到電影 '{movie['title']}'")
            else:
                print("⚠️ 資料庫可能是空的")
                
    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")
        
    finally:
        if 'driver' in locals():
            driver.close()
            print("🔒 連接已關閉")

if __name__ == "__main__":
    print("🎬 開始測試 Movie DBMS 連接...")
    test_movie_connection()