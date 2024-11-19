import os
from dotenv import load_dotenv
from scraper import GithubReadmeScraper
from qdrant_manager import QdrantManager
from rag_pipeline import RAGPipeline
import gradio as gr

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise Exception("OpenAI API key is not set. Please check your .env file.")

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = api_key

# Initialize QdrantManager and RAGPipeline
qdrant_manager = QdrantManager()
qdrant_manager.initialize_collection()
rag_pipeline = None  # Will be initialized after README scraping

# Gradio functions
def scrape_and_store(repo_url):
    """
    Scrape the README from the given GitHub repository URL and store it in Qdrant.
    :param repo_url: GitHub repository URL
    :return: Status message
    """
    global rag_pipeline
    try:
        scraper = GithubReadmeScraper()
        readme_content = scraper.scrape_readme(repo_url)
        qdrant_manager.store_readme(readme_content)
        retriever = qdrant_manager.create_retriever()
        rag_pipeline = RAGPipeline(retriever=retriever)
        return "README content successfully scraped and stored. Ready to answer questions."
    except Exception as e:
        return f"Error: {e}"


def answer_question(query):
    """
    Answer questions about the scraped README content using the RAG pipeline.
    :param query: User's question
    :return: Generated response
    """
    global rag_pipeline
    if rag_pipeline is None:
        return "No README content available. Please scrape a repository first."
    try:
        return rag_pipeline.ask_question(query)
    except Exception as e:
        return f"Error while processing query: {e}"


# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# GitHub README Scraper and Q&A System")
    gr.Markdown("Enter a GitHub repository URL to scrape its README and ask questions about its content.")

    with gr.Row():
        repo_url_input = gr.Textbox(label="GitHub Repository URL", placeholder="Enter GitHub repository URL")
        scrape_button = gr.Button("Scrape README")

    scrape_status = gr.Textbox(label="Status", interactive=False)

    scrape_button.click(scrape_and_store, inputs=[repo_url_input], outputs=[scrape_status])

    question_input = gr.Textbox(label="Ask a Question", placeholder="Ask something about the README content")
    answer_output = gr.Textbox(label="Answer", interactive=False)

    question_input.submit(answer_question, inputs=[question_input], outputs=[answer_output])

# Launch the Gradio App
if __name__ == "__main__":
    demo.launch()
