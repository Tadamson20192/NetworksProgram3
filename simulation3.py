'''
Created on Oct 12, 2016

@author: mwittie
'''
import network2 as network
import link2 as link
import threading
from time import sleep

##configuration parameters
router_queue_size = 0 #0 means unlimited
simulation_time = 2 #give the network sufficient time to transfer all packets before quitting
#set of routing tables where the key is the destination and the value is the link out of the router
routingTables = [{3:0, 4:1},{3:0},{4:0},{3:0,4:1}]

if __name__ == '__main__':
    object_L = [] #keeps track of objects, so we can kill their threads
    
    #create network nodes
    clientA = network.Host(1)
    clientB = network.Host(2)
    object_L.append(clientA)
    object_L.append(clientB)
    serverA = network.Host(3)
    serverB = network.Host(4)
    object_L.append(serverA)
    object_L.append(serverB)
    router_A = network.Router(name='A', intf_count=2, max_queue_size=router_queue_size, routingTables[0])
    router_B = network.Router(name='B', intf_count=1, max_queue_size=router_queue_size, routingTables[1])
    router_C = network.Router(name='C', intf_count=2, max_queue_size=router_queue_size, routingTables[2])
    router_D = network.Router(name='D', intf_count=1, max_queue_size=router_queue_size, routingTables[3])
    object_L.append(router_A)
    object_L.append(router_B)
    object_L.append(router_C)
    object_L.append(router_D)
	
	
	
	
    #create a Link Layer to keep track of links between network nodes
    link_layer = link.LinkLayer()
    object_L.append(link_layer)
    
    #add all the links
    #link parameters: from_node, from_intf_num, to_node, to_intf_num, mtu
    link_layer.add_link(link.Link(clientA, 0, router_A, 0, 50))
    link_layer.add_link(link.Link(clientB, 1, router_A, 1, 50))
    link_layer.add_link(link.Link(router_A, 0, router_B, 0, 30))
    link_layer.add_link(link.Link(router_A, 1, router_C, 0, 30))
    link_layer.add_link(link.Link(router_B, 0, router_D, 0, 30))
    link_layer.add_link(link.Link(router_C, 0, router_D, 1, 30))
    link_layer.add_link(link.Link(router_D, 0, serverA, 0, 30))
    link_layer.add_link(link.Link(router_D, 1, serverB, 0, 30))
    
    #start all the objects
    thread_L = []
    thread_L.append(threading.Thread(name=clientA.__str__(), target=clientA.run))
    thread_L.append(threading.Thread(name=clientB.__str__(), target=clientB.run))
    thread_L.append(threading.Thread(name=server.__str__(), target=serverA.run))
    thread_L.append(threading.Thread(name=serverB.__str__(), target=serverB.run))
    thread_L.append(threading.Thread(name=router_A.__str__(), target=router_A.run))
    thread_L.append(threading.Thread(name=router_B.__str__(), target=router_B.run))
    thread_L.append(threading.Thread(name=router_C.__str__(), target=router_C.run))
    thread_L.append(threading.Thread(name=router_D.__str__(), target=router_D.run))
    
    thread_L.append(threading.Thread(name="Network", target=link_layer.run))
    
    for t in thread_L:
        t.start()
    
    
    #create some send events    
    for i in range(1):
        client.udt_send(2, 'This is a really long string of eighty characters. It has to be really really long end.',link_layer.link_L[1].out_intf.mtu)
    
    
    #give the network sufficient time to transfer all packets before quitting
    sleep(simulation_time)
    
    #join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()
        
    print("All simulation threads joined")



# writes to host periodically