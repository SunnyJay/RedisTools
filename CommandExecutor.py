import Configurations
'''
@author: Administrator
'''

cache_info=Configurations.cache_info

sentinel_address=Configurations.sentinel_address
cache_address=Configurations.cache_address
seninel_ip=Configurations.seninel_ip
seninel_port=Configurations.seninel_port
sentinel=Configurations.sentinel
    
command_input=raw_input('Please input the command you want to execute:\n')
command_len=len(command_input.split(' '))
command=command_input.split(' ')[0]
args=command_input.split(' ')
args.remove(command)

confirm=raw_input('Please confirm your input (yes/no):\n')
if confirm!='yes':
    print 'bye....'
    exit()


for cache_node in cache_address:
    master = sentinel.master_for(cache_node)
    print '*******************************************',cache_node,'*******************************************'
    if command_len == 1:
        reply = master.execute_command(command)
    elif command_len == 2:
        reply = master.execute_command(command,args[0])
    else:
        reply = master.execute_command(command,args[0],args[1])
    print reply
    print


