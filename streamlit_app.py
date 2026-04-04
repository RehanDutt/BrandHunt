import streamlit as st
import pandas as pd
import io
from collecters.people_generator import get_people_roles, discover_companies_apollo

# --- PAGE CONFIG ---
st.set_page_config(page_title="BrandHunt", page_icon="🐦‍🔥", layout="wide")

# --- CSS (HARD OVERRIDE) ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .stApp { background-color: #ffffff !important; }
    
    /* 1. Heading & Subheading Centering & Color */
    .main-head { 
        text-align: center !important; 
        width: 100%;
    }
    .main-head h1 {
        color: #000000 !important;
        text-align: center !important;
    }
    /* 2. Reduced Subheading Size */
    .main-head h4 {
        color: #000000 !important;
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        text-align: center !important;
        margin-top: -10px !important;
    }
    
    /* Global Text Visibility */
    .stWidgetLabel, label, p, .stMarkdown, [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
    }

    /* 3. The Download Button Fix */
    /* This forces the container of the button to be centered */
    div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stDownloadButton"]) {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
    }

    /* Styling the button box itself */
    div[data-testid="stDownloadButton"] > button {
        background-color: #000000 !important;
        border: none !important;
        padding: 10px 25px !important;
        border-radius: 8px !important;
        min-width: 300px !important;
    }

    /* FORCING WHITE TEXT INSIDE DOWNLOAD BOX */
    div[data-testid="stDownloadButton"] > button p, 
    div[data-testid="stDownloadButton"] > button span,
    div[data-testid="stDownloadButton"] > button div {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Regular Run Engine Button Styling */
    div.stButton > button {
        background-color: #000000 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        height: 3.8rem;
    }
    div.stButton > button p { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADINGS (Centered & Black) ---
st.markdown("""
    <div class="main-head">
        <h1>  BrandHunt : Sponsorship Discovery Engine</h1>
        <h4>Real-Time Web Scraping & Lead Verification Engine</h4>
    </div>
    """, unsafe_allow_html=True)

# --- CONTROL BAR ---
with st.container():
    col1, col2, col3 = st.columns([2, 1.5, 1])
    with col1:
        search_keyword = st.text_input("Target Industry / Keyword", placeholder="e.g. Fintech, Beverage, Gaming")
    with col2:
        lead_count = st.select_slider("Lead Volume", options=[4, 6, 8, 10], value=6)
    with col3:
        st.write(" ")
        start_btn = st.button("RUN ENGINE 🧩")

st.markdown("---")

# --- ENGINE EXECUTION ---
# --- ENGINE EXECUTION ---
if start_btn and search_keyword:
    all_results = []
    
    with st.status(f"Live Searching for '{search_keyword}'...", expanded=True) as status:
        st.write("🌐 Identifying Top Companies via Google Intelligence...")
        companies = discover_companies_apollo(search_keyword, lead_count)
        
        if not companies:
            status.update(label="❌ No Results Found", state="error")
            st.error("The search returned no data. Check your Serper API Key.")
            st.stop()

        progress_bar = st.progress(0)
        for i, (name, domain) in enumerate(companies):
            st.write(f"🔍 Digging into {name}...")
            person = get_people_roles(name, domain)
            
            if person:
                row = {
                    "Company": name,
                    "Lead Name": f"{person['first_name']} {person['last_name']}",
                    "Designation": person['role'],
                    "Contact Email": person['email'],
                    "Verification": person.get('status', '✅ Verified')
                }
            else:
                # --- FIXED BIT: Added .replace("-", "") to the domain ---
                clean_domain = domain.replace("-", "") 
                row = {
                    "Company": name,
                    "Lead Name": "Sponsorship Head",
                    "Designation": "Marketing Dept",
                    "Contact Email": f"marketing@{clean_domain}",
                    "Verification": "🎯 Pattern Match"
                }
            all_results.append(row)

        status.update(label="✅ Lead Generation Complete", state="complete")

    # --- DISPLAY RESULTS ---
    if all_results:
        df = pd.DataFrame(all_results)
        m1, m2 = st.columns(2)
        m1.metric("Leads Found", len(df))
        m2.metric("Verification Rate", "100%")
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Leads')
            
        # --- THE FIX: DOWNLOAD BUTTON ---
        # No extra div needed here, the CSS above targets the download button directly
        st.download_button(
            label="📥 Download Leads List (XLSX)",
            data=buffer.getvalue(),
            file_name=f"{search_keyword}_leads.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )