import subprocess
import docker
import re
from docker.errors import APIError

APACHE_CONFIG = '/etc/apache2/sites-available/000-default.conf'

def reload_apache():
    subprocess.run(['sudo', 'systemctl', 'reload', 'apache2'])

def update_apache_config(app_name, port):
     with open(APACHE_CONFIG, 'r') as f:
          config = f.read()

     new_line = f"    SetEnvIf Host ^{app_name}\.${{DOMAIN}}$ DOCKER_PORT={port}\n"

     # Find the last SetEnvIf line and add the new one after it
     last_setenvif = list(re.finditer(r'^\s*SetEnvIf', config, re.MULTILINE))[-1]
     insert_position = last_setenvif.end() + 1

     new_config = config[:insert_position] + new_line + config[insert_position:]

     with open(APACHE_CONFIG, 'w') as f:
        f.write(new_config)

     return "app3.debsen.co"
     
def deploy(image_name: str) -> list:
     client = docker.from_env()
     try:
          client.images.pull(image_name)
     except APIError:
         return ["container image does not exist", image_name]
     
     
     container = client.containers.run(
          image_name,
          ports={'8000/tcp': 8003}, #port is fixed for 8003 for now
          detach=True
     )

     hostname = update_apache_config("app3", 8003)
     reload_apache() 

     return [image_name, hostname]
