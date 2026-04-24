from google import genai
from google.genai import types
import json
import os
from k8s_tools import get_pod_status, get_pod_logs, get_pod_events

# Configure Gemini
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Define tools as functions for Gemini
def get_pod_status_tool(namespace: str) -> str:
    """Get all pods in a namespace with their status, conditions and container states"""
    result = get_pod_status(namespace)
    return json.dumps(result, indent=2)

def get_pod_logs_tool(namespace: str, pod_name: str, tail: int = 50) -> str:
    """Get the last N lines of logs from a specific pod"""
    result = get_pod_logs(namespace, pod_name, tail)
    return result

def get_pod_events_tool(namespace: str) -> str:
    """Get warning events in a namespace to understand what is going wrong"""
    result = get_pod_events(namespace)
    return json.dumps(result, indent=2)

available_tools = {
    "get_pod_status_tool": get_pod_status_tool,
    "get_pod_logs_tool": get_pod_logs_tool,
    "get_pod_events_tool": get_pod_events_tool,
}

def run_agent(namespace: str, user_query: str):
    """Main agent loop using Gemini"""

    system_prompt = """You are a Kubernetes troubleshooting expert agent.
Your job is to investigate issues in a Kubernetes cluster and provide clear diagnosis and fixes.

When given a namespace or problem:
1. First check pod status
2. Get events to understand warnings
3. Fetch logs if needed
4. Provide a clear diagnosis and exact fix commands

Always end with:
- 🔍 Root Cause
- 🛠️ Fix (with exact kubectl commands)
- 🛡️ Prevention tip"""

    print(f"\n🤖 Agent starting investigation on namespace: {namespace}\n")
    print("-" * 50)

    messages = [f"{user_query}\nNamespace: {namespace}"]

    # Agent loop
    while True:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[get_pod_status_tool, get_pod_logs_tool, get_pod_events_tool],
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=False
                )
            ),
            contents=messages
        )

        # Check for tool calls
        has_tool_call = False
        if not response.candidates or not response.candidates[0].content:
            print("No response from Gemini, retrying...")
            continue
        for part in response.candidates[0].content.parts:
            if part.function_call:
                has_tool_call = True
                tool_name = part.function_call.name
                tool_args = dict(part.function_call.args)
                print(f"🔧 Calling tool: {tool_name}({tool_args})")
                result = available_tools[tool_name](**tool_args)
                print(f"📊 Result preview: {result[:200]}...\n")

        if not has_tool_call:
            print("-" * 50)
            print("\n📋 AGENT DIAGNOSIS:\n")
            print(response.text)
            break

        # Add response to messages and continue
        messages.append(response.candidates[0].content)