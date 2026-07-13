from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextSplitter:

    def __init__(
        self,
        chunk_size=1000,
        chunk_overlap=200,
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split_documents(self, documents):

        chunks = []

        for document in documents:

            splits = self.splitter.split_text(
                document["content"]
            )

            for index, chunk in enumerate(splits):

                chunks.append(
                    {
                        "path": document["path"],
                        "chunk": chunk,
                        "chunk_id": index,
                    }
                )

        return chunks