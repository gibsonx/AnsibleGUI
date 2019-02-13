from common.InventoryGen import DynamicInventory

def _example1():
    # test inventory
    resource={'group1':{'hosts':[{'hostid':'localhost','hostname':'h1','hostip':'127.0.0.1','username':'root',
                                  'password':'123456','port':'22','sshkey':'','k1':'v1'},
                                 ],
                        'groupvars':{"g1key":"g1value"}},
              }
    # test inventory
    iobj=DynamicInventory(resource)
    iobj.testcase()


if __name__ == '__main__':
    _example1()