import requests
from prettytable import PrettyTable
import os

key = os.environ.get('SECRET_KEY')
address = '192.168.12.105'

header = {'Authorization': f'jwt {key}'}

raw_data_vm = requests.get(
            f'http://{address}/api/domains', headers=header)
VMs = []
VM_ids = []
if raw_data_vm.status_code == 200:
    data_vm = raw_data_vm.json()
    print('OK')
    number_of_VM = data_vm['count']


    for i in range(number_of_VM):
        if not data_vm['results'][i]['template']:
            VMs.append(data_vm['results'][i]['verbose_name'])
            VM_ids.append(data_vm['results'][i]['id'])


    print('Список виртуальных машин:')
    for i in range(len(VMs)):
        print(i + 1, " ", VMs[i])
else:
    print('Huston, we have a problem!')

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
    for host in hosts:
        print(host)

else:
    print('Huston, we have a problem!')
print()
print()

print('Инвентаризация ВМ')

table = []

with open("inventoryVM.csv", "w") as inventory_file:
    inventory_file.write("Name," + "CPU," + "Memory," + "OS," + "Interfaces," + "Disks," + "LUNs," + "Placed on node, " \
                         + "Total uptime, " + "CPU usage %, " + "Memory usage %, " + '\n')
    # print('+---------------------+-----+--------+--------------------------------------------------+-------------+-------+------+')
    # print('| Name                | CPU | Memory | OS                                               | Interfaces  | Disks | LUNs |')
    # print(
    #     '+---------------------+-----+--------+--------------------------------------------------+-------------+-------+------+')
    for i in range(len(VM_ids)):
        vm_info = requests.get(
            f'http://{address}/api/domains/{VM_ids[i]}', headers=header).json()
        inventory_table_line = []
        # print()
        # print()
        # print(vm_info['verbose_name'])
        # print('CPU: ', vm_info['cpu_topology']['cpu_count'])
        # print('Memory: ', vm_info['memory_count'])
        # print('OS: ', vm_info['os_version'])
        # print('Interfaces:', vm_info['vmachine_infs_count'])
        # print('Disks: ', vm_info['vdisks_count'])
        # print('LUNs: ', vm_info['luns_count'])
        # print('Размещен на ноде: ', vm_info['node']['verbose_name'])
        # print('Всего uptime: ', vm_info['uptime_total'])
        # print('Задействовано CPU: ', vm_info['cpu_used_percent_user'], '%')
        # print('Задействовано ОЗУ: ', vm_info['mem_used_percent_user'], '%')
        inventory_table_line.append(vm_info['verbose_name'])
        inventory_table_line.append(vm_info['cpu_topology']['cpu_count'])
        inventory_table_line.append(vm_info['memory_count'])
        inventory_table_line.append(vm_info['os_version'])
        inventory_table_line.append(vm_info['vmachine_infs_count'])
        inventory_table_line.append(vm_info['vdisks_count'])
        inventory_table_line.append(vm_info['luns_count'])
        inventory_table_line.append(vm_info['node']['verbose_name'])
        inventory_table_line.append(vm_info['uptime_total'])
        inventory_table_line.append(vm_info['cpu_used_percent_user'])
        inventory_table_line.append(vm_info['mem_used_percent_user'])
        inventory_line1 = vm_info['verbose_name'] + ',' + str(vm_info['cpu_topology']['cpu_count']) +','
        inventory_line2 = str(vm_info['memory_count']) + ',' + vm_info['os_version'] + ','
        inventory_line3 = str(vm_info['vmachine_infs_count']) + ',' + str(vm_info['vdisks_count']) + ','
        inventory_line4 = str(vm_info['luns_count']) + ',' + vm_info['node']['verbose_name'] + ','
        inventory_line5 = str(vm_info['uptime_total']) + ',' + str(vm_info['cpu_used_percent_user']) + ','
        inventory_line6 = str(vm_info['mem_used_percent_user'])
        inventory_line = inventory_line1 + inventory_line2 + inventory_line3 + inventory_line4 + inventory_line5 + inventory_line6
        # print(inventory_line)
        # print(inventory_table_line)
        table.append(inventory_table_line)
        inventory_file.write(inventory_line + "\n")

inventoryVMtable = PrettyTable()
inventoryVMtable.field_names = ["Name", "CPU", "Memory", "OS", "Interfaces", "Disks", "LUNs", "Placed on node", \
                         "Total uptime", "CPU usage %", "Memory usage %"]
inventoryVMtable.add_rows(table)
inventoryVMtable.align = 'l'
print(inventoryVMtable)

host_id = data_nodes['results'][0]['id']

hw_info_raw = requests.get(
            f'http://{address}/api/nodes/{host_id}/hw-info', headers=header)
processor_count = 0
memory_count = 0
disk_count = 0
if hw_info_raw.status_code == 200:
    hw_info = hw_info_raw.json()['children'][0]['children']
    hw_info_all = hw_info_raw.json()
    for i in range(len(hw_info)):
        if hw_info[i]['class'] == 'processor':
            processor_count += 1
            processor = hw_info[i]['product']
        elif hw_info[i]['class'] == 'memory' and hw_info[i]['description'] not in ['BIOS', 'L1 cache', 'L2 cache', 'L3 cache']:
            memory_info = hw_info[i]['children']

    for i in range(len(memory_info)):
        if memory_info[i]['class'] == 'memory':
            memory_count += 1
            memory = memory_info[i]['description']


else:
    print('Huston, we have a problem!')

print()
print()
print('Инвентаризация хостов')
print('Хост: ', data_nodes['results'][0]['verbose_name'])
print(hw_info_all['children'][0]['product'])
print('CPU', processor_count, 'x', processor)
print('Memory', memory_count, 'x', memory)

