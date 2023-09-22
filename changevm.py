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
        VMs.append(data_vm['results'][i]['verbose_name'])

    print('Список виртуальных машин:')
    for i in range(len(VMs)):
        print(i + 1, " ", VMs[i])
else:
    print('Huston, we have a problem!')

user_choice = int(input('Введите номер виртуальной машины для изменения: '))
id = data_vm['results'][user_choice - 1]['id']
name = data_vm['results'][user_choice - 1]['verbose_name']
status = data_vm['results'][user_choice - 1]['status']
memory = data_vm['results'][user_choice - 1]['memory_count']
cpus = data_vm['results'][user_choice - 1]['cpu_topology']['cpu_cores']
disks = data_vm['results'][user_choice - 1]['vdisks_count']
interfaces = data_vm['results'][user_choice - 1]['vmachine_infs_count']
node = data_vm['results'][user_choice - 1]['node']['verbose_name']

print('Текущее состояние выбранной ВМ: ')
print('ID: ', id)
print('Name: ', name)
print(status)
print('CPU: ', cpus)
print('Memory: ', memory)
print('Interfaces: ', interfaces)
print('Placed on node: ', node)

print('Мы можем поменять, например, имя машины')
user_choice2 = input('Введите новое имя машины: ')

name_change = {"verbose_name": f'{user_choice2}'}
change_vm = requests.put(
        f'http://{address}/api/domains/{id}/', json=name_change, headers=header)
if change_vm.status_code == 200:
    print('OK')
    new_data = requests.get(f'http://{address}/api/domains/{id}', headers=header).json()

    name = new_data['verbose_name']
    status = new_data['status']
    memory = new_data['memory_count']
    cpus = new_data['cpu_topology']['cpu_cores']
    disks = new_data['vdisks_count']
    node = new_data['node']['verbose_name']

    print('Текущее состояние выбранной ВМ: ')
    print('ID: ', id)
    print('Name: ', name)
    print(status)
    print('CPU: ', cpus)
    print('Memory: ', memory)
    print('Placed on node: ', node)

else:
    print('Huston, we have a problem!', change_vm.status_code)




