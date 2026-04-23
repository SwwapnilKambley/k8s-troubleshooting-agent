markdown# 🤖 K8s Troubleshooting Agent

An AI-powered Kubernetes troubleshooting agent that investigates pod issues and provides diagnosis and fixes — automatically.

Built with **Gemini AI** + **Kubernetes Python SDK**.

---

## 🧠 How It Works

```
You provide a namespace
        ↓
Agent fetches pod status, events, logs (via K8s API)
        ↓
Gemini AI reasons over the data
        ↓
Returns diagnosis + exact kubectl fix commands
```

---

## 🛠️ Tech Stack

- **Google Gemini 2.5 Flash** — LLM reasoning engine
- **Kubernetes Python SDK** — cluster data fetching
- **Minikube** — local K8s cluster for testing
- **Python 3.9+**

---

## 📁 Project Structure

```
k8s-troubleshooting-agent/
├── agent/
│   ├── main.py          # Entry point
│   ├── k8s_tools.py     # K8s API tools (pods, logs, events)
│   └── llm_agent.py     # Gemini-powered reasoning loop
├── k8s/
│   └── test-app/
│       └── broken-deployment.yaml   # Sample broken app
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- `kubectl` configured (Minikube or real cluster)
- Gemini API key from [aistudio.google.com](https://aistudio.google.com)

### Installation

```bash
# Clone the repo
git clone https://github.com/SwwapnilKambley/k8s-troubleshooting-agent.git
cd k8s-troubleshooting-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set your Gemini API key
export GEMINI_API_KEY="your-key-here"
```

### Deploy a test broken app

```bash
kubectl create namespace demo
kubectl apply -f k8s/test-app/broken-deployment.yaml
```

### Run the agent

```bash
cd agent
python main.py demo
```

---

## 🔍 Example Output

```
🤖 Agent starting investigation on namespace: demo

🔧 Calling tool: get_pod_status_tool({'namespace': 'demo'})
🔧 Calling tool: get_pod_events_tool({'namespace': 'demo'})

📋 AGENT DIAGNOSIS:

🔍 Root Cause
The pod is in ImagePullBackOff state because the image tag
`nginx:this-tag-does-not-exist` does not exist on Docker Hub.

🛠️ Fix
kubectl edit deployment broken-app -n demo
# Change image to: nginx:latest

🛡️ Prevention tip
Always pin exact valid image tags in production.
Use image scanning in your CI/CD pipeline.
```

---

## 🗺️ Roadmap

- [x] ImagePullBackOff detection
- [ ] CrashLoopBackOff diagnosis
- [ ] OOMKilled detection
- [ ] Pending pod (resource limits) diagnosis
- [ ] Slack/webhook alerting
- [ ] GKE + Vertex AI deployment

---

## 👤 Author

**Swwapnil Kambley** — DevOps & Cloud Engineer
GCP ACE | GCP PCA | Terraform Associate | CKA (in progress)

[GitHub](https://github.com/SwwapnilKambley)
