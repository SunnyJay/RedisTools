#-*- coding:gb18030 -*
import Configurations
'''
@author: Administrator
'''
import operator

cache_info=Configurations.cache_info

sentinel_address=Configurations.sentinel_address
cache_address=Configurations.cache_address
seninel_ip=Configurations.seninel_ip
seninel_port=Configurations.seninel_port
sentinel=Configurations.sentinel
sentinel_db1=Configurations.sentinel_db1

#����cache��Ⱥ���ܵ�mstpid����
def findAllMstpIdNum():
    all_num_mstpid = 0
    for cache_node in cache_address:
        master = sentinel_db1.master_for(cache_node)
        mstpid_list = master.keys('*')
        all_num_mstpid += len(mstpid_list)
    return all_num_mstpid

#���ҡ�ͳ��seqId������ָ����Χ�ڵ�mstpid
def findMstpIdWhoseSeqIdIsInSection():
    begin_num = int(raw_input('Please input the begin number of seqId:\n'))
    end_num = int(raw_input('Please input the end number of seqId:\n'))
    if end_num<=begin_num:
        print 'Error Input!'
        exit()
    count = 0
    for cache_node in cache_address:
        master = sentinel_db1.master_for(cache_node)
        mstpid_list = master.keys('*')
        
        for mstpid in mstpid_list:
            mstpid_len =  master.hlen(mstpid)
            if begin_num < mstpid_len < end_num:
                count += 1
                print mstpid,master.hlen(mstpid)
    print 'Rate is',count*1.0/findAllMstpIdNum()*100,'%'
    

#��� ����
def flushDB():
    for cache_node in cache_address:
        print cache_node
    choice = raw_input("Please input the cache address(like 'ip:port') you want to flush. 'all' represents flush all cach nodes")
    
    if choice != all:
        confirm = raw_input('Are you sure to flushDB the cache node? yes/no')
        if confirm != 'yes':
            exit()
        master0 = sentinel.master_for(choice)
        master1= sentinel_db1.master_for(choice)
        master0.flushDB()
        master1.flushDB()
    else:
        confirm = raw_input('Are you sure to flushDB all cache nodes? yes/no')
        if confirm != 'yes':
            exit()
        for cache_node in cache_address:
            master0 = sentinel.master_for(cache_node)
            master1= sentinel_db1.master_for(cache_node)
            master0.flushDB()
            master1.flushDB()
        
    for cache_node in cache_address:
        master0 = sentinel.master_for(cache_node)
        master1= sentinel_db1.master_for(cache_node)
        print cache_node,'\t',master0.dbsize(),'\t',master1.dbsize()

#��ӡĿǰ��Щд�����Ŀͻ���ip
def printWriteClient():
    while True:
        for cache_node in cache_address:
            master = sentinel.master_for(cache_node)
            client_list = master.client_list()
            ip_set = set()
            for client in client_list:
                cmd = client['cmd']
                idle = client['idle']
                if(cmd == 'set' or cmd == 'hset') and idle < 2:
                    ip_set.add(client['addr'].split(':')[0])
            print ip_set
        
        print '*******************************************'
                
                
                
    

#��ӡ��Ⱥ������mstpid�µ�seqid���� 
def findSeqNumOfAllMstpid():
    dict = {}
    for cache_node in cache_address:
        master = sentinel_db1.master_for(cache_node)
        mstpid_list = master.keys('*')
        for mstpid in mstpid_list:
            seqid_list = master.hkeys(mstpid)
            dict.setdefault(mstpid,len(seqid_list))
    sorted_dict = sorted(dict.iteritems(), key=operator.itemgetter(1), reverse=True)    #����seqid�������� Ĭ������
    for item in sorted_dict:
        print item[0],'\t',item[1]
            
            

#ɾ����Ⱥ�����й�ϣ�洢�ṹΪhashtable������ziplist��mstpid
def deleteHashMstpId():
    hash_mstpid_dict = findHashMstpId()
    confirm=raw_input('Are you sure to delete?(yes/no)\n')
    if confirm != 'yes':
        exit()
    for item in hash_mstpid_dict:
        master = sentinel_db1.master_for(hash_mstpid_dict[item])
        master.delete(item)
    print 'deleted num:',len(hash_mstpid_dict)

#���Ҽ�Ⱥ�����й�ϣ�洢�ṹΪhashtable������ziplist��mstpid���Լ������
def findHashMstpId():
    findsets = {}
    for cache_node in cache_address:
        master = sentinel_db1.master_for(cache_node)
        mstpid_list = master.keys('*')
        
        for mstpid in mstpid_list:
            data_type = master.object('encoding',mstpid)
            if data_type == 'hashtable':
                print mstpid, cache_node
                findsets.setdefault(mstpid,cache_node)
    print 'Rate is',len(findsets)*1.0/findAllMstpIdNum()*100,'%'
    return findsets

#����ĳ��mstpid������
def findContentOfMstpId():
    mstpid_input = raw_input('Please input the mstpid:\n')
    isExists,locatin = findWhereIsMstpId(mstpid_input)
    if isExists == False:
        return;
    master = sentinel_db1.master_for(locatin)
    content = master.hgetall(mstpid_input) #����������Ϊpythonû��ziplist�ṹ,�洢���ֵ����Ϊ��ϣֵ����
    data_type = master.object('encoding',mstpid_input)
    master0 = sentinel.master_for(locatin)
    latest_seqId_0 = master0.get(mstpid_input.split('MSTPID')[0]+'SEQ_0')
    latest_seqId_1 = master0.get(mstpid_input.split('MSTPID')[0]+'SEQ_1')
    latest_ackId_0 = master0.hget(mstpid_input.split('MSTPID')[0]+'ACK',0)
    latest_ackId_1 = master0.hget(mstpid_input.split('MSTPID')[0]+'ACK',1)
    print 'latest seqId 0:',latest_seqId_0,'\tlatest seqId 1:',latest_seqId_1
    print 'latest ackId 0:',latest_ackId_0,'\tlatest ackId 1:',latest_ackId_1
    print 'data type:',data_type
    print 'item num:',len(content)
    print 'contents:'
    seqid_list = master.hkeys(mstpid_input)
    for item in seqid_list:
        print item,'\t',content[item]
    

#�����Ƿ����ĳ��mstpid����λ��
def findWhereIsMstpId(mstpid):
    
    isExists = False
    for cache_node in cache_address:
        master = sentinel_db1.master_for(cache_node)
        isExists = master.exists(mstpid)
        if isExists == True:
            locatino = cache_node
            print 'mstpid location:',cache_node
            break
    if isExists == False:
            print 'can not find mstpid:',mstpid
    return isExists,locatino

#����ָ��mstpid��seqid�µ�msgid���Ӧmsgbody
def findMsg():
    mstpid_input = raw_input('Please input the mstpid:\n')
    seqid_input = raw_input('Please input the seqid:\n')
    for cache_node in cache_address:
        master = sentinel_db1.master_for(cache_node)
        msgid = master.hget(mstpid_input,seqid_input)
        if msgid != None:
            print 'mstpid location:',cache_node
            break
    if msgid == None:
        print 'can not find the msgid you want\n'  
        exit() 
    for cache_node in cache_address:
        master = sentinel.master_for(cache_node)
        msgbody = master.get(msgid)
        if msgbody != None:
            print 'message location:',cache_node
            print 'msgid:',msgid
            print 'msgbody:\n',msgbody
            break
#findMsg()
#findContentOfMstpId()
findHashMstpId()
#findSeqNumOfAllMstpid()
#printWriteClient()
#findMstpIdWhoseSeqIdIsInSection()