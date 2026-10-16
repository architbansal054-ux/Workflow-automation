import json
from core.engine import WorkflowOrchestrator

test_queries = [
    "Which products need restocking?",
    "Where is order ORD-1001?",
    "Assign this urgent task to the best available developer."
]

def main():
    orchestrator = WorkflowOrchestrator()
    print("=" * 80)
    print("AI AGENT WORKFLOW AUTOMATION - EXECUTION TRACE")
    print("=" * 80)

    for i, query in enumerate(test_queries, 1):
        output = orchestrator.execute(query)
        print(f"\n[Test Case {i}] User Request: \"{query}\"")
        print(f"Selected Workflow: {output['selected_workflow']}")
        print("Result:")
        print(json.dumps(output['result'], indent=2))
        print("-" * 80)

if __name__ == "__main__":
    main()