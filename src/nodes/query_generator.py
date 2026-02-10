from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.utils.llm import get_llm
from src.state.state import AgentState
from src.utils.parsing import parse_json_output

def query_generator_node(state: AgentState):
    """
    Generates search queries for extracted claims.
    """
    print("--- QUERY GENERATOR ---")
    claims = state.get("extracted_claims", [])
    if not claims:
        return {"search_queries": []}
    
    # Filter for claims that are not yet verified
    pending_claims = [c["text"] for c in claims if not c.get("verified")]

    if not pending_claims:
        return {"search_queries": []}

    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a research assistant. For each claim provided, generate a targeted web search query to find supporting evidence. "
                   "Return a JSON object with a key 'queries' containing a list of strings."),
        ("user", "Claims: {claims}")
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        result_text = chain.invoke({"claims": pending_claims})
        result = parse_json_output(result_text)
        queries = result.get("queries", [])
        return {"search_queries": queries}
    except Exception as e:
        print(f"Error generating queries: {e}")
        return {"search_queries": []}
