import streamlit as st
import os
import re
from datetime import datetime
from agents.travel_retirement_agent import TravelRetirementAgent
from translations import translations

st.set_page_config(
    page_title="🌴 Smart Travel & Retirement Agent",
    page_icon="🌴",
    layout="wide"
)

# Clean Professional Styling
st.markdown("""
<style>
    .stApp { background-color: #f8f5f0; }
    h1 { color: #1a5276; font-weight: 700; }
    .subtitle { 
        font-size: 1.18rem; 
        color: #2c3e50; 
        margin-bottom: 1.2rem;
    }
    .stButton > button { 
        border-radius: 10px; 
        font-weight: 600;
    }
    .stButton > button[kind="primary"] {
        background-color: #27ae60;
    }
    [data-testid="stSidebar"] { 
        background-color: #f1ede4; 
    }
    .example-prompt {
        color: #555555;
        font-style: italic;
        margin: 8px 0 15px 0;
        padding: 12px 16px;
        background-color: #f1ede4;
        border-radius: 8px;
        border-left: 4px solid #3498db;
    }
</style>
""", unsafe_allow_html=True)

def format_plan_name(filename):
    name = os.path.splitext(filename)[0]
    name = name.replace("_", " ")
    match = re.search(r"(\d{8})\s*(\d{4})", name)
    if match:
        try:
            dt = datetime.strptime(match.group(1) + match.group(2), "%Y%m%d%H%M")
            nice_date = dt.strftime("%Y-%m-%d %H:%M")
            name = re.sub(r"\d{8}\s*\d{4}", f"({nice_date})", name)
        except:
            pass
    return name.strip()

# Session State
if "agent" not in st.session_state:
    st.session_state.agent = TravelRetirementAgent()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"
if "has_unsaved_changes" not in st.session_state:
    st.session_state.has_unsaved_changes = False

selected_lang_display = st.selectbox("🌐 Language", list(translations.keys()), index=0, key="lang_selector")

if selected_lang_display != st.session_state.selected_language:
    st.session_state.selected_language = selected_lang_display
    st.rerun()

t = translations[st.session_state.selected_language]

# ==================== HEADER ====================
col_logo, col_title = st.columns([1.2, 5])
with col_logo:
    try:
        st.image("logo.png", width=135)
    except:
        st.markdown("🌴", unsafe_allow_html=True)

with col_title:
    st.title(t["title"])

st.markdown(f'<p class="subtitle">{t["subtitle"]}</p>', unsafe_allow_html=True)

# ==================== HERO BANNER (Fixed deprecation) ====================
# st.image("hero_banner.jpg", 
#         use_container_width=True,
#         caption="Your next relaxed adventure awaits...")
#
# st.markdown("---")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.header(t["traveler_header"])
    traveler_type = st.selectbox(t["who_traveling"], t["traveler_options"], index=0)
    
    st.divider()
    st.header(t["actions_header"])
    
    save_title = st.text_input(
        t["save_label"], 
        t["default_title"], 
        key=f"save_{st.session_state.selected_language}",
        help=t.get("tooltip_plan_title", "")
    )
    
    if st.button(t["save_btn"], help=t.get("tooltip_save", "")):
        try:
            st.session_state.agent.save_plan(save_title)
            st.success("✅ Plan saved successfully!")
            st.session_state.has_unsaved_changes = False
        except Exception as e:
            st.error(f"Could not save plan: {str(e)}")

    export_format = st.radio(
        t["export_label"],
        ["PDF", "Markdown", "Text"],
        horizontal=True,
        index=0,
        key=f"format_{st.session_state.selected_language}",
        help=t.get("tooltip_export", "")
    )
    
    if st.button("📤 Export Plan", help=t.get("tooltip_export", "")):
        try:
            if export_format == "PDF":
                path = st.session_state.agent.export_markdown_plan(save_title)
                with open(path, "rb") as f:
                    pdf_bytes = f.read()
                st.download_button("📥 Download PDF Now", pdf_bytes, file_name=f"{save_title}.pdf", mime="application/pdf")
            elif export_format == "Markdown":
                path = st.session_state.agent.export_markdown_plan(save_title)
                with open(path, "rb") as f:
                    st.download_button("📥 Download Markdown Now", f, file_name=f"{save_title}.md")
            else:
                path = st.session_state.agent.save_plan(save_title)
                with open(path, "rb") as f:
                    st.download_button("📥 Download Text Now", f, file_name=f"{save_title}.txt")
        except Exception as e:
            st.error(f"Could not export: {str(e)}")

    if st.button(t["generate_btn"], help=t.get("tooltip_generate", "")):
        with st.spinner(t["thinking"]):
            full_prompt = f"Respond in {selected_lang_display.split('(')[0].strip()}. {t['full_proposal_prompt']}"
            response = st.session_state.agent.ask(full_prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.has_unsaved_changes = True

    if st.button(t["clear_btn"], help=t.get("tooltip_clear", "")):
        st.session_state.messages = []
        st.session_state.has_unsaved_changes = False
        st.success("✅ Conversation cleared!")
        st.rerun()

    st.divider()
    st.header(t["saved_plans_header"])
    plans_dir = "travel_plans"
    if os.path.exists(plans_dir):
        plans = sorted([f for f in os.listdir(plans_dir) if f.endswith(('.txt', '.md'))], reverse=True)
        if plans:
            for plan in plans[:8]:
                display_name = format_plan_name(plan)
                if st.button(display_name, key=f"gallery_{plan}"):
                    last_loaded = None
                    for msg in reversed(st.session_state.messages):
                        if msg["role"] == "assistant" and "**📂 Loaded Saved Plan:**" in msg["content"]:
                            last_loaded = msg["content"].split("**📂 Loaded Saved Plan:**")[1].split("\n")[0].strip()
                            break
                    if last_loaded == display_name:
                        st.info("This plan is already loaded.")
                    else:
                        with open(os.path.join(plans_dir, plan), "r", encoding="utf-8") as f:
                            content = f.read()
                        loaded_msg = {"role": "assistant", "content": f"**📂 Loaded Saved Plan:** {display_name}\n\n{content}"}
                        st.session_state.messages.append(loaded_msg)
                        if hasattr(st.session_state.agent, "messages"):
                            st.session_state.agent.messages.append(loaded_msg)
                        st.session_state.has_unsaved_changes = False
                        st.rerun()
        else:
            st.write("No saved plans yet.")
    else:
        st.write("No saved plans yet.")

# ==================== MAIN CHAT ====================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(t["input_placeholder"]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.has_unsaved_changes = True
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner(t["thinking"]):
            full_prompt = f"Respond in {selected_lang_display.split('(')[0].strip()}. {prompt}"
            response = st.session_state.agent.ask(full_prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Example Prompt - NOW DIRECTLY UNDER THE CHAT INPUT
st.markdown(f'<div class="example-prompt">{t.get("example_prompt", "💡 Example: Create a 10-day relaxed itinerary for Dubai for a couple who like galleries and gentle walks.")}</div>', unsafe_allow_html=True)

st.caption(t["footer"])

with st.expander(t.get("quick_tips_title", "💡 Quick Start Tips")):
    st.markdown(t.get("quick_tips_content", ""))