from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

import chainlit as cl

load_dotenv()


@cl.on_chat_start
async def start():
    files = None
    # 等待用户上传文件
    while files is None:
        files = await cl.AskFileMessage(
            content='请上传你要提问的PDF文件',
            # 这里只运行 PDF 的文件
            accept=["application/pdf"],
            max_size_mb=3
        ).send()

    _file = files[0]

    # 文件还没加载成功之前显示一个消息提示
    msg = cl.Message(content=f'正在处理处理: `{_file.name}`...')
    await msg.send()

    # 将上传的文件保存到服务器本地
    file_path = f'./tmp/{_file.name}'
    with open(file_path, 'wb') as f:
        f.write(_file.content)

    # 加载 PDF 文档
    docs = PyMuPDFLoader(file_path).load()

    # 分割文档
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=100
    )
    split_docs = text_splitter.split_documents(docs)

    # 创建 Chroma 存储
    embeddings = OpenAIEmbeddings()
    docsearch = await cl.make_async(Chroma.from_documents)(
        split_docs, embeddings, collection_name=_file.name
    )
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        output_key='answer',
        return_messages=True,
    )

    # 基于 Chroma 存储创建一个问答链
    chain = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(
            temperature=0,
            model='gpt-4-1106-preview',
        ),
        chain_type='stuff',
        retriever=docsearch.as_retriever(),
        memory=memory,
        # 因为我们需要将搜索到的结果当做来源展示到页面上，
        # 所以这里需要设置为 True
        return_source_documents=True,
    )

    msg.content = f'`{_file.name}` 处理完成，请开始你的问答。'
    await msg.update()

    # 将 chain 对象保存到用户 session 中
    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message: cl.Message):
    # 获取在初始化时存储的 Chain 对象
    chain = cl.user_session.get('chain')

    # AsyncLangchainCallbackHandle 会将执行时中间步骤实时显示到聊天列表中
    cb = cl.AsyncLangchainCallbackHandler()
    # 进行检索
    res = await chain.acall(message.content, callbacks=[cb])
    answer = res['answer']
    source_documents = res['source_documents']

    # 将检索到的内容一并显示到界面上
    text_elements = []
    if source_documents:
        for index, source_doc in enumerate(source_documents):
            source_name = f'来源{index + 1}'
            text_elements.append(
                cl.Text(content=source_doc.page_content, name=source_name)
            )
        source_names = [text_el.name for text_el in text_elements]

        if source_names:
            answer += f'\n\n来源: {", ".join(source_names)}'
        else:
            answer += '\n\n来源未找到'

    await cl.Message(content=answer, elements=text_elements).send()
