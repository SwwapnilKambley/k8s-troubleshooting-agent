from kubernetes import client, config

def load_k8s_config():
    """Load kubeconfig (works with minikube locally)"""
    config.load_kube_config()

def get_pod_status(namespace: str) -> list[dict]:
    """Get all pods in a namespace with their status"""
    load_k8s_config()
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace)
    
    result = []
    for pod in pods.items:
        result.append({
            "name": pod.metadata.name,
            "status": pod.status.phase,
            "conditions": [
                {"type": c.type, "status": c.status, "reason": c.reason}
                for c in (pod.status.conditions or [])
            ],
            "containers": [
                {
                    "name": cs.name,
                    "ready": cs.ready,
                    "restart_count": cs.restart_count,
                    "state": str(cs.state)
                }
                for cs in (pod.status.container_statuses or [])
            ]
        })
    return result

def get_pod_logs(namespace: str, pod_name: str, tail: int = 50) -> str:
    """Get last N lines of logs from a pod"""
    load_k8s_config()
    v1 = client.CoreV1Api()
    try:
        logs = v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            tail_lines=tail
        )
        return logs if logs else "No logs available"
    except Exception as e:
        return f"Could not fetch logs: {str(e)}"

def get_pod_events(namespace: str) -> list[dict]:
    """Get events in a namespace (warnings, errors)"""
    load_k8s_config()
    v1 = client.CoreV1Api()
    events = v1.list_namespaced_event(namespace)
    
    result = []
    for event in events.items:
        if event.type == "Warning":  # Only grab warnings
            result.append({
                "reason": event.reason,
                "message": event.message,
                "object": event.involved_object.name,
                "count": event.count
            })
    return result