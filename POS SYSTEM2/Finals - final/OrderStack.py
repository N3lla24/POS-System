class Node:     # Using Singly Linked List
    def __init__(self, data):
        self.next = None
        self.data = data


class Singly:
    def __init__(self):
        self.head = None

    # Insertion of items
    def queue_insertion(self, data):
        node = Node(data)
        if self.head:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
        else:
            self.head = node

    # Delete item
    def delete_item(self, search_button):
        if self.head:
            current = self.head
            button = current.data['BtnObject']
            if search_button == button:         # Checking if inputted id is found at the first node or head
                print('\nItem Deleted')
                orderitem = current.data
                for key, value in orderitem.items():
                    print(key, ' : ', value)
                print()
                self.head = self.head.next
            else:                       # Checking if inputted id is found after the head
                try:
                    while button != search_button:      # Traversing the list
                        pre_current = current   # To find the matching id
                        current = current.next
                        button = current.data['BtnObject']
                    print('\nItem Deleted')
                    pre_current.next = current.next     # Deleting the node that matches the inputted id
                except:                 # If inputted id is not found, error message will display
                    print('Item not Found')
        else:
            print('List of items is empty')


    # Total Number of items 
    def total_items(self):
        num = 0
        if self.head:
            current = self.head
            while current:
                num += 1
                current = current.next
            return num
        else:
            return num
        
    def calcu_total_price(self):
        total = 0
        if self.head:
            current = self.head
            while current:
                total += current.data['Price']
                current = current.next
            return total
        else:
            return total
        
    def get_order_name(self, seqnum):
        if self.head:
            i = 1
            current = self.head
            while i < seqnum:
                current = current.next
                i += 1
            return current.data['Order Name']
        else:
            return None
        
    def get_order_quant(self, seqnum):
        if self.head:
            i = 1
            current = self.head
            while i < seqnum:
                current = current.next
                i += 1
            return current.data['Quantity']
        else:
            return None
    
    def get_order_price(self, seqnum):
        if self.head:
            i = 1
            current = self.head
            while i < seqnum:
                current = current.next
                i += 1
            return current.data['Price']
        else:
            return None
        
    def get_prod_num(self, seqnum):
        if self.head:
            i = 1
            current = self.head
            while i < seqnum:
                current = current.next
                i += 1
            return current.data['ProdNum']
        else:
            return None

    # Display all items
    # def display(self):
    #     if self.head:
    #         current = self.head
    #         while current:
    #             orderitems = current.data
    #             for key, value in orderitems.items():
    #                 str = "" + key + ' : ' + value + "\n"
    #                 displaystr = f'{displaystr}{str}'
    #             current = current.next
    #         return displaystr
    #     else:
    #         return('List of items is empty')