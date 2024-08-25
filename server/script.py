import subprocess
import docker
import re
from docker.errors import APIError
import docker.errors
import crud

APACHE_CONFIG = '/etc/apache2/sites-available/000-default.conf'

def find_available_port(start_port=8000, end_port=9000) -> int:
    client = docker.from_env()
    used_ports = set(container.attrs['NetworkSettings']['Ports'].keys() 
                     for container in client.containers.list())
    
    for port in range(start_port, end_port):
        if not any(str(port) in p for p in used_ports):
            return port
    raise Exception("No available ports")

def reload_apache() -> None:
    subprocess.run(['sudo', 'systemctl', 'reload', 'apache2'])

def update_apache_config(app_name, port, method=1) -> None: #method = 1 for adding and 0 for deleting
     with open(APACHE_CONFIG, 'r') as f:
          config = f.read()
     line = f"    SetEnvIf Host ^{app_name}\.${{DOMAIN}}$ DOCKER_PORT={port}\n"

     if method:
          # Find the last SetEnvIf line and add the new one after it
          last_setenvif = list(re.finditer(r'^\s*SetEnvIf\s+Host\s+\^.*\\\.\$\{DOMAIN\}\$\s+DOCKER_PORT=\d+$', config, re.MULTILINE))[-1]
          insert_position = last_setenvif.end() + 1

          new_config = config[:insert_position] + line + config[insert_position:]
     else:
          pattern = re.escape(line)
          new_config = re.sub(pattern, '', config)

     with open(APACHE_CONFIG, 'w') as f:
          f.write(new_config)
     
def deploy(image_name: str, port_to_listen: int, subdomain_name: str) -> list:
     """
     Get the image -> Find a free port -> map the port_to_listen to assigned port -> deploy and get the container id
     -> update database and apache config
     """
     client = docker.from_env()
     try:
          client.images.pull(image_name)
     except APIError:
         return ["container image does not exist", image_name]
     
     port_no = find_available_port()

     container = client.containers.run(
          image_name,
          ports={f"{port_to_listen}/tcp": port_no},
          detach=True,
          restart_policy={"Name": "always"} #for starting the running containers automatically after restart
     )

     register = crud.create_item(subdomain_name, container.id, port_no)

     hostname = update_apache_config(subdomain_name, port_no)
     reload_apache() 

     return [image_name, hostname]

def delete(subdomain_name: str) -> str:
     """
     fetch container id from db -> stop and remove the container -> remove unused images -> delete from the apache
     -> reload apache -> send confirmation
     """
     client = docker.from_env()
     container_info = crud.read_item(subdomain_name)
     port_no = 0
     if container_info:
          container = client.containers.get(container_info.container_id)
          port_no = container_info.assigned_port
          try:
              container.stop()
              container.remove()
          except docker.errors.NotFound:
              return None
          except docker.errors.APIError as e:
              return None
          subprocess.run(['docker', 'image', 'prune', '-a', '-f'])

          crud.delete_item(subdomain_name)
     else:
         return None
     
     update_apache_config(subdomain_name, port_no, 0)
     reload_apache()

     return "Success"


