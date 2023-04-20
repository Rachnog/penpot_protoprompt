from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

from src.utils import *

def create_sources_from_files(
        path = "../training_data_raw", 
        description = "This is the SVG for the graphic object",
        openai_document = True):

    def load_svg_files(path):
        svg_files = []
        svg_names = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".svg"):
                    svg_files.append(os.path.join(root, file))
                    svg_names.append(file)
        return svg_files, svg_names

    # load SVG files recursively from the training_data folder alongside their names
    svg_files, svg_names = load_svg_files(path)
    sources = []
    for file, name in zip(svg_files, svg_names):
        # run_svgoptim(file, file)
        svg_opened = open(file, "r").read()
        svg_opened = remove_style_from_string(svg_opened)
        svg_opened = shorten_svg_ids(svg_opened)
        svg_opened = round_svg_numbers(svg_opened)
        prompt = f"""{description} {name.split('.')[0]}: {svg_opened}"""

        if openai_document:
            sources.append(
                Document(
                    page_content=prompt,
                    metadata={
                        "source": file,
                        "name": name.split(".")[0], 
                        "style": file.split("/")[0],
                        },
            ))
        else:
            sources.append(
                {"svg": svg_opened, 
                 "source": file}
            )
    return sources


def create_chunks_from_the_sources(sources, separators = [], chunk_size = 1024, chunk_overlap = 0):
    chunks = []
    splitter = RecursiveCharacterTextSplitter(
        separators=separators,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    for source in sources:
        for chunk in splitter.split_text(source.page_content):
            chunks.append(Document(page_content=chunk, metadata=source.metadata))
    return chunks


def create_index_from_the_chunks(chunks):
    return FAISS.from_documents(chunks, OpenAIEmbeddings())