class RBTreeNode:
    #declaring the structure of a node in redblack tree
    def __init__(self, user_id= None, seat_id = None, color = "red", parent = None):
        self.user_id = user_id
        self.seat_id = seat_id
        self.color = color
        self.parent = parent
        self.left = None
        self.right = None

class RBTree:
    def __init__(self):
        self.null = RBTreeNode(color = "black")
        self.null.left = self.null
        self.null.right = self.null
        self.root = self.null
        self.print_value = ""
    
    def insert_node(self, user_id, seat_id):
        new_node = RBTreeNode(user_id=user_id, seat_id=seat_id, color="red")
        new_node.left = self.null
        new_node.right = self.null
        if self.root == self.null: #empty tree
            self.root = new_node
            new_node.color = "black"
        else:
            curr = self.root
            while True:
                if new_node.seat_id < curr.seat_id:#traversing to get the position of insertion
                    if curr.left == self.null:
                        curr.left = new_node
                        new_node.parent = curr
                        break
                    curr = curr.left
                else:
                    if curr.right == self.null:
                        curr.right = new_node
                        new_node.parent = curr
                        break
                    curr = curr.right

        self.balance_insertion(new_node) #balancing of tree post insertion (fix color and rotations)
    
    def balance_insertion(self, node):
        while node != self.root and node.parent.color == "red":
            if node.parent == node.parent.parent.left:
                u = node.parent.parent.right  # uncle node
                if u.color == "red":  # uncle is red
                    node.parent.color = "black"
                    u.color = "black"
                    node.parent.parent.color = "red"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:  # node is right child
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = "black"  # node is left child
                    node.parent.parent.color = "red"
                    self.right_rotate(node.parent.parent)
            else:
                u = node.parent.parent.left  # uncle node
                if u.color == "red":  # uncle is red
                    node.parent.color = "black"
                    u.color = "black"
                    node.parent.parent.color = "red"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:  # node is left child
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = "black"# node is right child
                    node.parent.parent.color = "red"
                    self.left_rotate(node.parent.parent)
        self.root.color = "black"  # root is always black


    def right_rotate(self, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right != self.null:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child


    def left_rotate(self, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left != self.null:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child


    def inorder_helper(self, node): # helper to traverse tree inorder recursively
      if node != self.null:
        self.inorder_helper(node.left)
        self.print_value += f"Seat {node.seat_id}, User {node.user_id} \n"
        self.inorder_helper(node.right)  
    
    def inorder_traversal(self):
            self.inorder_helper(self.root)
            output = self.print_value
            self.print_value = ""
            return output

    def delete_node(self, user_id,seat_id,cancel=True): 
        node_to_delete = self.search_tree_helper(user_id) #checks if node is present
        if node_to_delete == None: #exit if not present
            # print(f"User ID {user_id} not found in the tree.")
            return False
        elif cancel and node_to_delete.seat_id!=seat_id: #user id is present but the seat mentioned for deletion is not the same mapped 
            # print(f"User {user_id} has no reservation for seat {seat_id} to cancel")#cannot delete as seat is not present
            return False

        original_color = node_to_delete.color
        if node_to_delete.left == self.null:
            x = node_to_delete.right
            self.transplant(node_to_delete, node_to_delete.right) #replacing subtrees
        elif node_to_delete.right == self.null:
            x = node_to_delete.left
            self.transplant(node_to_delete, node_to_delete.left)
        else:
            y = self.minimum(node_to_delete.right)
            original_color = y.color
            x = y.right
            if y.parent == node_to_delete:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = node_to_delete.right
                y.right.parent = y

            self.transplant(node_to_delete, y)
            y.left = node_to_delete.left
            y.left.parent = y
            y.color = node_to_delete.color

        if original_color == "black":
            self.fix_delete(x)
        return True

    def fix_delete(self, x): #maintaining the property of redblack tree post deletion. x is the replaced node possibly causing disturbances in rb tree props
        while x != self.root and x.color == "black":
            if x == x.parent.left:#x is left child
                s = x.parent.right #s is sibling of x
                if s.color == "red":#update color to black and update parent colors occordingly
                    s.color = "black"
                    x.parent.color = "red"
                    self.left_rotate(x.parent)
                    s = x.parent.right
                if s.left.color == "black" and s.right.color == "black":#s and its children colored black  
                    s.color = "red"
                    x = x.parent
                else: #s ->black, s->left is red and s->right is black
                    if s.right.color == "black":
                        s.left.color = "black"
                        s.color = "red"
                        self.right_rotate(s)
                        s = x.parent.right
                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.right.color = "black"
                    self.left_rotate(x.parent)
                    x = self.root
            else:#x is right child and similar cases for sibling x
                s = x.parent.left
                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self.right_rotate(x.parent)
                    s = x.parent.left
                if s.right.color == "black" and s.left.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    if s.left.color == "black":
                        s.right.color = "black"
                        s.color = "red"
                        self.left_rotate(s)
                        s = x.parent.left
                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.left.color = "black"
                    self.right_rotate(x.parent)
                    x = self.root #breaks loop
        x.color = "black" #root is always black

    def transplant(self, node_to_replace, replacement_node):
        if node_to_replace.parent is None: # if node_to_replace is the root, set the replacement_node as the new root
            self.root = replacement_node
        elif node_to_replace == node_to_replace.parent.left: #if node to replace is left child parent left pointer to be updated
            node_to_replace.parent.left = replacement_node
        else:#lese parent right pointer to be update
            node_to_replace.parent.right = replacement_node
        if replacement_node is not None: #set the parent to parent of node to replace
            replacement_node.parent = node_to_replace.parent

    def minimum(self, node): #finds min
        while node.left != self.null:
            node = node.left
        return node

    def search_tree_helper(self, user_id): 
        return self.inorder_search(self.root, user_id) 

    def inorder_search(self, node, user_id): #recursively searching the subtrees of node for value user_id
        if node == self.null:
            return None
        if node.user_id == user_id:
            return node
        left_result = self.inorder_search(node.left, user_id)
        if left_result:
            return left_result
        return self.inorder_search(node.right, user_id)
