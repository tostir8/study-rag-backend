from langchain.text_splitter import RecursiveCharacterTextSplitter


class Chunker:
    """
    Splits large documents into overlapping chunks.

    Overlapping chunks preserve context between adjacent
    pieces of text, improving retrieval quality.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> None:

        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def split(self, text: str) -> list[str]:
        """
        Splits a document into text chunks.
        """

        return self._splitter.split_text(text)
