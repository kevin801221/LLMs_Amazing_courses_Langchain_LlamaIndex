import discord
from discord import app_commands
from discord.ext import commands
import my_commands.database
from my_commands.stock_price import stock_price
from my_commands.stock_news import stock_news
from my_commands.stock_value import stock_fundamental
from my_commands.stock_gpt import stock_gpt
from my_commands.dict_tabulate import dict_to_tabulate
import os
from my_commands.stock_prediction import predict_stock  # Add this line

token = os.getenv('TOKEN')

intents = discord.Intents.default()  # 取得預設的 intent
intents.message_content = True  # 啟用訊息內容

# 建立指令機器人
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
  print(f'{client.user} 已登入')
  try:
    synced = await client.tree.sync()
    print(f"{len(synced)}")
  except Exception as e:
    print(e)


# Add this new command
@client.tree.command(name="stock_predict", description="預測股票趨勢")
@app_commands.rename(stock_id="股票代碼")
@app_commands.describe(stock_id="輸入要預測的股票代碼, 如：2330")
async def dc_predict(interaction: discord.Interaction, stock_id: str):
  await interaction.response.defer()
  prediction = predict_stock(stock_id)
  await interaction.followup.send(prediction)


# 個股股價資料
@client.tree.command(name="stock_price", description="搜尋最近股價資料")
@app_commands.rename(stock_id="股票代碼")
@app_commands.describe(stock_id="輸入要查詢的股票代碼, 如：2330")
async def dc_stock(interaction: discord.Interaction, stock_id: str):
  data = stock_price(stock_id)
  stock_data = dict_to_tabulate(data)
  stock_block = "```\n" + stock_data + "```"
  title = f'{stock_id} 各日成交資訊'
  # 建立內嵌訊息
  embed = discord.Embed(title=title, description=stock_block)
  await interaction.response.send_message(embed=embed)


# 基本面資料
@client.tree.command(name="stock_value", description="搜尋季營收報表資料")
@app_commands.rename(stock_id="股票代碼")
@app_commands.describe(stock_id="輸入要查詢的股票代碼, 如：2330")
async def dc_value(interaction: discord.Interaction, stock_id: str):
  data = stock_fundamental(stock_id)
  stock_data = dict_to_tabulate(data)
  stock_block = "```\n" + stock_data + "```"
  title = f'{stock_id} 個股季營收報表資料'
  # 建立內嵌訊息
  embed = discord.Embed(title=title, description=stock_block)
  await interaction.response.send_message(embed=embed)


# 新聞資料
@client.tree.command(name="stock_news", description="搜尋新聞")
@app_commands.rename(stock_id="股票代碼")
@app_commands.describe(stock_id="輸入要查詢的股票代碼, 如：2330")
async def dc_news(interaction: discord.Interaction, stock_id: str):
  data = stock_news(stock_id, add_content=False)
  stock_data = dict_to_tabulate(data)
  stock_block = "```\n" + stock_data + "```"
  title = f'{stock_id} 新聞資料'
  # 建立內嵌訊息
  embed = discord.Embed(title=title, description=stock_block)
  await interaction.response.send_message(embed=embed)


@client.tree.command(name="stock_gpt", description="讓 AI 來分析")
@app_commands.rename(stock_id="股票代碼")
@app_commands.describe(stock_id="輸入要查詢的股票代碼, 如：2330")
async def dc_ai(interaction: discord.Interaction, stock_id: str):
  await interaction.response.defer()
  gpt_reply = stock_gpt(stock_id)

  # 將回覆分割成多個消息,以避免超過 Discord 的消息長度限制
  max_length = 1900  # Discord 消息的最大長度略低於 2000
  messages = []
  for i in range(0, len(gpt_reply), max_length):
    messages.append(gpt_reply[i:i+max_length])

  for message in messages:
    await interaction.followup.send(message)


client.run(token)
