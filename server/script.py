import subprocess, yaml
import docker
from docker.errors import APIError

def deploy(image_name: str) -> list:
    client = docker.from_env()
    
    try:
         client.images.pull(image_name)
    except APIError:
         return ["container image does not exist", image_name]

    container = client.containers.run(
        image_name,
        ports={'8000/tcp': 6000},
        detach=True
    )
    
    
    hostname = 'sankha.debsen.co'
    new_record = {
         'hostname': hostname, #fixed for now
         'service': 'https://localhost:6000' #fixed port for now
    }

    with open('/etc/cloudflared/config.yml', 'r', encoding='utf-8') as file: 
	    site_records = yaml.safe_load(file)

    site_records['ingress'].insert(-1, new_record)

    with open('/etc/cloudflared/config.yml', 'w', encoding='utf-8') as file: 
        yaml.safe_dump(site_records, file, default_flow_style=False)
    
    process = subprocess.call(["sudo", "systemctl", "restart", "cloudflared"])

    return [image_name, hostname]

