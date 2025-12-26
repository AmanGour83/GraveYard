import docker
import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from .models import Project, DemoSession

client = docker.from_env()

def launch_demo_session(db: Session, project_id: int, duration_minutes: int = 15):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None

    session_token = f"demo-{secrets.token_hex(4)}"
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=duration_minutes)

    try:
        # Ask Docker to assign a random host port
        ports_config = {f"{project.internal_port}/tcp": None}

        container = client.containers.run(
            project.docker_image,
            detach=True,
            mem_limit="512m",
            nano_cpus=500000000,
            ports=ports_config,
            labels={
                "expires_at": expires_at.isoformat(),
                "session_token": session_token
            }
        )

        container.reload()
        # Find the random port assigned by Docker
        host_port = container.attrs['NetworkSettings']['Ports'][f'{project.internal_port}/tcp'][0]['HostPort']

        db_session = DemoSession(
            project_id=project.id,
            session_token=session_token,
            container_id=container.id,
            expires_at=expires_at
        )
        db.add(db_session)
        db.commit()
        return host_port

    except Exception as e:
        print(f"Error launching: {e}")
        return None