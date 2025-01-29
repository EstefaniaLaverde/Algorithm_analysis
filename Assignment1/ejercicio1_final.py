from queue import Queue
import sys

class FacebookNetwork:
    def __init__(self, users: list[int], friends: list[tuple[int,int]]):
        """
        Initializes a social network with users and their friendships.

        Initializes a social network with a list of users and their friendships. The users are stored in a set for efficient addition or removal of users in future implementations. The friendships are stored in a dictionary where each user maps to a set of their friends, allowing for efficient addition or removal of friendships in future implementations. 

        Parameters:
        users (list[int]): A list of users.
        friends (list[tuple[int,int]]): A list of friendships, where each friendship is a tuple of two users.
        """

        self.users=set(users)
        self.friends={user:set() for user in users}
        for user1,user2 in friends:
            # the friendships are bidirectional, so they are added to both users' sets of friends
            self.friends[user1].add(user2)
            self.friends[user2].add(user1)

    def check6degrees(self, max_level: int = 6) -> bool:
        """
        Verifies if the social network adheres to the six degrees of separation theory.

        This method performs a breadth-first search (BFS) traversal of the social network, starting from each user. It checks if all users can be reached within a specified maximum degree of separation. If any user exceeds this limit or if the network is disconnected, the method returns False. Otherwise, it returns True.

        Parameters:
        max_level (int): The maximum degree of separation to check against. Defaults to 6.

        Returns:
        bool: True if the social network adheres to the six degrees of separation theory and is connected, False otherwise.
        """
        # Initialize a flag to track if any user exceeds the specified maximum degree of separation 
        exceeds_max_levels = False

        # Initialize a flag to track if the network is fully connected
        is_disconnected = False
        
        # Iterate over each user in the social network
        for root_user in self.users:

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

                # Check if the current level exceeds the specified maximum degree of separation
                exceeds_max_levels = level > max_level 

            # Check whether at the end of BFS all users have been visited
            is_disconnected = visited != self.users

            # If the condition is met, break the loop and return False
            if exceeds_max_levels or is_disconnected:
                return False

        # Return True if the network is connected and no users exceed the maximum level
        return True
    
    def draw_graph(self):
        """
        Visualizes the social network graph using matplotlib.
        """
        import matplotlib.pyplot as plt
        import networkx as nx

        # Create a new undirected graph
        G = nx.Graph()

        # Add edges to the graph
        for user, friends in self.friends.items():
            for friend in friends:
                G.add_edge(user, friend)

        # Draw the graph
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, arrows=False)
        plt.show()

if __name__ == '__main__':
    # Read the graph from a txt file with the specified format
    with open(sys.argv[1]) as f:
        content = f.read()  # Read the entire file content
        sections = [section.strip() for section in content.split('\n\n') if section.strip()]  # Split by double newlines and strip whitespace

    # Save the results
    results = []

    # Process each section
    for section in sections:
        lines = section.splitlines()  
        nodes = list(map(int, lines[0].split()))  # First line for nodes
        m = int(lines[1])  # Second line for number of edges
        edges = []
        for i in range(2, 2 + m):  # Read the edges
            a, b = map(int, lines[i].split())
            edges.append((a, b))

        # Create the FacebookNetwork instance
        G = FacebookNetwork(nodes, edges)

        # Check for 6 degrees of separation
        result = G.check6degrees()
        results.append(result)
        print(result)

        # Save results in a .out file
        with open(sys.argv[2], 'w') as f:
            for result in results:
                f.write(str(result) + '\n')