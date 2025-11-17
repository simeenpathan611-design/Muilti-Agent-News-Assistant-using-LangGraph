# Entry point for AI Newsletter Agent

# if __name__ == '__main__':
#     print('Run the AI Newsletter Agent workflow...')

# main.py

from langgraph_workflow.graph_definition import run_newsletter_workflow

if __name__ == "__main__":
    print("🚀 Running complete AI Newsletter workflow...")
    result = run_newsletter_workflow()
    print("\n✅ Workflow Summary:")
    for k, v in result.items():
        print(f"{k}: {v}")

