{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Vector stores and retrievers\n",
    "This video tutorial will familiarize you with LangChain's vector store and retriever abstractions. These abstractions are designed to support retrieval of data-- from (vector) databases and other sources-- for integration with LLM workflows. They are important for applications that fetch data to be reasoned over as part of model inference, as in the case of retrieval-augmented generation.\n",
    "\n",
    "We will cover \n",
    "- Documents\n",
    "- Vector stores\n",
    "- Retrievers\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "ERROR: Could not find a version that satisfies the requirement lnagchain (from versions: none)\n",
      "ERROR: No matching distribution found for lnagchain\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: langchain-chroma in e:\\udemy final\\langchain\\venv\\lib\\site-packages (0.1.1)\n",
      "Requirement already satisfied: chromadb<0.6.0,>=0.4.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain-chroma) (0.5.3)\n",
      "Requirement already satisfied: fastapi<1,>=0.95.2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain-chroma) (0.111.0)\n",
      "Requirement already satisfied: langchain-core<0.3,>=0.1.40 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain-chroma) (0.2.10)\n",
      "Requirement already satisfied: numpy<2,>=1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain-chroma) (1.26.4)\n",
      "Requirement already satisfied: build>=1.0.3 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.2.1)\n",
      "Requirement already satisfied: requests>=2.28 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (2.31.0)\n",
      "Requirement already satisfied: pydantic>=1.9 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.10.13)\n",
      "Requirement already satisfied: chroma-hnswlib==0.7.3 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.7.3)\n",
      "Requirement already satisfied: uvicorn>=0.18.3 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from uvicorn[standard]>=0.18.3->chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.30.1)\n",
      "Requirement already satisfied: posthog>=2.4.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (3.5.0)\n",
      "Requirement already satisfied: typing-extensions>=4.5.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (4.12.2)\n",
      "Requirement already satisfied: onnxruntime>=1.14.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.18.0)\n",
      "Requirement already satisfied: opentelemetry-api>=1.2.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.25.0)\n",
      "Requirement already satisfied: opentelemetry-exporter-otlp-proto-grpc>=1.2.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.25.0)\n",
      "Requirement already satisfied: opentelemetry-instrumentation-fastapi>=0.41b0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.46b0)\n",
      "Requirement already satisfied: opentelemetry-sdk>=1.2.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.25.0)\n",
      "Requirement already satisfied: tokenizers>=0.13.2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.19.1)\n",
      "Requirement already satisfied: pypika>=0.48.9 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.48.9)\n",
      "Requirement already satisfied: tqdm>=4.65.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (4.66.4)\n",
      "Requirement already satisfied: overrides>=7.3.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (7.7.0)\n",
      "Requirement already satisfied: importlib-resources in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (6.4.0)\n",
      "Requirement already satisfied: grpcio>=1.58.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.64.1)\n",
      "Requirement already satisfied: bcrypt>=4.0.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (4.1.3)\n",
      "Requirement already satisfied: typer>=0.9.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.12.3)\n",
      "Requirement already satisfied: kubernetes>=28.1.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (30.1.0)\n",
      "Requirement already satisfied: tenacity>=8.2.3 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (8.4.1)\n",
      "Requirement already satisfied: PyYAML>=6.0.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (6.0.1)\n",
      "Requirement already satisfied: mmh3>=4.0.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (4.1.0)\n",
      "Requirement already satisfied: orjson>=3.9.12 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (3.10.5)\n",
      "Requirement already satisfied: httpx>=0.27.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.27.0)\n",
      "Requirement already satisfied: starlette<0.38.0,>=0.37.2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from fastapi<1,>=0.95.2->langchain-chroma) (0.37.2)\n",
      "Requirement already satisfied: fastapi-cli>=0.0.2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from fastapi<1,>=0.95.2->langchain-chroma) (0.0.4)\n",
      "Requirement already satisfied: jinja2>=2.11.2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from fastapi<1,>=0.95.2->langchain-chroma) (3.1.4)\n",
      "Requirement already satisfied: python-multipart>=0.0.7 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from fastapi<1,>=0.95.2->langchain-chroma) (0.0.9)\n",
      "Requirement already satisfied: ujson!=4.0.2,!=4.1.0,!=4.2.0,!=4.3.0,!=5.0.0,!=5.1.0,>=4.0.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from fastapi<1,>=0.95.2->langchain-chroma) (5.10.0)\n",
      "Requirement already satisfied: email_validator>=2.0.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from fastapi<1,>=0.95.2->langchain-chroma) (2.2.0)\n",
      "Requirement already satisfied: jsonpatch<2.0,>=1.33 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain-core<0.3,>=0.1.40->langchain-chroma) (1.33)\n",
      "Requirement already satisfied: langsmith<0.2.0,>=0.1.75 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain-core<0.3,>=0.1.40->langchain-chroma) (0.1.77)\n",
      "Requirement already satisfied: packaging<25,>=23.2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain-core<0.3,>=0.1.40->langchain-chroma) (24.1)\n",
      "Requirement already satisfied: pyproject_hooks in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from build>=1.0.3->chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.1.0)\n",
      "Requirement already satisfied: colorama in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from build>=1.0.3->chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.4.6)\n",
      "Requirement already satisfied: importlib-metadata>=4.6 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from build>=1.0.3->chromadb<0.6.0,>=0.4.0->langchain-chroma) (7.1.0)\n",
      "Requirement already satisfied: tomli>=1.1.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from build>=1.0.3->chromadb<0.6.0,>=0.4.0->langchain-chroma) (2.0.1)\n",
      "Requirement already satisfied: dnspython>=2.0.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from email_validator>=2.0.0->fastapi<1,>=0.95.2->langchain-chroma) (2.6.1)\n",
      "Requirement already satisfied: idna>=2.0.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from email_validator>=2.0.0->fastapi<1,>=0.95.2->langchain-chroma) (3.7)\n",
      "Requirement already satisfied: anyio in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from httpx>=0.27.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (4.4.0)\n",
      "Requirement already satisfied: certifi in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from httpx>=0.27.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (2024.6.2)\n",
      "Requirement already satisfied: httpcore==1.* in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from httpx>=0.27.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.0.5)\n",
      "Requirement already satisfied: sniffio in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from httpx>=0.27.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.3.1)\n",
      "Requirement already satisfied: h11<0.15,>=0.13 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from httpcore==1.*->httpx>=0.27.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.14.0)\n",
      "Requirement already satisfied: MarkupSafe>=2.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from jinja2>=2.11.2->fastapi<1,>=0.95.2->langchain-chroma) (2.1.5)\n",
      "Requirement already satisfied: jsonpointer>=1.9 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from jsonpatch<2.0,>=1.33->langchain-core<0.3,>=0.1.40->langchain-chroma) (3.0.0)\n",
      "Requirement already satisfied: six>=1.9.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from kubernetes>=28.1.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.16.0)\n",
      "Requirement already satisfied: python-dateutil>=2.5.3 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from kubernetes>=28.1.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (2.9.0.post0)\n",
      "Requirement already satisfied: google-auth>=1.0.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from kubernetes>=28.1.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (2.30.0)\n",
      "Requirement already satisfied: websocket-client!=0.40.0,!=0.41.*,!=0.42.*,>=0.32.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from kubernetes>=28.1.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.8.0)\n",
      "Requirement already satisfied: requests-oauthlib in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from kubernetes>=28.1.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (2.0.0)\n",
      "Requirement already satisfied: oauthlib>=3.2.2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from kubernetes>=28.1.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (3.2.2)\n",
      "Requirement already satisfied: urllib3>=1.24.2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from kubernetes>=28.1.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (2.2.2)\n",
      "Requirement already satisfied: coloredlogs in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from onnxruntime>=1.14.1->chromadb<0.6.0,>=0.4.0->langchain-chroma) (15.0.1)\n",
      "Requirement already satisfied: flatbuffers in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from onnxruntime>=1.14.1->chromadb<0.6.0,>=0.4.0->langchain-chroma) (24.3.25)\n",
      "Requirement already satisfied: protobuf in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from onnxruntime>=1.14.1->chromadb<0.6.0,>=0.4.0->langchain-chroma) (4.25.3)\n",
      "Requirement already satisfied: sympy in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from onnxruntime>=1.14.1->chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.12.1)\n",
      "Requirement already satisfied: deprecated>=1.2.6 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from opentelemetry-api>=1.2.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.2.14)\n",
      "Requirement already satisfied: googleapis-common-protos~=1.52 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from opentelemetry-exporter-otlp-proto-grpc>=1.2.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.63.1)\n",
      "Requirement already satisfied: opentelemetry-exporter-otlp-proto-common==1.25.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from opentelemetry-exporter-otlp-proto-grpc>=1.2.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.25.0)\n",
      "Requirement already satisfied: opentelemetry-proto==1.25.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from opentelemetry-exporter-otlp-proto-grpc>=1.2.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.25.0)\n",
      "Requirement already satisfied: opentelemetry-instrumentation-asgi==0.46b0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from opentelemetry-instrumentation-fastapi>=0.41b0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.46b0)\n",
      "Requirement already satisfied: opentelemetry-instrumentation==0.46b0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from opentelemetry-instrumentation-fastapi>=0.41b0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.46b0)\n",
      "Requirement already satisfied: opentelemetry-semantic-conventions==0.46b0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from opentelemetry-instrumentation-fastapi>=0.41b0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.46b0)\n",
      "Requirement already satisfied: opentelemetry-util-http==0.46b0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from opentelemetry-instrumentation-fastapi>=0.41b0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.46b0)\n",
      "Requirement already satisfied: setuptools>=16.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from opentelemetry-instrumentation==0.46b0->opentelemetry-instrumentation-fastapi>=0.41b0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (69.5.1)\n",
      "Requirement already satisfied: wrapt<2.0.0,>=1.0.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from opentelemetry-instrumentation==0.46b0->opentelemetry-instrumentation-fastapi>=0.41b0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.16.0)\n",
      "Requirement already satisfied: asgiref~=3.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from opentelemetry-instrumentation-asgi==0.46b0->opentelemetry-instrumentation-fastapi>=0.41b0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (3.8.1)\n",
      "Requirement already satisfied: monotonic>=1.5 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from posthog>=2.4.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.6)\n",
      "Requirement already satisfied: backoff>=1.10.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from posthog>=2.4.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (2.2.1)\n",
      "Requirement already satisfied: charset-normalizer<4,>=2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from requests>=2.28->chromadb<0.6.0,>=0.4.0->langchain-chroma) (3.3.2)\n",
      "Requirement already satisfied: huggingface-hub<1.0,>=0.16.4 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from tokenizers>=0.13.2->chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.23.4)\n",
      "Requirement already satisfied: click>=8.0.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from typer>=0.9.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (8.1.7)\n",
      "Requirement already satisfied: shellingham>=1.3.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from typer>=0.9.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.5.4)\n",
      "Requirement already satisfied: rich>=10.11.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from typer>=0.9.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (13.7.1)\n",
      "Requirement already satisfied: httptools>=0.5.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from uvicorn[standard]>=0.18.3->chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.6.1)\n",
      "Requirement already satisfied: python-dotenv>=0.13 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from uvicorn[standard]>=0.18.3->chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.0.1)\n",
      "Requirement already satisfied: watchfiles>=0.13 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from uvicorn[standard]>=0.18.3->chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.22.0)\n",
      "Requirement already satisfied: websockets>=10.4 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from uvicorn[standard]>=0.18.3->chromadb<0.6.0,>=0.4.0->langchain-chroma) (12.0)\n",
      "Requirement already satisfied: exceptiongroup>=1.0.2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from anyio->httpx>=0.27.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.2.1)\n",
      "Requirement already satisfied: cachetools<6.0,>=2.0.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from google-auth>=1.0.1->kubernetes>=28.1.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (5.3.3)\n",
      "Requirement already satisfied: pyasn1-modules>=0.2.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from google-auth>=1.0.1->kubernetes>=28.1.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.4.0)\n",
      "Requirement already satisfied: rsa<5,>=3.1.4 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from google-auth>=1.0.1->kubernetes>=28.1.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (4.9)\n",
      "Requirement already satisfied: filelock in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from huggingface-hub<1.0,>=0.16.4->tokenizers>=0.13.2->chromadb<0.6.0,>=0.4.0->langchain-chroma) (3.15.4)\n",
      "Requirement already satisfied: fsspec>=2023.5.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from huggingface-hub<1.0,>=0.16.4->tokenizers>=0.13.2->chromadb<0.6.0,>=0.4.0->langchain-chroma) (2024.6.0)\n",
      "Requirement already satisfied: zipp>=0.5 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from importlib-metadata>=4.6->build>=1.0.3->chromadb<0.6.0,>=0.4.0->langchain-chroma) (3.19.2)\n",
      "Requirement already satisfied: markdown-it-py>=2.2.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from rich>=10.11.0->typer>=0.9.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (3.0.0)\n",
      "Requirement already satisfied: pygments<3.0.0,>=2.13.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from rich>=10.11.0->typer>=0.9.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (2.18.0)\n",
      "Requirement already satisfied: humanfriendly>=9.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from coloredlogs->onnxruntime>=1.14.1->chromadb<0.6.0,>=0.4.0->langchain-chroma) (10.0)\n",
      "Requirement already satisfied: mpmath<1.4.0,>=1.1.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from sympy->onnxruntime>=1.14.1->chromadb<0.6.0,>=0.4.0->langchain-chroma) (1.3.0)\n",
      "Requirement already satisfied: pyreadline3 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from humanfriendly>=9.1->coloredlogs->onnxruntime>=1.14.1->chromadb<0.6.0,>=0.4.0->langchain-chroma) (3.4.1)\n",
      "Requirement already satisfied: mdurl~=0.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from markdown-it-py>=2.2.0->rich>=10.11.0->typer>=0.9.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.1.2)\n",
      "Requirement already satisfied: pyasn1<0.7.0,>=0.4.6 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from pyasn1-modules>=0.2.1->google-auth>=1.0.1->kubernetes>=28.1.0->chromadb<0.6.0,>=0.4.0->langchain-chroma) (0.6.0)\n",
      "Requirement already satisfied: langchain_groq in e:\\udemy final\\langchain\\venv\\lib\\site-packages (0.1.6)\n",
      "Requirement already satisfied: groq<1,>=0.4.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain_groq) (0.9.0)\n",
      "Requirement already satisfied: langchain-core<0.3,>=0.2.2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain_groq) (0.2.10)\n",
      "Requirement already satisfied: anyio<5,>=3.5.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from groq<1,>=0.4.1->langchain_groq) (4.4.0)\n",
      "Requirement already satisfied: distro<2,>=1.7.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from groq<1,>=0.4.1->langchain_groq) (1.9.0)\n",
      "Requirement already satisfied: httpx<1,>=0.23.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from groq<1,>=0.4.1->langchain_groq) (0.27.0)\n",
      "Requirement already satisfied: pydantic<3,>=1.9.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from groq<1,>=0.4.1->langchain_groq) (1.10.13)\n",
      "Requirement already satisfied: sniffio in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from groq<1,>=0.4.1->langchain_groq) (1.3.1)\n",
      "Requirement already satisfied: typing-extensions<5,>=4.7 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from groq<1,>=0.4.1->langchain_groq) (4.12.2)\n",
      "Requirement already satisfied: PyYAML>=5.3 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain-core<0.3,>=0.2.2->langchain_groq) (6.0.1)\n",
      "Requirement already satisfied: jsonpatch<2.0,>=1.33 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain-core<0.3,>=0.2.2->langchain_groq) (1.33)\n",
      "Requirement already satisfied: langsmith<0.2.0,>=0.1.75 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain-core<0.3,>=0.2.2->langchain_groq) (0.1.77)\n",
      "Requirement already satisfied: packaging<25,>=23.2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain-core<0.3,>=0.2.2->langchain_groq) (24.1)\n",
      "Requirement already satisfied: tenacity!=8.4.0,<9.0.0,>=8.1.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain-core<0.3,>=0.2.2->langchain_groq) (8.4.1)\n",
      "Requirement already satisfied: idna>=2.8 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from anyio<5,>=3.5.0->groq<1,>=0.4.1->langchain_groq) (3.7)\n",
      "Requirement already satisfied: exceptiongroup>=1.0.2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from anyio<5,>=3.5.0->groq<1,>=0.4.1->langchain_groq) (1.2.1)\n",
      "Requirement already satisfied: certifi in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from httpx<1,>=0.23.0->groq<1,>=0.4.1->langchain_groq) (2024.6.2)\n",
      "Requirement already satisfied: httpcore==1.* in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from httpx<1,>=0.23.0->groq<1,>=0.4.1->langchain_groq) (1.0.5)\n",
      "Requirement already satisfied: h11<0.15,>=0.13 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from httpcore==1.*->httpx<1,>=0.23.0->groq<1,>=0.4.1->langchain_groq) (0.14.0)\n",
      "Requirement already satisfied: jsonpointer>=1.9 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from jsonpatch<2.0,>=1.33->langchain-core<0.3,>=0.2.2->langchain_groq) (3.0.0)\n",
      "Requirement already satisfied: orjson<4.0.0,>=3.9.14 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langsmith<0.2.0,>=0.1.75->langchain-core<0.3,>=0.2.2->langchain_groq) (3.10.5)\n",
      "Requirement already satisfied: requests<3,>=2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langsmith<0.2.0,>=0.1.75->langchain-core<0.3,>=0.2.2->langchain_groq) (2.31.0)\n",
      "Requirement already satisfied: charset-normalizer<4,>=2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from requests<3,>=2->langsmith<0.2.0,>=0.1.75->langchain-core<0.3,>=0.2.2->langchain_groq) (3.3.2)\n",
      "Requirement already satisfied: urllib3<3,>=1.21.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from requests<3,>=2->langsmith<0.2.0,>=0.1.75->langchain-core<0.3,>=0.2.2->langchain_groq) (2.2.2)\n"
     ]
    }
   ],
   "source": [
    "!pip install langchain\n",
    "!pip install langchain-chroma\n",
    "!pip install langchain_groq"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Documents\n",
    "LangChain implements a Document abstraction, which is intended to represent a unit of text and associated metadata. It has two attributes:\n",
    "\n",
    "- page_content: a string representing the content;\n",
    "- metadata: a dict containing arbitrary metadata.\n",
    "The metadata attribute can capture information about the source of the document, its relationship to other documents, and other information. Note that an individual Document object often represents a chunk of a larger document.\n",
    "\n",
    "Let's generate some sample documents:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "from langchain_core.documents import Document\n",
    "\n",
    "documents = [\n",
    "    Document(\n",
    "        page_content=\"Dogs are great companions, known for their loyalty and friendliness.\",\n",
    "        metadata={\"source\": \"mammal-pets-doc\"},\n",
    "    ),\n",
    "    Document(\n",
    "        page_content=\"Cats are independent pets that often enjoy their own space.\",\n",
    "        metadata={\"source\": \"mammal-pets-doc\"},\n",
    "    ),\n",
    "    Document(\n",
    "        page_content=\"Goldfish are popular pets for beginners, requiring relatively simple care.\",\n",
    "        metadata={\"source\": \"fish-pets-doc\"},\n",
    "    ),\n",
    "    Document(\n",
    "        page_content=\"Parrots are intelligent birds capable of mimicking human speech.\",\n",
    "        metadata={\"source\": \"bird-pets-doc\"},\n",
    "    ),\n",
    "    Document(\n",
    "        page_content=\"Rabbits are social animals that need plenty of space to hop around.\",\n",
    "        metadata={\"source\": \"mammal-pets-doc\"},\n",
    "    ),\n",
    "]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[Document(page_content='Dogs are great companions, known for their loyalty and friendliness.', metadata={'source': 'mammal-pets-doc'}),\n",
       " Document(page_content='Cats are independent pets that often enjoy their own space.', metadata={'source': 'mammal-pets-doc'}),\n",
       " Document(page_content='Goldfish are popular pets for beginners, requiring relatively simple care.', metadata={'source': 'fish-pets-doc'}),\n",
       " Document(page_content='Parrots are intelligent birds capable of mimicking human speech.', metadata={'source': 'bird-pets-doc'}),\n",
       " Document(page_content='Rabbits are social animals that need plenty of space to hop around.', metadata={'source': 'mammal-pets-doc'})]"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "documents"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "ChatGroq(client=<groq.resources.chat.completions.Completions object at 0x000001AF0FD424A0>, async_client=<groq.resources.chat.completions.AsyncCompletions object at 0x000001AF0FD43010>, model_name='Llama3-8b-8192', groq_api_key=SecretStr('**********'))"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import os\n",
    "from dotenv import load_dotenv\n",
    "load_dotenv()\n",
    "from langchain_groq import ChatGroq\n",
    "groq_api_key=os.getenv(\"GROQ_API_KEY\")\n",
    "\n",
    "os.environ[\"HF_TOKEN\"]=os.getenv(\"HF_TOKEN\")\n",
    "\n",
    "llm=ChatGroq(groq_api_key=groq_api_key,model=\"Llama3-8b-8192\")\n",
    "llm"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: langchain_huggingface in e:\\udemy final\\langchain\\venv\\lib\\site-packages (0.0.3)\n",
      "Requirement already satisfied: huggingface-hub>=0.23.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain_huggingface) (0.23.4)\n",
      "Requirement already satisfied: langchain-core<0.3,>=0.1.52 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain_huggingface) (0.2.10)\n",
      "Requirement already satisfied: sentence-transformers>=2.6.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain_huggingface) (3.0.1)\n",
      "Requirement already satisfied: tokenizers>=0.19.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain_huggingface) (0.19.1)\n",
      "Requirement already satisfied: transformers>=4.39.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain_huggingface) (4.41.2)\n",
      "Requirement already satisfied: filelock in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from huggingface-hub>=0.23.0->langchain_huggingface) (3.15.4)\n",
      "Requirement already satisfied: fsspec>=2023.5.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from huggingface-hub>=0.23.0->langchain_huggingface) (2024.6.0)\n",
      "Requirement already satisfied: packaging>=20.9 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from huggingface-hub>=0.23.0->langchain_huggingface) (24.1)\n",
      "Requirement already satisfied: pyyaml>=5.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from huggingface-hub>=0.23.0->langchain_huggingface) (6.0.1)\n",
      "Requirement already satisfied: requests in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from huggingface-hub>=0.23.0->langchain_huggingface) (2.31.0)\n",
      "Requirement already satisfied: tqdm>=4.42.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from huggingface-hub>=0.23.0->langchain_huggingface) (4.66.4)\n",
      "Requirement already satisfied: typing-extensions>=3.7.4.3 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from huggingface-hub>=0.23.0->langchain_huggingface) (4.12.2)\n",
      "Requirement already satisfied: jsonpatch<2.0,>=1.33 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain-core<0.3,>=0.1.52->langchain_huggingface) (1.33)\n",
      "Requirement already satisfied: langsmith<0.2.0,>=0.1.75 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain-core<0.3,>=0.1.52->langchain_huggingface) (0.1.77)\n",
      "Requirement already satisfied: pydantic<3,>=1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain-core<0.3,>=0.1.52->langchain_huggingface) (1.10.13)\n",
      "Requirement already satisfied: tenacity!=8.4.0,<9.0.0,>=8.1.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langchain-core<0.3,>=0.1.52->langchain_huggingface) (8.4.1)\n",
      "Requirement already satisfied: torch>=1.11.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from sentence-transformers>=2.6.0->langchain_huggingface) (2.3.1)\n",
      "Requirement already satisfied: numpy in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from sentence-transformers>=2.6.0->langchain_huggingface) (1.26.4)\n",
      "Requirement already satisfied: scikit-learn in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from sentence-transformers>=2.6.0->langchain_huggingface) (1.5.0)\n",
      "Requirement already satisfied: scipy in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from sentence-transformers>=2.6.0->langchain_huggingface) (1.13.1)\n",
      "Requirement already satisfied: Pillow in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from sentence-transformers>=2.6.0->langchain_huggingface) (10.3.0)\n",
      "Requirement already satisfied: regex!=2019.12.17 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from transformers>=4.39.0->langchain_huggingface) (2024.5.15)\n",
      "Requirement already satisfied: safetensors>=0.4.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from transformers>=4.39.0->langchain_huggingface) (0.4.3)\n",
      "Requirement already satisfied: jsonpointer>=1.9 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from jsonpatch<2.0,>=1.33->langchain-core<0.3,>=0.1.52->langchain_huggingface) (3.0.0)\n",
      "Requirement already satisfied: orjson<4.0.0,>=3.9.14 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from langsmith<0.2.0,>=0.1.75->langchain-core<0.3,>=0.1.52->langchain_huggingface) (3.10.5)\n",
      "Requirement already satisfied: charset-normalizer<4,>=2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from requests->huggingface-hub>=0.23.0->langchain_huggingface) (3.3.2)\n",
      "Requirement already satisfied: idna<4,>=2.5 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from requests->huggingface-hub>=0.23.0->langchain_huggingface) (3.7)\n",
      "Requirement already satisfied: urllib3<3,>=1.21.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from requests->huggingface-hub>=0.23.0->langchain_huggingface) (2.2.2)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from requests->huggingface-hub>=0.23.0->langchain_huggingface) (2024.6.2)\n",
      "Requirement already satisfied: sympy in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from torch>=1.11.0->sentence-transformers>=2.6.0->langchain_huggingface) (1.12.1)\n",
      "Requirement already satisfied: networkx in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from torch>=1.11.0->sentence-transformers>=2.6.0->langchain_huggingface) (3.3)\n",
      "Requirement already satisfied: jinja2 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from torch>=1.11.0->sentence-transformers>=2.6.0->langchain_huggingface) (3.1.4)\n",
      "Requirement already satisfied: mkl<=2021.4.0,>=2021.1.1 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from torch>=1.11.0->sentence-transformers>=2.6.0->langchain_huggingface) (2021.4.0)\n",
      "Requirement already satisfied: colorama in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from tqdm>=4.42.1->huggingface-hub>=0.23.0->langchain_huggingface) (0.4.6)\n",
      "Requirement already satisfied: joblib>=1.2.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from scikit-learn->sentence-transformers>=2.6.0->langchain_huggingface) (1.4.2)\n",
      "Requirement already satisfied: threadpoolctl>=3.1.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from scikit-learn->sentence-transformers>=2.6.0->langchain_huggingface) (3.5.0)\n",
      "Requirement already satisfied: intel-openmp==2021.* in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from mkl<=2021.4.0,>=2021.1.1->torch>=1.11.0->sentence-transformers>=2.6.0->langchain_huggingface) (2021.4.0)\n",
      "Requirement already satisfied: tbb==2021.* in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from mkl<=2021.4.0,>=2021.1.1->torch>=1.11.0->sentence-transformers>=2.6.0->langchain_huggingface) (2021.13.0)\n",
      "Requirement already satisfied: MarkupSafe>=2.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from jinja2->torch>=1.11.0->sentence-transformers>=2.6.0->langchain_huggingface) (2.1.5)\n",
      "Requirement already satisfied: mpmath<1.4.0,>=1.1.0 in e:\\udemy final\\langchain\\venv\\lib\\site-packages (from sympy->torch>=1.11.0->sentence-transformers>=2.6.0->langchain_huggingface) (1.3.0)\n"
     ]
    }
   ],
   "source": [
    "!pip install langchain_huggingface"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "e:\\UDemy Final\\Langchain\\venv\\lib\\site-packages\\sentence_transformers\\cross_encoder\\CrossEncoder.py:11: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html\n",
      "  from tqdm.autonotebook import tqdm, trange\n",
      "e:\\UDemy Final\\Langchain\\venv\\lib\\site-packages\\huggingface_hub\\file_download.py:1132: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.\n",
      "  warnings.warn(\n"
     ]
    }
   ],
   "source": [
    "from langchain_huggingface import HuggingFaceEmbeddings\n",
    "embeddings=HuggingFaceEmbeddings(model_name=\"all-MiniLM-L6-v2\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<langchain_chroma.vectorstores.Chroma at 0x1af0fd8f160>"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "## VectorStores\n",
    "from langchain_chroma import Chroma\n",
    "\n",
    "vectorstore=Chroma.from_documents(documents,embedding=embeddings)\n",
    "vectorstore\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[Document(page_content='Cats are independent pets that often enjoy their own space.', metadata={'source': 'mammal-pets-doc'}),\n",
       " Document(page_content='Dogs are great companions, known for their loyalty and friendliness.', metadata={'source': 'mammal-pets-doc'}),\n",
       " Document(page_content='Rabbits are social animals that need plenty of space to hop around.', metadata={'source': 'mammal-pets-doc'}),\n",
       " Document(page_content='Parrots are intelligent birds capable of mimicking human speech.', metadata={'source': 'bird-pets-doc'})]"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "vectorstore.similarity_search(\"cat\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[Document(page_content='Cats are independent pets that often enjoy their own space.', metadata={'source': 'mammal-pets-doc'}),\n",
       " Document(page_content='Dogs are great companions, known for their loyalty and friendliness.', metadata={'source': 'mammal-pets-doc'}),\n",
       " Document(page_content='Rabbits are social animals that need plenty of space to hop around.', metadata={'source': 'mammal-pets-doc'}),\n",
       " Document(page_content='Parrots are intelligent birds capable of mimicking human speech.', metadata={'source': 'bird-pets-doc'})]"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "## Async query\n",
    "await vectorstore.asimilarity_search(\"cat\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[(Document(page_content='Cats are independent pets that often enjoy their own space.', metadata={'source': 'mammal-pets-doc'}),\n",
       "  0.9351058006286621),\n",
       " (Document(page_content='Dogs are great companions, known for their loyalty and friendliness.', metadata={'source': 'mammal-pets-doc'}),\n",
       "  1.5740901231765747),\n",
       " (Document(page_content='Rabbits are social animals that need plenty of space to hop around.', metadata={'source': 'mammal-pets-doc'}),\n",
       "  1.595690131187439),\n",
       " (Document(page_content='Parrots are intelligent birds capable of mimicking human speech.', metadata={'source': 'bird-pets-doc'}),\n",
       "  1.665792465209961)]"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "vectorstore.similarity_search_with_score(\"cat\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Retrievers\n",
    "LangChain VectorStore objects do not subclass Runnable, and so cannot immediately be integrated into LangChain Expression Language chains.\n",
    "\n",
    "LangChain Retrievers are Runnables, so they implement a standard set of methods (e.g., synchronous and asynchronous invoke and batch operations) and are designed to be incorporated in LCEL chains.\n",
    "\n",
    "We can create a simple version of this ourselves, without subclassing Retriever. If we choose what method we wish to use to retrieve documents, we can create a runnable easily. Below we will build one around the similarity_search method:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[[Document(page_content='Cats are independent pets that often enjoy their own space.', metadata={'source': 'mammal-pets-doc'})],\n",
       " [Document(page_content='Dogs are great companions, known for their loyalty and friendliness.', metadata={'source': 'mammal-pets-doc'})]]"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "from typing import List\n",
    "\n",
    "from langchain_core.documents import Document\n",
    "from langchain_core.runnables import RunnableLambda\n",
    "\n",
    "retriever=RunnableLambda(vectorstore.similarity_search).bind(k=1)\n",
    "retriever.batch([\"cat\",\"dog\"])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Vectorstores implement an as_retriever method that will generate a Retriever, specifically a VectorStoreRetriever. These retrievers include specific search_type and search_kwargs attributes that identify what methods of the underlying vector store to call, and how to parameterize them. For instance, we can replicate the above with the following:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[[Document(page_content='Cats are independent pets that often enjoy their own space.', metadata={'source': 'mammal-pets-doc'})],\n",
       " [Document(page_content='Dogs are great companions, known for their loyalty and friendliness.', metadata={'source': 'mammal-pets-doc'})]]"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "retriever=vectorstore.as_retriever(\n",
    "    search_type=\"similarity\",\n",
    "    search_kwargs={\"k\":1}\n",
    ")\n",
    "retriever.batch([\"cat\",\"dog\"])\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "According to the provided context, dogs are great companions, known for their loyalty and friendliness.\n"
     ]
    }
   ],
   "source": [
    "## RAG\n",
    "from langchain_core.prompts import ChatPromptTemplate\n",
    "from langchain_core.runnables import RunnablePassthrough\n",
    "\n",
    "message = \"\"\"\n",
    "Answer this question using the provided context only.\n",
    "\n",
    "{question}\n",
    "\n",
    "Context:\n",
    "{context}\n",
    "\"\"\"\n",
    "prompt = ChatPromptTemplate.from_messages([(\"human\", message)])\n",
    "\n",
    "rag_chain={\"context\":retriever,\"question\":RunnablePassthrough()}|prompt|llm\n",
    "\n",
    "response=rag_chain.invoke(\"tell me about dogs\")\n",
    "print(response.content)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
