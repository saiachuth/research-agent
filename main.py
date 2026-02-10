import os
import sys

# Add src to python path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.graph.graph import build_graph

def main():
    print("Initializing Research Agent...")
    try:
        app = build_graph()
        
        if len(sys.argv) > 1:
            sample_draft = " ".join(sys.argv[1:])
        else:
            print("Enter the draft text to research (press Enter twice to finish):")
            lines = []
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)
            sample_draft = "\n".join(lines)
            
        if not sample_draft.strip():
            print("No text provided. Exiting.")
            return
        
        initial_state = {
            "original_draft": sample_draft,
            "extracted_claims": [],
            "search_queries": [],
            "web_results": [],
            "validated_sources": [],
            "formatted_citations": [],
            "enhanced_draft": "",
            "verification_status": {},
            "quality_check_passed": False
        }
        
        print(f"Processing draft: {sample_draft}")
        
        # Config for memory saver (mock thread id)
        config = {"configurable": {"thread_id": "1"}}
        
        # Run the graph
        for output in app.stream(initial_state, config=config):
            for key, value in output.items():
                print(f"Finished node: {key}")
                print(f"Output: {value}") # Verbose
        
        # Get final state
        final_state = app.get_state(config).values
        print("\n--- Final Enhanced Draft ---")
        print(final_state.get("enhanced_draft"))
        
        print("\n--- Citations ---")
        for citation in final_state.get("formatted_citations", []):
            print(citation)

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
