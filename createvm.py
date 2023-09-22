import requests
import os

key = os.environ.get('SECRET_KEY')
address = '192.168.12.105'

header = {'Authorization': f'jwt {key}'}

raw_data_nodes = requests.get(
            f'http://{address}/api/nodes', headers=header)
if raw_data_nodes.status_code == 200:
    data_nodes = raw_data_nodes.json()
    print('OK')
    number_of_hosts = data_nodes['count']
    hosts = []

    for i in range(number_of_hosts):
        hosts.append(data_nodes['results'][i]['verbose_name'])

    print('Список хостов виртуализации:')
    for i in range(len(hosts)):
        print(i + 1, ' ', hosts[i])

else:
    print('Huston, we have a problem!')

node_choice = int(input('Выберите ноду, на которой будет создаваться ВМ: '))
node_id = data_nodes['results'][node_choice - 1]['id']
print(node_id)

raw_data_vm = requests.get(
            f'http://{address}/api/domains', headers=header)

if raw_data_vm.status_code == 200:
    data_vm = raw_data_vm.json()
    print('OK')
    number_of_VM = data_vm['count']
    templates = []

    for i in range(number_of_VM):
        if data_vm['results'][i]['template']:
            templates.append(data_vm['results'][i]['verbose_name'])

    print('Список доступных темплейтов:')
    for i in range(len(templates)):
        print(i + 1, ' ', templates[i])

else:
    print('Huston, we have a problem!')

template_choice = int(input('Выберите шаблон, из которого будет создаваться ВМ: '))
template_id = data_vm['results'][template_choice - 1]['id']
print(template_id)

parameters = {
'verbose_name': 'NewVM',
'node': 'aaba45d5-e6e7-444e-9f90-55331e626006',
'resource_pool': '5341a620-6cab-4358-9bcc-63a89ac7b13f',
'template': False
}

raw_create_vm = requests.post(
            f'http://{address}/api/domains/{template_id}/clone/?async=1', json=parameters, headers=header)
if raw_create_vm.status_code == 200 or raw_create_vm.status_code == 202:
    print('OK')
else:
    print('Huston, we have a problem!', raw_create_vm.status_code)


