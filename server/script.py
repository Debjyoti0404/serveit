import subprocess

def deploy(cont_name: str) -> list:
    #with open('/etc/cloudflared/config.yml', 'r', encoding='utf-8') as file: 
    #data = file.readlines() 

    #print(data) 
    #data[1] = "Here is my modified Line 2\n"

    #with open('example.txt', 'w', encoding='utf-8') as file: 
    #file.writelines(data) 

    process = subprocess.Popen(["sudo", "echo", "hello"], stdout=subprocess.PIPE)
    output = process.communicate()

    return [output, cont_name]

