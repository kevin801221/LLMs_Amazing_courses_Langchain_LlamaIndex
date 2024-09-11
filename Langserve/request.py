from langserve import RemoteRunnable

# 定義要連接的伺服器路徑
remote_chain = RemoteRunnable("http://localhost:8000/chain/")

# 發送一個翻譯請求，將 "hi" 翻譯成義大利語
response = remote_chain.invoke({"language": "italian", "text": "hi"})

# 打印翻譯結果
print(response)  # 預期結果： 'Ciao'
