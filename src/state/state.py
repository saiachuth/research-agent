from typing import List, Dict, TypedDict, Optional

class AgentState(TypedDict):
    """
    Represents the state of the research agent.
    """
    original_draft: str
    extracted_claims: List[Dict]  # List of claims to verify
    search_queries: List[str]     # List of generated search queries
    web_results: List[Dict]       # List of raw search results (url, title, snippet, content)
    validated_sources: List[Dict] # List of sources that passed validation
    formatted_citations: List[str]# List of formatted citations
    enhanced_draft: str           # The final draft with citations
    verification_status: Dict     # Status of verification for each claim
    quality_check_passed: bool    # whether the quality check passed
    retry_count: int              # number of retries for research
