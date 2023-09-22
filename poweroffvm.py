import requests
import os

key = os.environ.get('SECRET_KEY')
address = '192.168.12.105'

header = {'Authorization': f'jwt {key}'}

raw_data_vm = requests.get(
            f'http://{address}/api/domains', headers=header)
VMs = []

if raw_data_vm.status_code == 200:
    data_vm = raw_data_vm.json()
    print('OK')
    number_of_VM = data_vm['count']

    for i in range(number_of_VM):
        if (not data_vm['results'][i]['template']):
            VMs.append(data_vm['results'][i]['verbose_name'])

    print('Список виртуальных машин:')
    for i in range(len(VMs)):
        print(i + 1, " ", VMs[i])
else:
    print('Huston, we have a problem!')

user_choice = int(input('Введите номер виртуальной машины для выключения: '))
id = data_vm['results'][user_choice - 1]['id']

poweroff = requests.post(f'http://{address}/api/domains/{id}/shutdown/', headers=header)
if poweroff.status_code == 200:
    print('OK')
else:
    print('Huston, we have a problem!')

user_choice3 = int(input('Включить ВМ? 1 - да, 2 - нет: '))

if user_choice3 == 1:
    startvm = requests.post(f'http://{address}/api/domains/{id}/start/', headers=header)
    if startvm.status_code == 200:
        print('OK')
    else:
        print('Huston, we have a problem!')



