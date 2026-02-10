from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.utils.llm import get_llm
from src.state.state import AgentState
from src.utils.parsing import parse_json_output

def citation_formatter_node(state: AgentState):
    """
    Formats citations for validated sources.
    """
    print("--- CITATION FORMATTER ---")
    valid_sources = state.get("validated_sources", [])
    
    if not valid_sources:
        return {"formatted_citations": []}

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a bibliographer. Format the following sources into APA style citations. "
                   "Return a JSON object with 'citations' list of strings."),
        ("user", "Sources: {sources}")
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        result_text = chain.invoke({
            "sources": valid_sources
        })
        response = parse_json_output(result_text)
        
        return {"formatted_citations": response.get("citations", [])}
    except Exception as e:
        print(f"Error formatting citations: {e}")
        return {"formatted_citations": []}
