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


for cache_node in cache_address:
    
    master = sentinel.master_for(cache_node)
    mem_size = master.info('memory')["used_memory_human"]
    dbsize0 = master.info('keyspace')["db0"]['keys']
    dbsize1 = master.info('keyspace')["db1"]['keys']
    role = master.info('replication')['role']
    slave_num = master.info('replication')["connected_slaves"]
    slave_info = master.info('replication')["slave0"]
    uptime = master.info('server')["uptime_in_days"]
    print '*******************************************',cache_node,'*******************************************'
    print 'mem_size:',mem_size
    print 'dbsize0:',dbsize0,' dbsize1:',dbsize1
    print 'role:',role
    #print 'slave_num:',slave_num
    print 'slave_info:',slave_info
    print 'uptime:',uptime,'days'
    

