from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:
    @staticmethod
    def load(path):
        loader = PyPDFLoader(path)
        documents = loader.load()
        return documents


# documewnt = PDFLoader.load("../Global Indian Travel & Relocation Network.pdf")
# print(documewnt[0].page_content)
