from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.utils.llm import get_llm
from src.state.state import AgentState
from src.utils.parsing import clean_text_output

def content_rewriter_node(state: AgentState):
    """
    Rewrites the draft with inline citations.
    """
    print("--- CONTENT REWRITER ---")
    draft = state.get("original_draft", "")
    valid_sources = state.get("validated_sources", [])
    
    if not valid_sources:
        return {"enhanced_draft": draft}

    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert editor. Incorporate the following verified information into the draft. "
                   "Add inline citations (e.g., (Author, Year) or [Source Title]) where appropriate. "
                   "Maintain the original voice and flow."),
        ("user", "Original Draft: {draft}\n\nVerified Sources: {sources}")
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        # Simplification: passing entire list of sources
        raw_draft = chain.invoke({"draft": draft, "sources": valid_sources})
        enhanced_draft = clean_text_output(raw_draft)
        return {"enhanced_draft": enhanced_draft}
    except Exception as e:
        print(f"Error rewriting content: {e}")
        return {"enhanced_draft": draft}
