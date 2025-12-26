from pydantic import BaseModel, field_validator
import re

class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    docker_image: str
    internal_port: int

    @field_validator('internal_port')
    def validate_port(cls, v):
        if not (1 <= v <= 65535):
            raise ValueError('Port must be between 1 and 65535')
        return v

    @field_validator('docker_image')
    def validate_docker_image(cls, v):
        # Allow standard format (repo/image:tag)
        pattern = r'^[\w\-\./]+(:[\w\-\.]+)?$'
        if not re.match(pattern, v):
            raise ValueError('Invalid Docker image format.')
        return v

class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        from_attributes = True