from langchain.text_splitter import RecursiveCharacterTextSplitter


class NoticeTextSplitter(RecursiveCharacterTextSplitter):

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50, **kwargs):
        separators = ["\n\n", "\n", ".", "?", "!", " ", ""]
        super().__init__(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
            **kwargs
        )