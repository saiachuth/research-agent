from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from src.state.state import AgentState
from src.nodes.draft_parser import draft_parser_node
from src.nodes.query_generator import query_generator_node
from src.nodes.web_researcher import web_researcher_node
from src.nodes.source_validator import source_validator_node
from src.nodes.citation_formatter import citation_formatter_node
from src.nodes.content_rewriter import content_rewriter_node
from src.nodes.quality_checker import quality_checker_node

def check_quality(state: AgentState):
    """
    Conditional edge function to check quality status.
    """
    passed = state.get("quality_check_passed", False)
    retries = state.get("retry_count", 0)
    
    if passed or retries >= 1: # Limit to 1 retry for this demo
        return "formatter"
    else:
        print(f"--- QUALITY CHECK FAILED (Retries: {retries}) ---")
        return "generator"

def build_graph():
    """
    Constructs the LangGraph workflow.
    """
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("parser", draft_parser_node)
    
    # helper to update retry count
    def update_retry(state):
        return {"retry_count": state.get("retry_count", 0) + 1}
        
    workflow.add_node("generator", query_generator_node)
    workflow.add_node("researcher", web_researcher_node)
    workflow.add_node("validator", source_validator_node)
    workflow.add_node("quality", quality_checker_node)
    workflow.add_node("formatter", citation_formatter_node)
    workflow.add_node("rewriter", content_rewriter_node)
    
    # Node to increment retry, or we just rely on state passing. 
    # To keep it simple, we won't add a dedicated node, just let the loop happen 
    # and we rely on 'generator' or 'quality' to not reset it?
    # Actually explicit node or state update is better.
    # Let's just manage retry_count in the check_quality or via a small node.
    # But graph edges don't update state.
    # We can add a "retry_policy" node.
    
    def retry_policy(state):
        print("--- RETRYING RESEARCH ---")
        return {"retry_count": state.get("retry_count", 0) + 1}

    workflow.add_node("retry_policy", retry_policy)

    # Define edges
    workflow.set_entry_point("parser")
    workflow.add_edge("parser", "generator")
    workflow.add_edge("generator", "researcher")
    workflow.add_edge("researcher", "validator")
    workflow.add_edge("validator", "quality")
    
    workflow.add_conditional_edges(
        "quality", 
        check_quality, 
        {
            "formatter": "formatter", 
            "generator": "retry_policy"
        }
    )
    
    workflow.add_edge("retry_policy", "generator")
    workflow.add_edge("formatter", "rewriter")
    workflow.add_edge("rewriter", END)

    # Checkpointing
    memory = MemorySaver()

    app = workflow.compile(checkpointer=memory)
    return app
