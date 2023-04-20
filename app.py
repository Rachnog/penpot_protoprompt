import streamlit as st
import yaml
import sys, os
import base64
import pandas as pd
import pickle

from src.utils import *
from src.svg_quality_checks import *
from src.gpt_wrappers import *
from src.langchain_database import *

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAIChat, OpenAI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
import openai

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

with open("resources/index.pkl", "rb") as f:
    index = pickle.load(f)

openai.api_key = config["OPENAI_KEY"]
os.environ["OPENAI_API_KEY"] = config["OPENAI_KEY"]

def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)




system_prompt_svg = \
"""
    You are an expert in design in different fields, you use different vector graphics tools.
    You deal professionally with SVG files, you know how to create complex design with them.
"""
question_prompt_svg = \
"""
=========
Write code of the SVG that contains {question}.
=========
You must use following SVGs as examples and take as much as you can style, color, size, fonts from them:
{summaries}
=========
Keep it as short and optimized as you can, be limited by the tokens.
Start with <svg xmlns="http://www.w3.org/2000/svg"... and end with </svg>.
"""
template_svg = system_prompt_svg + question_prompt_svg
prompt_svg = PromptTemplate(template=template_svg, input_variables=["summaries", "question"])






question_prompt_html = \
"""
=========
Write code of the HTML that contains {question}.
=========
You must use following SVGs as examples and take as much as you can style, color, size, fonts from them:
{summaries}
=========
Keep it as short and optimized as you can, be limited by the tokens.
Start with <html> and end with </html>.
"""
template_html = system_prompt_svg + question_prompt_html
prompt_html = PromptTemplate(template=template_html, input_variables=["summaries", "question"])






st.title("SVG Design System Generator")
st.header("Tell us what you want to design")

question = st.text_input(
                            "Enter a question", 
                            "Footer with segmented buttons saying Email, Post, Horse with corresponding emojis"
                         )

search_checkbox = st.checkbox("Search for similar SVGs in the database")
generate_checkbox = st.checkbox("Generate SVGs")
generate_html_checkbox = st.checkbox("Generate HTMLs")

if search_checkbox:

    st.subheader("Most similar SVGs in the database:")

    similarity_results = index.similarity_search(question, k=4)
    col1_search, col2_search, col3_search, col4_search = st.columns(4)
    with col1_search:
        st.write(similarity_results[0].metadata["name"])
        svg_search1 = open(similarity_results[0].metadata["source"][3:], 'r').read()
        render_svg(svg_search1)
        st.text_input("", svg_search1, key="svg_search1")
    with col2_search:
        st.write(similarity_results[1].metadata["name"])
        svg_search2 = open(similarity_results[1].metadata["source"][3:], 'r').read()
        render_svg(svg_search2)
        st.text_input("", svg_search2, key="svg_search2")
    with col3_search:
        st.write(similarity_results[2].metadata["name"])
        svg_search3 = open(similarity_results[2].metadata["source"][3:], 'r').read()
        render_svg(svg_search3)
        st.text_input("", svg_search3, key="svg_search3")
    with col4_search:
        st.write(similarity_results[3].metadata["name"])
        svg_search4 = open(similarity_results[3].metadata["source"][3:], 'r').read()
        render_svg(svg_search4)
        st.text_input("", svg_search4, key="svg_search4")
    
if generate_checkbox:
    
    st.subheader("Generated SVGs:")

    col1_gen, col2_gen, col3_gen, col4_gen = st.columns(4)

    similarity_results = index.similarity_search(question, k=4)

    with col1_gen:
        st.write("Temperature 0.0")
        chain = load_qa_with_sources_chain(OpenAIChat(temperature=0.0, model_name="gpt-3.5-turbo"), prompt=prompt_svg)
        answer = chain(
            {
                "input_documents": similarity_results,
                "question": question,
            },
            return_only_outputs=True,
        )["output_text"]
        # save_gpt_answer_as_svg(answer, 'answer1', 'generated_data')
        # answer_loaded = open(f'generated_data/answer1_optimized.svg', 'r').read()
        render_svg(answer)
        st.text_input("", answer, key="svg_gen1")

    with col2_gen:
        st.write("Temperature 0.1")
        chain = load_qa_with_sources_chain(OpenAIChat(temperature=0.1, model_name="gpt-3.5-turbo"), prompt=prompt_svg)
        answer = chain(
            {
                "input_documents": similarity_results,
                "question": question,
            },
            return_only_outputs=True,
        )["output_text"]
        # save_gpt_answer_as_svg(answer, 'answer2', 'generated_data')
        # answer_loaded = open(f'generated_data/answer2_optimized.svg', 'r').read()
        render_svg(answer)
        st.text_input("", answer, key="svg_gen2")

    with col3_gen:
        st.write("Temperature 0.9")
        chain = load_qa_with_sources_chain(OpenAIChat(temperature=0.9, model_name="gpt-3.5-turbo"), prompt=prompt_svg)
        answer = chain(
            {
                "input_documents": similarity_results,
                "question": question,
            },
            return_only_outputs=True,
        )["output_text"]
        # save_gpt_answer_as_svg(answer, 'answer3', 'generated_data')
        # answer_loaded = open(f'generated_data/answer3_optimized.svg', 'r').read()
        render_svg(answer)
        st.text_input("", answer, key="svg_gen3")

    with col4_gen:
        st.write("Temperature 1.0")
        chain = load_qa_with_sources_chain(OpenAIChat(temperature=1.0, model_name="gpt-3.5-turbo"), prompt=prompt_svg)
        answer = chain(
            {
                "input_documents": similarity_results,
                "question": question,
            },
            return_only_outputs=True,
        )["output_text"]
        # save_gpt_answer_as_svg(answer, 'answer4', 'generated_data')
        # answer_loaded = open(f'generated_data/answer4_optimized.svg', 'r').read()
        render_svg(answer)
        st.text_input("", answer, key="svg_gen4")


if generate_html_checkbox:

    st.subheader("Generated HTMLs:")

    col1_gen_html, col2_gen_html, col3_gen_html, col4_gen_html = st.columns(4)

    similarity_results = index.similarity_search(question, k=4)

    with col1_gen_html:
        st.write("Temperature 0.0")
        chain = load_qa_with_sources_chain(OpenAIChat(temperature=0.0, model_name="gpt-3.5-turbo"), prompt=prompt_html)
        answer = chain(
            {
                "input_documents": similarity_results,
                "question": question,
            },
            return_only_outputs=True,
        )["output_text"]
        st.components.v1.html(answer)
        st.text_input("", answer, key="html_gen1")

    with col2_gen_html:
        st.write("Temperature 0.1")
        chain = load_qa_with_sources_chain(OpenAIChat(temperature=0.1, model_name="gpt-3.5-turbo"), prompt=prompt_html)
        answer = chain(
            {
                "input_documents": similarity_results,
                "question": question,
            },
            return_only_outputs=True,
        )["output_text"]
        st.components.v1.html(answer)
        st.text_input("", answer, key="html_gen2")

    with col3_gen_html:
        st.write("Temperature 0.9")
        chain = load_qa_with_sources_chain(OpenAIChat(temperature=0.9, model_name="gpt-3.5-turbo"), prompt=prompt_html)
        answer = chain(
            {
                "input_documents": similarity_results,
                "question": question,
            },
            return_only_outputs=True,
        )["output_text"]
        st.components.v1.html(answer)
        st.text_input("", answer, key="html_gen3")

    with col4_gen_html:
        st.write("Temperature 1.0")
        chain = load_qa_with_sources_chain(OpenAIChat(temperature=1.0, model_name="gpt-3.5-turbo"), prompt=prompt_html)
        answer = chain(
            {
                "input_documents": similarity_results,
                "question": question,
            },
            return_only_outputs=True,
        )["output_text"]
        st.components.v1.html(answer)
        st.text_input("", answer, key="html_gen4")