import subprocess

def deploy(cont_name: str) -> list:
    process = subprocess.Popen(["sudo", "echo", "hello"], stdout=subprocess.PIPE)
    data = process.communicate()

    return [data, cont_name]

