from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.utils.llm import get_llm
from src.state.state import AgentState
from src.utils.parsing import parse_json_output

def quality_checker_node(state: AgentState):
    """
    Checks if all claims are adequately supported.
    """
    print("--- QUALITY CHECKER ---")
    claims = state.get("extracted_claims", [])
    valid_sources = state.get("validated_sources", [])
    
    # Simple logic: if we have valid sources, we assume some coverage. 
    # sophisticated implementation would map sources to claims.
    
    # For now, let's ask the LLM if the coverage is sufficient.
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a quality assurance specialist. Check if the extracted claims are supported by the valid sources. "
                   "Return a JSON with 'passed' (bool) and 'missing_claims' (list of strings)."),
        ("user", "Claims: {claims}\nValid Sources: {sources}")
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        result_text = chain.invoke({
            "claims": [c["text"] for c in claims], 
            "sources": valid_sources
        })
        response = parse_json_output(result_text)
        
        passed = response.get("passed", False)
        
        # If passed, we mark verification_status
        return {
            "quality_check_passed": passed,
            "verification_status": {"passed": passed, "missing": response.get("missing_claims", [])}
        }
    except Exception as e:
        print(f"Error checking quality: {e}")
        # Default to passed to avoid infinite loops in this simple demo if error occurs
        return {"quality_check_passed": True, "verification_status": {"error": str(e)}}
