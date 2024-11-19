from langchain.llms import OpenAI
from langchain.chains import RetrievalQA


class RAGPipeline:
    """
    Sets up and manages the RAG pipeline.
    """

    def __init__(self, retriever, llm_model: str = "text-davinci-003"):
        self.llm = OpenAI(model_name=llm_model)
        self.qa_chain = RetrievalQA(retriever=retriever, llm=self.llm)

    def ask_question(self, query: str) -> str:
        """
        Queries the pipeline and retrieves a generated response.
        :param query: User's query string.
        :return: Generated response.
        """
        return self.qa_chain.run(query)
