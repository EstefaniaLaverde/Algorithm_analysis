from queue import Queue

def check_exceeds6degrees(friends: dict[int:list[int]]) -> bool:
    """
    This function checks if any user in the social network exceeds 6 degrees of separation.
    
    Parameters:
    friends (dict[int:list[int]]): A dictionary where each key is a user ID and the value is a list of their friends' IDs.
    
    Returns:
    bool: True if any user exceeds 6 degrees of separation, False otherwise.
    """
    # Initialize a flag to track if any user exceeds 6 degrees of separation
    exceeds_6_levels = False
    
    # Get a list of all users in the social network
    users = list(friends.keys())

    # Iterate over each user in the social network
    index = 0
    while index<len(users) and not exceeds_6_levels:
        # Select the current user as the root user
        root_user = users[index]
        print('user',root_user)

        # If the root user is disconnected (has no friends), return True
        if friends[root_user] == []:
            return True

        # Initialize a set to keep track of visited users
        visited = set()
        
        # Initialize a queue for BFS traversal
        queue = Queue()

        # Add the root user to the visited set and the queue (with the level)
        visited.add(root_user)
        queue.put([root_user,0])

        # Perform BFS traversal
        while not queue.empty():
            # Dequeue a user
            selected,lev = queue.get()
            
            # Iterate over the friends of the current user
            for friend in friends[selected]:
                # If the friend has not been visited before, add them to the queue and the visited set (with the level of the father +1)
                if friend not in visited:
                    queue.put([friend, lev+1])
                    visited.add(friend)

        
            # Check if the current level exceeds 6 degrees of separation
            exceeds_6_levels = lev > 6

        # Move on to the next user
        index += 1

    # Return the result
    return exceeds_6_levels 

if __name__=='__main__':
    input_path=sys.argv[1]

    #leer grafo desde un archivo txt con el formato especificado
    with open(sys.argv[1]) as f:
        nodes=list(map(int,f.readline().split()))
        m=int(f.readline())

        edges=[]
        for i in range(m):
            a,b=map(int,f.readline().split())
            edges.append([a,b])

    G=Graph(nodes,edges)

    print(G.check_6degrees2())
