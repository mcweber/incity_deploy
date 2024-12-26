# ---------------------------------------------------
VERSION = "26.12.2024"
# Author: M. Weber
# ---------------------------------------------------
# 26.12.2024 switched to ask_llm.py
# ---------------------------------------------------

from datetime import datetime
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

import streamlit as st

import ask_llm
import ask_web

# Define Constants ---------------------------------------------------
KATEGORIEN = ["Restaurant & Bars", "Kunst & Museen", "Kino & Theater", "Konzerte", "Szene", "Sport"]
LLM = "gemini"
HEUTE = str(datetime.now().date())
TEMPERATURE = 0.2

web_handler = ask_web.WebSearch()
llm_handler = ask_llm.LLMHandler(llm="gemini", local=False)


# Functions -----------------------------------------------------------

def web_search(score: float = 0.9, limit: int = 3) -> str:
    results_str: str = ""
    with st.expander("Suchergebnisse"):
        for kat in KATEGORIEN:
            st.subheader(f"{kat}:")
            query = f"Ausgehtipps für den {HEUTE} in {st.session_state.city} für {kat}"
            result_list = web_handler.search(query=query, limit=limit)
            for result_item in result_list:
                st.write(f"Title: {result_item['title']}\n\nUrl: {result_item['url']}\n\n")
                results_str += f"Title: {result_item['title']}\nUrl: {result_item['url']}\nContent:{result_item['content']}\n\n"
    return results_str
    

def write_summary(content: str = "", url: str = "") -> str:
    text = ""
    if url != "":
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"}
        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return "error", "error"
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.body:
            text = soup.get_text()
    elif content != "":
        text = content
    if text != "":
        summary = llm_handler.ask_llm(
            temperature=TEMPERATURE,
            question = f"Schreibe eine Zusammenfassung des folgendes Textes: {text}."
            )
    else:
        summary = ""
    return summary

# Main -----------------------------------------------------------------

def main() -> None:

    st.set_page_config(page_title='CITY Insight')
    st.title("CITY Insight")
    st.write(f"Programmversion: {VERSION} Status: POC")
    
    # Initialize Session State -----------------------------------------
    if 'init' not in st.session_state:
        st.session_state.init: bool = True
        st.session_state.city: str = "Hamburg"
        st.session_state.search_status: bool = False

    SYSTEM_PROMPT = f"""
        Du bist ein Concierge in einem Hotel in {st.session_state.city}.
        Du antwortest auf Deutsch.
        Du weißt alles über die Stadt und kannst den Gästen Tipps geben.
        Heute ist der {HEUTE}.
        Deine Antwort bezieht sich immer auf den heutigen Tag und die genannte Stadt.
        Die Antwort besteht immer aus der Sektion {KATEGORIEN}.
        Die Antwort gibt immer konkrete Tipps, die sich auf eine bestimmte Aktivität beziehen.
        Die Antwort beinhaltet immer einen weiterführenden Link, entweder auf die konkrete Aktivität oder auf eine Webseite, die weitere Informationen bietet.
        """ 

    # Define Search Form ----------------------------------------------
    with st.form(key="new_search_form"):
        st.session_state.city = st.text_input(label="Für welche Stadt suchst Du Tipps?", value=st.session_state.city)
        if st.form_submit_button("Generiere Vorschläge"):
            st.session_state.search_status = True

    # Define Search & Search Results -------------------------------------------
    if st.session_state.search_status:

        # Web Search ------------------------------------------------
        web_results_str = web_search(score=0.9, limit=5)
        
        # LLM Search ------------------------------------------------
        response = llm_handler.ask_llm(
            temperature=TEMPERATURE,
            question="Stelle die besten Tipps zusammen, mindestens 3 pro Kategorie.",
            system_prompt=SYSTEM_PROMPT, 
            web_results_str=web_results_str
            )
        
        st.write(response)
        st.session_state.search_status = False


if __name__ == "__main__":
    main()