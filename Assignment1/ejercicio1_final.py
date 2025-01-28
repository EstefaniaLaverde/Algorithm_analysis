from queue import Queue
import sys

class FacebookNetwork:
    def __init__(self, users: list[int], friends: list[tuple[int,int]]):
        """
        Initializes a social network with users and their friendships.

        Initializes a social network with a list of users and their friendships. The users are stored in a set for efficient addition or removal of users in future implementations. The friendships are stored in a dictionary where each user maps to a set of their friends, allowing for efficient addition or removal of friendships in future implementations. 

        Parameters:
        users (list[int]): A list of user IDs.
        friends (list[tuple[int,int]]): A list of friendships, where each friendship is a tuple of two user IDs.
        """

        self.users=set(users)
        self.friends={user:set() for user in users}
        for user1,user2 in friends:
            # the friendships are bidirectional, so they are added to both users' sets of friends
            self.friends[user1].add(user2)
            self.friends[user2].add(user1)

    def check_exceeds6degrees(self, max_level: int = 6) -> bool:
        """
        Determines if any user in the social network exceeds the specified maximum degree of separation.

        This method employs a breadth-first search (BFS) to traverse the social network starting from each user. It marks each user as visited and explores their friends up to a specified maximum depth. If any user exceeds the maximum degree of separation or if the network is fully connected (i.e., all users are reachable from each other), the method returns True. Otherwise, it returns False.

        Parameters:
        max_level (int): The maximum degree of separation to check against. Defaults to 6.

        Returns:
        bool: True if any user exceeds the specified maximum degree of separation or if the network is fully connected, False otherwise.
        """
        # Initialize a flag to track if any user exceeds the specified maximum degree of separation or if the network is fully connected
        exceeds_max_levels = False
        
        # Iterate over each user in the social network
        for root_user in self.users:
            print('user', root_user)

            # If the root user is disconnected (has no friends), return True
            if not self.friends[root_user]:
                return True

            # Initialize a set to keep track of visited users
            visited = set()
            
            # Initialize a queue for BFS traversal
            queue = Queue()

            # Add the root user to the visited set and the queue (with the level)
            visited.add(root_user)
            queue.put([root_user, 0])

            # Perform BFS traversal
            while not queue.empty():
                # Dequeue a user
                selected, level = queue.get()
                
                # Iterate over the friends of the current user
                for friend in self.friends[selected]:
                    # If the friend has not been visited before, add them to the queue and the visited set (increasing the level)
                    if friend not in visited:
                        queue.put([friend, level + 1])
                        visited.add(friend)

                # Check if the current level exceeds the specified maximum degree of separation or whether the network is disconnected
                exceeds_max_levels = level > max_level or len(visited) != len(self.users)

                # If the condition is met, break the loop
                if exceeds_max_levels:
                    break

            # If the condition is met, break the loop
            if exceeds_max_levels:
                break

        # Return the result
        return exceeds_max_levels

if __name__=='__main__':

    # Read the graph from a txt file with the specified format
    with open(sys.argv[1]) as f:
        nodes=list(map(int,f.readline().split()))
        m=int(f.readline())

        edges=[]
        for i in range(m):
            a,b=map(int,f.readline().split())
            edges.append((a,b))


    G=FacebookNetwork(nodes,edges)

    k=6
    print(G.check_exceeds6degrees())