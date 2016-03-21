from redis.sentinel import Sentinel
'''
@author: Administrator
'''
cache_info='192.168.1.214:26379;192.168.1.215:26379;192.168.1.216:26379;192.168.1.217:26379;192.168.1.218:26379\
_192.168.1.219:6379;192.168.1.221:6379;192.168.1.223:6379;192.168.1.225:6379'


sentinel_address=cache_info.split('_')[0].split(';')
cache_address=cache_info.split('_')[1].split(';')
seninel_ip=sentinel_address[0].split(':')[0]
seninel_port=sentinel_address[0].split(':')[1]
sentinel=Sentinel([(seninel_ip,seninel_port)])
sentinel_db1=Sentinel([(seninel_ip,seninel_port)],db=1)