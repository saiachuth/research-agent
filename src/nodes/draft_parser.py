from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.utils.llm import get_llm
from src.state.state import AgentState
from src.utils.parsing import parse_json_output

def draft_parser_node(state: AgentState):
    """
    Analyzes the draft to extract factual claims.
    """
    print("--- DRAFT PARSER ---")
    draft = state["original_draft"]
    llm = get_llm()

    # Use StrOutputParser then custom parse
    parser = StrOutputParser()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert editor. Your task is to identify factual claims in the text that need verification. "
                   "Return a JSON object with a key 'claims' containing a list of strings, where each string is a claim. "
                   "Do not output markdown code blocks or reasoning, just the raw JSON."),
        ("user", "Draft: {draft}")
    ])

    chain = prompt | llm | parser

    try:
        result_text = chain.invoke({"draft": draft})
        result = parse_json_output(result_text)
        
        claims = result.get("claims", [])
        # Convert list of strings to list of dicts for tracking status
        claims_data = [{"text": c, "verified": False} for c in claims]
        return {"extracted_claims": claims_data}
    except Exception as e:
        print(f"Error parsing draft: {e}")
        return {"extracted_claims": []}
