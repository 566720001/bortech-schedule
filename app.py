import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Замены для 2СОО5", page_icon="🔄", layout="centered")

URL = "https://bortech.by"

@st.cache_data(ttl=600)
def fetch_replacements():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(URL, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return None, f"Ошибка доступа к сайту: код {response.status_code}"
            
        soup = BeautifulSoup(response.text, "html.parser")
        content_area = soup.find("main") or soup.find("article") or soup.body
        found_rows = []
        pattern = re.compile(r"2[cс][oо][oо]5", re.IGNORECASE)
        
        tables = content_area.find_all("table")
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                row_text = row.get_text(separator=" ").strip()
                if pattern.search(row_text):
                    cells = [cell.get_text().strip() for cell in row.find_all(["td", "th"])]
                    found_rows.append({"type": "table_row", "data": cells})
        
        if not found_rows:
            paragraphs = content_area.find_all
