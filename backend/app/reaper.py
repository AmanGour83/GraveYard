import docker
from datetime import datetime, timezone

client = docker.from_env()

def reap_zombies():
    # print("💀 Reaper running...") # Uncomment to see logs
    try:
        containers = client.containers.list(filters={"label": "session_token"})
        
        for container in containers:
            expires_str = container.labels.get("expires_at")
            if not expires_str: continue
                
            expires_at = datetime.fromisoformat(expires_str)
            if datetime.now(timezone.utc) > expires_at:
                print(f"Killing {container.short_id}")
                container.stop(timeout=1)
                container.remove(force=True)
    except Exception as e:
        print(f"Reaper error: {e}")