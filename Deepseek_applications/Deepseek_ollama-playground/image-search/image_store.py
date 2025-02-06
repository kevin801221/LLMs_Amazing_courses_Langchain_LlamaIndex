import ollama
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document

class ImageStore:

    embeddings = OllamaEmbeddings(model="llama3.2:latest")
    vector_store = InMemoryVectorStore(embedding=embeddings)

    document_ids_to_images = {}
    document_ids_to_documents = {}

    images_directory = 'image-search/images/'

    @classmethod
    def upload_image(cls, file):
        with open(cls.images_directory + file.name, "wb") as f:
            f.write(file.getbuffer())

        description = cls._describe_image(cls.images_directory + file.name)
        document = Document(page_content=description)
        document_id = cls.vector_store.add_documents([document])[0]
        cls.document_ids_to_images[document_id] = file.name
        cls.document_ids_to_documents[document_id] = document

        return document_id


    @classmethod
    def _describe_image(cls, image_path):
        res = ollama.chat(
            model="llava:34b",
            messages=[
                {
                    'role': 'user',
                    'content': 'Tell me what do you see in this picture in only one sentence. Be concise.',
                    'images': [image_path]
                }
            ],
            options={'temperature': 0}
        )

        return res['message']['content']

    @classmethod
    def retrieve_docs_by_query(cls, query):
        return cls.vector_store.similarity_search(query, k=1)

    @classmethod
    def retrieve_docs_by_image(cls, image):
        with open(cls.images_directory + image.name, "wb") as f:
            f.write(image.getbuffer())

        description = cls._describe_image(cls.images_directory + image.name)
        return cls.retrieve_docs_by_query(description)

    @classmethod
    def get_by_id(cls, doc_id):
        return cls.document_ids_to_documents[doc_id]

    @classmethod
    def get_image_path_by_id(cls, doc_id):
       return cls.images_directory + cls.document_ids_to_images[doc_id]

