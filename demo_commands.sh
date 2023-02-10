
#!/bin/zsh
export SC_HOST="https://ia01b-01.lab.local"  #"https://10.200.2.226"
export SC_USERNAME="admin"
export SC_PASSWORD="admin"
clear
read -p "View complete inventory run ansible-inventory --graph  " -n1 -s
echo "run ansible-inventory --graph"
echo
ansible-inventory --graph
echo
read -p "Review Iventory - Press any key to run 'ansible-playbook -i ./inventory/cluster_inventory.yml Fleet_HyperCore_Config.yml -l staging'  " -n1 -s
echo
ansible-playbook -i ./inventory/cluster_inventory.yml Fleet_HyperCore_Config.yml -l staging
echo
echo "Review summary - Fleet_HypercoreConfig complete - check pharmacy cloud-init"
echo 
read -p "In-Guest deployment - Press any key to run 'ansible-inventory -i ./inventory/hypercore_vm_inventory.yml --graph'  " -n1 -s
ansible-inventory -i ./inventory/hypercore_vm_inventory.yml --graph
echo 
read -p "Deploy container into guests - Press any key to run 'ansible-playbook -i ./inventory/hypercore_vm_inventory.yml using_hypercore_inventory.yml '  " -n1 -s
echo 
ansible-playbook -i ./inventory/hypercore_vm_inventory.yml using_hypercore_inventory.yml 
echo 
read -p "show idempotence for new container - Press any key to run 'ansible-playbook -i ./inventory/hypercore_vm_inventory.yml using_hypercore_inventory.yml '  " -n1 -s
echo 
ansible-playbook -i ./inventory/hypercore_vm_inventory.yml using_hypercore_inventory.yml 
echo 
read -p "Register Linux VMs to Azure Arc - Press any key to run 'ansible-playbook -i ./inventory/hypercore_vm_inventory.yml AzureArcLinuxOnboard.yml  " -n1 -s
echo 
ansible-playbook -i ./inventory/hypercore_vm_inventory.yml AzureArcLinuxOnboard.yml
echo 
#read -p "Fleet-Wide Day2 guest configuration - Press any key to run 'ansible-playbook -i ./inventory/cluster_inventory.yml -l staging Fleet_UseHyperCore_Inventory.yml -v' " -n1 -s
#echo 
ansible-playbook -i ./inventory/cluster_inventory.yml -l staging Fleet_UseHyperCore_Inventory.yml -v 