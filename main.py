import sys
import re
import os
# import pdb
from min_heap import PriorityQueue,AvailableSeats
from rbtree import RBTree
class GatorTicketMaster:
    def __init__(self,output_file):
        self.red_black_tree = RBTree()  # for reservations
        self.waitlist = PriorityQueue()  # for the waitlist
        self.available_seats = AvailableSeats()  # for managing available seats
        self.output_file = output_file
        self.started = False

    def initialize(self, seat_count): #starting with seatcoun number of seats
        if not self.started:
            self.available_seats.adding(seat_count)
            self.output_file.write(f"{seat_count} Seats are made available for reservation \n")
            self.started= True
        else: #edge case where initialize is called somewhere in between for the second time
            self.available_seats.empty_heap()
            self.waitlist.empty_heap() 
            self.red_black_tree = RBTree()
            self.add_seats(seat_count)
            self.output_file.write(f"{seat_count} Seats are made available for reservation \n")

    def available(self): #available seats and users in waitlist
        available_seat_count = len(self.available_seats.available.heap)
        waitlist_length = len(self.waitlist.waitlist.heap)
        self.output_file.write(f"Total Seats Available : {available_seat_count}, Waitlist : {waitlist_length} \n")

    def reserve(self, user_id, user_priority):
        seat_id = self.available_seats.get_seat() #checks for seats
        if self.red_black_tree.search_tree_helper(user_id) != None: #checks if user id already in rb tree
            self.output_file.write(f"User {user_id} is already has a reservation with {self.red_black_tree.search_tree_helper(user_id).seat_id} \n")
            return
        if seat_id is not None: #if seat exists check with waitlist
            if len(self.waitlist.waitlist.heap) == 0: #if noone in wailist push into redblack tree directly
                self.red_black_tree.insert_node(user_id, seat_id)
                self.output_file.write(f"User {user_id} reserved seat {seat_id} \n")
            else:#if someone in reservations push into waitlist and pop waitlist
                temp = [user_id, user_priority]
                self.waitlist.enqueue(temp)
                first_priority = self.waitlist.dequeue()
                self.red_black_tree.insert_node(first_priority[0], first_priority[1])#insert the popped entry in to red blac tree
                self.output_file.write(f"User {user_id} is added to the waiting list \n")
                self.output_file.write(f"User {first_priority[0]} reserved seat {first_priority[1]} \n")
        else:
            self.waitlist.enqueue([user_id,user_priority])#no seats then add to waitlist
            self.output_file.write(f"User {user_id} is added to the waiting list \n")
            
            
    def printing(self):#helper func to debug for checking elements in waitlist
        self.waitlist.print_heap()   

    def cancel(self, seat_id, user_id):  #deleting with respective to user and seat if in reservation if not in reservation but in waitlist delete user
        if self.red_black_tree.search_tree_helper(user_id) != None:#checks in reservations
            if self.red_black_tree.delete_node(user_id,seat_id):#matches user and seat 
                self.available_seats.re_adding(seat_id)
                self.output_file.write(f"User {user_id} cancelled their reservation \n")
                if len(self.waitlist.waitlist.heap) >0:
                    seat_id = self.available_seats.get_seat()
                    first_priority = self.waitlist.dequeue()
                    self.red_black_tree.insert_node(first_priority[0], seat_id)
                    self.output_file.write(f"User {first_priority[0]} reserved seat {seat_id} \n")
            else:
                 self.output_file.write(f"User {user_id} has no reservation for seat {seat_id} to cancel \n")
        else:
            # search in waitlist
            if self.waitlist.remove_multi(user_id):
                self.output_file.write(f"user {user_id} not present in reservation byt present in waitlist, hence removed from waitlist \n")
                self.available_seats.re_adding(seat_id)
    def exit_waitlist(self, user_id):#deleting from waitlist
        if self.waitlist.remove_multi(user_id):#check for user in waitlist
            self.output_file.write(f" user {user_id} deleted from waitlist \n")
            return 
        self.output_file.write(f"user {user_id} not found in waitlist \n")
        return 

    def update_priority(self, user_id, user_priority):#priority in waitlist for the given user to be updated
        if self.waitlist.update_priority(user_id,user_priority):#checks for successfull updation (returns true)
            self.output_file.write(f"User {user_id} priority has been updated to {user_priority} \n")
        else:
            self.output_file.write(f"User {user_id} priority is not updated  \n")

    def add_seats(self, count):#adding seats to existing 
        self.available_seats.adding(count)
        self.output_file.write(f"Additional {count} Seats are made available for reservation \n")
        loop_count = min(len(self.available_seats.available.heap),len(self.waitlist.waitlist.heap)) #checks for min of seats and len of waitlist to determine the length of for loop to run
        # print(f"min value is {loop_count} \n")
        for i in range (0,loop_count):#mapping the users in waitlist with the released seats
            seat_id = self.available_seats.get_seat()
            user_id = self.waitlist.dequeue()[0]
            self.red_black_tree.insert_node(user_id,seat_id)
            self.output_file.write(f"User {user_id} reserved seat {seat_id} \n")
    def print_reservations(self):
        self.output_file.write(self.red_black_tree.inorder_traversal())#writes the output of inorder traversal

    def release_seats(self, user_id1, user_id2):#deleting user ids in the range 
        for user_id in range(user_id1,user_id2+1):
            if self.red_black_tree.search_tree_helper(user_id)!= None:#maps elements in redblack tree with user_id to delete
                seat_id = self.red_black_tree.search_tree_helper(user_id).seat_id# seat ids to be released in to available seats
                self.red_black_tree.delete_node(user_id,seat_id=None, cancel=False)
                self.available_seats.re_adding(seat_id)
            else:  #if not in redblack tree checks for the users in waitlist and deletes
                self.waitlist.remove_multi(user_id)          
        loop_count = min(len(self.available_seats.available.heap),len(self.waitlist.waitlist.heap))
        self.output_file.write(f"Reservations of the Users in the range [{user_id1}, {user_id2}] are released \n") #the released seats to be matpped with the users in waitlist.
        for i in range (0,loop_count):
            seat_id = self.available_seats.get_seat()
            user_id = self.waitlist.dequeue()[0]
            self.red_black_tree.insert_node(user_id,seat_id)
            self.output_file.write(f"User {user_id} reserved seat {seat_id} \n") 
        
    def quit(self):
        self.output_file.write("Program Terminated!! \n")
        sys.exit()#terminate

    def process_command(self, command):
        match = re.match(r"(\w+)\((.*)\)", command)#mapping for pattern "word" followed by "(vals)"
        if not match:
            print(f"Invalid command format: {command}")
            return

        action = match.group(1)  #command word
        params = match.group(2)  #parameteres within paranthesis
        if action == "Initialize":
            seat_count = int(params)#single param ->no parsing required
            self.initialize(seat_count)

        elif action == "Available":
            self.available()

        elif action == "Reserve":
            user_id, user_priority = map(int, params.split(","))#->mapping the multi parameters in command similarly below
            self.reserve(user_id, user_priority) #function from gatorticket master

        elif action == "Cancel":
            seat_id, user_id = map(int, params.split(","))
            self.cancel(seat_id, user_id)

        elif action == "UpdatePriority":
            user_id, new_priority = map(int, params.split(","))
            self.update_priority(user_id, new_priority)

        elif action == "AddSeats":
            count = int(params)
            self.add_seats(count)
        elif action == "ExitWaitlist":
            count = int(params)
            self.exit_waitlist(count)

        elif action == "PrintReservations":
            self.print_reservations()

        elif action == "ReleaseSeats":
            user_id1, user_id2 = map(int, params.split(","))
            self.release_seats(user_id1, user_id2)

        elif action == "Quit":
            self.quit()

        else:
            print(f"Unknown command: {action}")

def main():
    if len(sys.argv)<2: #checks for input file name provided or not.
        print("please provide input file")
        return 
    else:
        input_file = sys.argv[1]
    output_file = f"{os.path.splitext(input_file)[0]}_output.txt"#naming the ouput file based on the input file name
    if not os.path.exists(input_file):#checks if present or not
        with open(input_file, 'w'):
            pass
        print("creating input file to useas it does not exist currently")
        return
    if not os.path.exists(output_file):
        with open(output_file, 'w') as f:#creates if not present
            pass
    with open(output_file, 'w') as output:
        ticket_system = GatorTicketMaster(output)
        with open(input_file, 'r') as file:
            for line in file:
                command = line.strip()
                ticket_system.process_command(command)
if __name__ == "__main__":
    main()
