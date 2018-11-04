'''
Created on Oct 12, 2016

@author: mwittie
'''
import network
import link
import threading
from time import sleep

##configuration parameters
router_queue_size = 0 #0 means unlimited
simulation_time = 1 #give the network sufficient time to transfer all packets before quitting

##routing tables
forward_a = {'server1': 0, 'server2': 1}
forward_b = {'server1': 0, 'server2': 0}
forward_c = {'server1': 0, 'server2': 0}
forward_d = {'server1': 0, 'server2': 1}

if __name__ == '__main__':
    object_L = [] #keeps track of objects, so we can kill their threads
    
    #create network nodes
    client1 = network.Host(1)
    object_L.append(client1)
    
    client2 = network.Host(2)
    object_L.append(client2)
    
    server1 = network.Host(3)
    object_L.append(server1)
    
    server2 = network.Host(4)
    object_L.append(server2)
    
    router_a = network.Router(name='A', intf_count=2, max_queue_size=router_queue_size)
    object_L.append(router_a)
    
    router_b = network.Router(name='B', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(router_b)
    
    router_c = network.Router(name='C', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(router_c)
    
    router_d = network.Router(name='D', intf_count=2, max_queue_size=router_queue_size)
    object_L.append(router_d)
    
    
    #create a Link Layer to keep track of links between network nodes
    link_layer = link.LinkLayer()
    object_L.append(link_layer)
    
    #add all the links
    #link parameters: from_node, from_intf_num, to_node, to_intf_num, mtu
    link_layer.add_link(link.Link(client1, 0, router_a, 0, 50))
    link_layer.add_link(link.Link(client2, 0, router_a, 1, 50))
    link_layer.add_link(link.Link(router_a, 0, router_b, 0, 50))
    link_layer.add_link(link.Link(router_a, 1, router_c, 0, 50))
    link_layer.add_link(link.Link(router_b, 0, router_d, 0, 50))
    link_layer.add_link(link.Link(router_c, 0, router_d, 1, 50))
    link_layer.add_link(link.Link(router_d, 0, server1, 0, 50))
    link_layer.add_link(link.Link(router_d, 1, server2, 0, 50))
    
    
    #start all the objects
    thread_L = []
    thread_L.append(threading.Thread(name=client1.__str__(), target=client1.run))
    thread_L.append(threading.Thread(name=client2.__str__(), target=client2.run))
    thread_L.append(threading.Thread(name=server1.__str__(), target=server1.run))
    thread_L.append(threading.Thread(name=server2.__str__(), target=server2.run))
    thread_L.append(threading.Thread(name=router_a.__str__(), target=router_a.run))
    thread_L.append(threading.Thread(name=router_b.__str__(), target=router_b.run))
    thread_L.append(threading.Thread(name=router_c.__str__(), target=router_c.run))
    thread_L.append(threading.Thread(name=router_d.__str__(), target=router_d.run))
    
    thread_L.append(threading.Thread(name="Network", target=link_layer.run))
    
    for t in thread_L:
        t.start()
    
    
    #create some send events    
    for i in range(3):
        client1.udt_send(2, 'Sample data %d' % i)
    
    
    #give the network sufficient time to transfer all packets before quitting
    sleep(simulation_time)
    
    #join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()
        
    print("All simulation threads joined")



# writes to host periodically