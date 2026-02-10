from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.utils.llm import get_llm
from src.state.state import AgentState
from src.utils.parsing import parse_json_output

def source_validator_node(state: AgentState):
    """
    Validates the relevance and credibility of search results.
    """
    print("--- SOURCE VALIDATOR ---")
    results = state.get("web_results", [])
    claims = state.get("extracted_claims", [])
    
    if not results:
        return {"validated_sources": []}

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a fact checker. Evaluate if the search results support the claims. "
                   "Return a JSON object with 'valid_sources' list. Each item should have 'claim', 'source_content', 'is_relevant' (bool), and 'reason'."),
        ("user", "Claims: {claims}\nSearch Results: {results}")
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        # Simplification: passing all claims and results. In production, might loop or batch.
        # formatting claims for prompt
        claims_text = [c["text"] for c in claims]
        
        result_text = chain.invoke({
            "claims": claims_text, 
            "results": results
        })
        
        response = parse_json_output(result_text)
        
        valid_sources = response.get("valid_sources", [])
        # Filter only relevant ones
        relevant_sources = [s for s in valid_sources if s.get("is_relevant")]
        
        return {"validated_sources": relevant_sources}

    except Exception as e:
        print(f"Error validating sources: {e}")
        return {"validated_sources": []}
