class MinHeap:
    def __init__(self):
        self.heap = [] 
        self.counter=0 #acts like a timer 
    def insert_single(self, item): #for available seats
        self.heap.append(item)
        self.heapify_insert_single()
    def insert_multi(self,item): #for waitlist insertions
        if len(item) == 3:
            heap_item =[item[0],item[1]*(-1),item[2]] #multiplied with -1 to mimic max-heap
        else:
            heap_item =[item[0],item[1]*(-1),self.counter]
            self.counter+=1
        self.heap.append(heap_item)
        self.heapify_insert_multi()
    def parent_ind(self,curr):#helpers for heapify and remove
        return (curr - 1)//2
    def left_child_ind(self,curr):
        return 1+curr*2 
    def right_child_ind(self,curr):
        return (curr*2) + 2
    def has_left(self,curr):
        val = False
        if self.left_child_ind(curr)<len(self.heap):
            val = True
        return val
    def has_right(self, curr):
        val = False
        if self.right_child_ind(curr)<len(self.heap):
            val = True
        return val
    def has_parent(self, curr):
        val = False
        if curr>0 and self.parent_ind(curr)<len(self.heap):
         val = True
        return val
    def is_leaf(self, curr):
        val = True
        if self.has_right(self,curr) or self.has_left(self,curr):
            val = False
        return val
    def swap(self,i1,i2):
        self.heap[i1], self.heap[i2] = self.heap[i2], self.heap[i1]
    def heapify_insert_single(self): #insertion happens at leaf so 
        curr = len(self.heap) - 1
        while self.has_parent(curr) and self.heap[self.parent_ind(curr)] > self.heap[curr]: #node traverses towards top to find its position by comparing with its parent nodes.
            self.swap(self.parent_ind(curr), curr)
            curr = self.parent_ind(curr)
    def heapify_delete_single(self):#deletions at root by replacing the leaf element with root the replaced element moves towards bottom to find its positions
        curr = 0
        while self.has_left(curr):  # only continue if there's a left child
            smaller_child_ind = self.left_child_ind(curr)#as its moving down, the comparisions will be with the child nodes
            if self.has_right(curr) and self.heap[self.right_child_ind(curr)] < self.heap[smaller_child_ind]:
                smaller_child_ind = self.right_child_ind(curr)
            if self.heap[curr] <= self.heap[smaller_child_ind]:
                break
            else:
                self.swap(curr, smaller_child_ind) #swaps if right child less than left child
            curr = smaller_child_ind

    def remove_single(self, item):#used for deleting available seats 
        try:
            index = self.heap.index(item)
        except ValueError:
            return  
        self.swap(index, len(self.heap) - 1)
        removed_item = self.heap.pop()
        if index < len(self.heap):
            if (self.parent_ind(index) >= 0 and 
                self.heap[index] < self.heap[self.parent_ind(index)]):
                self.heapify_insert_single() #to maintain the min heap properties
            else:
                self.heapify_delete_single()
            
        return removed_item
    
    def remove_multi(self, val):    #only for the waitlist entry removals
        ind = None
        temp = False
        for i, element in enumerate(self.heap):
            if element[0] == val:  # Accessing `user_id` as the first element in the tuple
                ind = i
                temp = True
                break
        if ind is None:
            return False
        self.swap(ind, len(self.heap) - 1)
        removed_item = self.heap.pop()
        if ind < len(self.heap):
            if (self.has_parent(ind) and 
                self.heap[ind][1] < self.heap[self.parent_ind(ind)][1]):
                self.heapify_insert_multi()  # Move up if it's smaller than its parent
            else:
                self.heapify_delete_multi()  # Otherwise, move down if necessary
        
        return temp
            
    def pop_heap_single(self):#lowest seat id for reservations
       if len(self.heap)<1:
          return None
       val = self.heap[0]
       self.heap[0] = self.heap[-1]
       self.heap.pop()
       self.heapify_delete_single()
       return val
    def pop_heap_multi(self):#highest priority user
       if len(self.heap)<1:
          return None
       val = self.heap[0]
       self.heap[0] = self.heap[-1]
       self.heap.pop()
       self.heapify_delete_multi()
       return val

    def heapify_insert_multi(self):#similar to single but the comparision considers the 2nd and 3rd elements
        curr = len(self.heap) - 1
        while self.has_parent(curr) and (   #in case of similar user priorities the counter values to be compared 
            self.heap[self.parent_ind(curr)][1] > self.heap[curr][1] or
            (self.heap[self.parent_ind(curr)][1] == self.heap[curr][1] and self.heap[self.parent_ind(curr)][2] > self.heap[curr][2])): #if counter value is less more preferred
            self.swap(self.parent_ind(curr), curr)
            curr = self.parent_ind(curr)
    def heapify_delete_multi(self):
        curr = 0
        while self.has_left(curr):
            smaller_child_ind = self.left_child_ind(curr)

            if self.has_right(curr) and (
                self.heap[self.right_child_ind(curr)][1] < self.heap[smaller_child_ind][1] or
                (self.heap[self.right_child_ind(curr)][1] == self.heap[smaller_child_ind][1] and self.heap[self.right_child_ind(curr)][2] < self.heap[smaller_child_ind][2])
            ):
                smaller_child_ind = self.right_child_ind(curr)

            if self.heap[curr][1] < self.heap[smaller_child_ind][1] or (
                self.heap[curr][1] == self.heap[smaller_child_ind][1] and self.heap[curr][2] < self.heap[smaller_child_ind][2]
            ):
                break
            else:
                self.swap(curr, smaller_child_ind)
            curr = smaller_child_ind

class PriorityQueue:
    def __init__(self):
       self.waitlist= MinHeap()
    
    def enqueue(self,user_seat_tuple):#adding into priority queue
       self.waitlist.insert_multi(user_seat_tuple)

    def dequeue(self):#popping the highest priority element
       return self.waitlist.pop_heap_multi()
    
    def remove_multi(self,val):#remove a given element
       return self.waitlist.remove_multi(val)
    
    def update_priority(self, user_id, new_priority):#priority value updation keeping the counter and user id same
        found = False
        for i, item in enumerate(self.waitlist.heap):
            if item[0] == user_id:
                found = True
                old_counter = item[2]  
                break

        if found:
            self.waitlist.swap(i, len(self.waitlist.heap) - 1)
            removed_item = self.waitlist.heap.pop()
            if i < len(self.waitlist.heap):
                if self.waitlist.has_parent(i) and self.waitlist.heap[i][1] < self.waitlist.heap[self.waitlist.parent_ind(i)][1] or(self.waitlist.heap[i][1] == self.waitlist.heap[self.waitlist.parent_ind(i)][1] and self.waitlist.heap[i][2] < self.waitlist.heap[self.waitlist.parent_ind(i)][2]):
                    self.waitlist.heapify_insert_multi()
                else:
                    self.waitlist.heapify_delete_multi()

            self.waitlist.heap.append([user_id, new_priority*(-1), old_counter])
            self.waitlist.heapify_insert_multi()
        else:
            return found
            # print(f"user id {user_id} is not found in waitlist")
        return found
    def print_heap(self):
        print("MinHeap contents:")
        for i, (user_id, priority, counter) in enumerate(self.waitlist.heap):
            print(f"Index {i}: User ID = {user_id}, Priority = {-priority}, Insertion Order = {counter}")
    def empty_heap(self):
       self.waitlist.heap.clear()

class AvailableSeats:
   def __init__(self):
      self.available = MinHeap()
      self.max_seat_index = 1 #seat indexes cannot start from 0
   def adding(self, val):#adding addtional seats
      val = self.max_seat_index+val
      while self.max_seat_index<val:
         self.available.insert_single(self.max_seat_index)
         self.max_seat_index += 1
   def get_seat(self, seat_id = None):#pops smallest seaat index for reservations
      if seat_id== None:
        return self.available.pop_heap_single() 
      else:
         seat_id = seat_id*(-1)
         return self.available.remove_single(seat_id)
   def re_adding(self, val):#seat emptied from reservations
       self.available.insert_single(val)
   def empty_heap(self):
       self.available.heap.clear()
