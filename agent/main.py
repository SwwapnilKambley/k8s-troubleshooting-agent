import sys
from llm_agent import run_agent

def main():
    print("🚀 K8s Troubleshooting Agent")
    print("=" * 50)
    
    # Get namespace from argument or ask user
    if len(sys.argv) > 1:
        namespace = sys.argv[1]
    else:
        namespace = input("Enter namespace to investigate: ").strip()
    
    query = "Investigate all pods in this namespace. Find any issues and provide diagnosis and fix."
    
    run_agent(namespace, query)

if __name__ == "__main__":
    main()