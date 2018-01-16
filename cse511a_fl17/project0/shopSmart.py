# shopSmart.py
# ------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""

import shop

def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """    
    "*** YOUR CODE HERE ***"
    cost1 = 0.0
    cost2 = 0.0
    for i in range(0,len(orderList),1):
        if orderList[i][0] == 'apples':
            applePrice1 = fruitShops[0].getCostPerPound('apples')
            cost1=cost1+(orderList[i][1]*applePrice1)
            applePrice2 = fruitShops[1].getCostPerPound('apples')
            cost2=cost2+(orderList[i][1]*applePrice2)
        elif orderList[i][0] == 'oranges':
            organePrice1= fruitShops[0].getCostPerPound('oranges')
            cost1=cost1+(orderList[i][1]*organePrice1)
            organePrice2 = fruitShops[1].getCostPerPound('oranges')
            cost2 = cost2 + (orderList[i][1] * organePrice2)

    if cost1 > cost2:
        return fruitShops[1]
    else:
        return fruitShops[0]
    
if __name__ == '__main__':
  "This code runs when you invoke the script from the command line"
  orders = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  print "For orders ", orders, ", the best shop is", shopSmart(orders, shops).getName()
  orders = [('apples',3.0)]
  print "For orders: ", orders, ", the best shop is", shopSmart(orders, shops).getName()

