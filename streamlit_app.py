import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to python path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.graph.graph import build_graph

st.set_page_config(page_title="Deep Research Agent", page_icon="🤖", layout="wide")

st.title("🤖 Deep Research Agent")
st.markdown("Enter a draft text below, and the agent will research, validate, and enhance it with citations.")

# Sidebar for configuration if needed later
with st.sidebar:
    st.header("Configuration")
    st.info("Using Groq + DuckDuckGo + LangGraph")

draft_input = st.text_area("Original Draft", height=200, placeholder="Paste your draft text here...")

if st.button("Enhance Draft", type="primary"):
    if not draft_input.strip():
        st.warning("Please enter some text to process.")
    else:
        try:
            with st.spinner("Initializing Agent..."):
                app = build_graph()
                
            initial_state = {
                "original_draft": draft_input,
                "extracted_claims": [],
                "search_queries": [],
                "web_results": [],
                "validated_sources": [],
                "formatted_citations": [],
                "enhanced_draft": "",
                "verification_status": {},
                "quality_check_passed": False,
                "retry_count": 0
            }
            
            config = {"configurable": {"thread_id": "streamlit_session"}}
            
            # Container to display progress
            progress_container = st.container()
            
            with st.status("Processing...", expanded=True) as status:
                for output in app.stream(initial_state, config=config):
                    for key, value in output.items():
                        status.write(f"Completed step: **{key}**")
                        
                        # Optional: Display intermediate results in expanders
                        if key == "parser":
                            with status.expander("Extracted Claims"):
                                st.dataframe(value.get("extracted_claims", []))
                        elif key == "generator":
                            with status.expander("Search Queries"):
                                st.write(value.get("search_queries", []))
                        elif key == "researcher":
                            with status.expander("Web Results"):
                                st.write(f"Found {len(value.get('web_results', []))} results")
                        elif key == "validator":
                            with status.expander("Validated Sources"):
                                st.dataframe(value.get("validated_sources", []))
                                
            # Get final state
            final_state = app.get_state(config).values
            enhanced_draft = final_state.get("enhanced_draft")
            citations = final_state.get("formatted_citations", [])
            
            st.success("Processing Complete!")
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Original")
                st.text(draft_input)
                
            with col2:
                st.subheader("Enhanced")
                st.markdown(enhanced_draft)
            
            st.divider()
            
            st.subheader("References")
            for citation in citations:
                st.markdown(f"- {citation}")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
            import traceback
            st.exception(e)
