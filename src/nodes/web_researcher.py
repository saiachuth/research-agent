from duckduckgo_search import DDGS
from src.state.state import AgentState

def web_researcher_node(state: AgentState):
    """
    Executes web searches for the generated queries.
    """
    print("--- WEB RESEARCHER ---")
    queries = state.get("search_queries", [])
    results = []
    
    # Use DDGS directly
    with DDGS() as ddgs:
        for query in queries:
            try:
                # search() returns a list of dicts: {'title':..., 'href':..., 'body':...}
                accumulated_results = [r for r in ddgs.text(query, max_results=2)]
                
                for r in accumulated_results:
                    results.append({
                        "query": query,
                        "content": r.get('body', ''),
                        "title": r.get('title', ''),
                        "url": r.get('href', '')
                    })
            except Exception as e:
                print(f"Error searching for {query}: {e}")
            
    return {"web_results": results}
