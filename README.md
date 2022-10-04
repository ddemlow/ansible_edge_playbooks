# ansible_edge_playbooks

Fleet_Config.yml is the main playbook that imports other playbooks and roles for edge VM deployment and configuration

Individual playbooks and roles exist for each VM to be deployed and configured including an Ubuntu 20.04 cloud image that is used when initially creating each workload VM - pharmacy, pos, and security VMs

The template is checked first using scale_computing.hypercore.vm_import module which will import the VM using parameters from inventory file if the template doesn't exist.  Once it does the next task uses scale_computing.hypercore.vm_params to set various attributes on the template VM including setting vcpus = 0 which will prevent the template from accidentally being started which may destroy it's ability to be used as a provisioning template. 

For eaxh workload VM - the role will use the scale_computing.hypercore.vm_clone module to determine if the VM exists and if it does not will clone VM from template providing cloud-init data to configure each VM using variables from inventory

If the VM exists, or after it is clone, next task uses scale_computing.hypercore.vm_disk module to set disk configuration including resizing disks and creating any additional virtual disks specified.

Following that task - the scale_computing.hypercore.vm_params: module configures specified virtual machine paramters including power_state: start which will result in the VM being started if it is not.

Below is an example of what a specific site configuration should look like
<img width="1366" alt="image" src="https://user-images.githubusercontent.com/26821128/193714990-73bdfc08-f374-4092-8369-b91b16e44bfc.png">

