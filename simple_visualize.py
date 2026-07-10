# simple_visualize.py
# Simple graph visualization using your existing friend_graph.py

import networkx as nx
import matplotlib.pyplot as plt
from user_manager import UserManager
from friend_graph import FriendGraph

def create_and_visualize():
    """Create a social network and visualize it"""
    
    # ========== CREATE YOUR DATA STRUCTURES ==========
    user_manager = UserManager()
    friend_graph = FriendGraph(user_manager)
    
    # ========== ADD USERS ==========
    print("Adding users...")
    alice = user_manager.add_user("Alice")
    bob = user_manager.add_user("Bob")
    charlie = user_manager.add_user("Charlie")
    diana = user_manager.add_user("Diana")
    eve = user_manager.add_user("Eve")
    frank = user_manager.add_user("Frank")
    grace = user_manager.add_user("Grace")
    henry = user_manager.add_user("Henry")
    ivy = user_manager.add_user("Ivy")
    jack = user_manager.add_user("Jack")
    
    # ========== ADD FRIENDSHIPS ==========
    print("Adding friendships...")
    friend_graph.add_friend(alice, bob)
    friend_graph.add_friend(alice, charlie)
    friend_graph.add_friend(alice, diana)
    friend_graph.add_friend(bob, charlie)
    friend_graph.add_friend(bob, eve)
    friend_graph.add_friend(charlie, frank)
    friend_graph.add_friend(diana, eve)
    friend_graph.add_friend(diana, grace)
    friend_graph.add_friend(eve, henry)
    friend_graph.add_friend(frank, grace)
    friend_graph.add_friend(grace, henry)
    friend_graph.add_friend(henry, ivy)
    friend_graph.add_friend(ivy, jack)
    friend_graph.add_friend(jack, alice)
    
    # ========== BUILD NETWORKX GRAPH ==========
    print("Building visualization...")
    G = nx.Graph()
    
    # Add all users as nodes
    all_users = user_manager.get_all_users()
    for user in all_users:
        G.add_node(user['id'], label=user['name'])
    
    # Add all friendships as edges
    friendships = friend_graph.get_all_friendships()
    for u1, u2 in friendships:
        G.add_edge(u1, u2)
    
    # Get node labels
    labels = {user['id']: user['name'] for user in all_users}
    
    # ========== VISUALIZE ==========
    print("Displaying graph...")
    
    # Create layout
    pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)
    
    # Calculate node sizes based on number of friends
    degrees = dict(G.degree())
    node_sizes = [300 + 200 * degrees[node] for node in G.nodes()]
    node_colors = [degrees[node] for node in G.nodes()]
    
    # Create figure
    plt.figure(figsize=(14, 10))
    
    # Draw nodes with colors based on degree
    nx.draw_networkx_nodes(G, pos, 
                          node_color=node_colors,
                          cmap=plt.cm.viridis,
                          node_size=node_sizes,
                          alpha=0.9)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color='gray', width=1.5)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight='bold')
    
    # Add title
    plt.title(f"Social Network Graph\nUsers: {len(G.nodes())}, Friendships: {len(G.edges())}", 
              fontsize=16, fontweight='bold')
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, 
                               norm=plt.Normalize(vmin=min(node_colors), 
                                                  vmax=max(node_colors)))
    sm.set_array([])
    plt.colorbar(sm, label='Number of Friends (Degree)')
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
    # ========== PRINT STATISTICS ==========
    print("\n" + "=" * 50)
    print("📊 SOCIAL NETWORK STATISTICS")
    print("=" * 50)
    print(f"Total Users: {len(G.nodes())}")
    print(f"Total Friendships: {len(G.edges())}")
    print(f"Average Friends: {sum(degrees.values()) / len(degrees):.2f}")
    print(f"Most Popular: {max(degrees, key=degrees.get)} with {max(degrees.values())} friends")
    print("=" * 50)
    
    return G

def visualize_mutual_friends():
    """Visualize mutual friends between two specific users"""
    
    user_manager = UserManager()
    friend_graph = FriendGraph(user_manager)
    
    # Add users
    alice = user_manager.add_user("Alice")
    bob = user_manager.add_user("Bob")
    charlie = user_manager.add_user("Charlie")
    diana = user_manager.add_user("Diana")
    eve = user_manager.add_user("Eve")
    
    # Add friendships - Alice and Bob share Charlie and Diana as mutual friends
    friend_graph.add_friend(alice, bob)
    friend_graph.add_friend(alice, charlie)
    friend_graph.add_friend(alice, diana)
    friend_graph.add_friend(alice, eve)
    friend_graph.add_friend(bob, charlie)
    friend_graph.add_friend(bob, diana)
    friend_graph.add_friend(bob, eve)
    
    # Build graph
    G = nx.Graph()
    all_users = user_manager.get_all_users()
    for user in all_users:
        G.add_node(user['id'], label=user['name'])
    
    friendships = friend_graph.get_all_friendships()
    for u1, u2 in friendships:
        G.add_edge(u1, u2)
    
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    labels = {user['id']: user['name'] for user in all_users}
    
    # Find mutual friends of Alice and Bob
    alice_friends = friend_graph.get_friends(alice)
    bob_friends = friend_graph.get_friends(bob)
    mutual = alice_friends.intersection(bob_friends)
    mutual_names = [user_manager.get_user(mid)['name'] for mid in mutual]
    
    print(f"\nMutual friends of Alice and Bob: {mutual_names}")
    
    # Color nodes
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if node == alice:
            node_colors.append('red')
            node_sizes.append(800)
        elif node == bob:
            node_colors.append('blue')
            node_sizes.append(800)
        elif node in mutual:
            node_colors.append('gold')
            node_sizes.append(600)
        else:
            node_colors.append('lightgray')
            node_sizes.append(300)
    
    # Draw
    plt.figure(figsize=(12, 10))
    
    nx.draw_networkx_edges(G, pos, alpha=0.2, edge_color='gray')
    
    # Highlight edges to mutual friends
    for mid in mutual:
        nx.draw_networkx_edges(G, pos, [(alice, mid)], 
                               edge_color='red', width=2, style='dashed')
        nx.draw_networkx_edges(G, pos, [(bob, mid)], 
                               edge_color='blue', width=2, style='dashed')
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes)
    nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight='bold')
    
    title = f"Mutual Friends: Alice and Bob\nMutual friends: {', '.join(mutual_names)}"
    plt.title(title, fontsize=14, fontweight='bold')
    
    # Legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
                   markersize=15, label='Alice'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', 
                   markersize=15, label='Bob'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gold', 
                   markersize=15, label='Mutual Friends'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgray', 
                   markersize=15, label='Other Users'),
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def visualize_recommendations():
    """Visualize friend recommendations"""
    
    from recommendation_heap import RecommendationEngine
    
    user_manager = UserManager()
    friend_graph = FriendGraph(user_manager)
    rec_engine = RecommendationEngine(friend_graph)
    
    # Add users
    alice = user_manager.add_user("Alice")
    bob = user_manager.add_user("Bob")
    charlie = user_manager.add_user("Charlie")
    diana = user_manager.add_user("Diana")
    eve = user_manager.add_user("Eve")
    frank = user_manager.add_user("Frank")
    grace = user_manager.add_user("Grace")
    
    # Add friendships - Alice is friends with Bob, Charlie, Diana
    # Bob is friends with Eve, Frank
    # Charlie is friends with Eve, Grace
    # Diana is friends with Frank, Grace
    
    friend_graph.add_friend(alice, bob)
    friend_graph.add_friend(alice, charlie)
    friend_graph.add_friend(alice, diana)
    friend_graph.add_friend(bob, eve)
    friend_graph.add_friend(bob, frank)
    friend_graph.add_friend(charlie, eve)
    friend_graph.add_friend(charlie, grace)
    friend_graph.add_friend(diana, frank)
    friend_graph.add_friend(diana, grace)
    
    # Get recommendations for Alice
    recs = rec_engine.recommend_friends(alice, top_k=3)
    rec_ids = [rec[0] for rec in recs]
    rec_scores = {rec[0]: rec[1] for rec in recs}
    
    print(f"\nTop recommendations for Alice:")
    for friend_id, score in recs:
        friend = user_manager.get_user(friend_id)
        print(f"  - {friend['name']} ({score} mutual friends)")
    
    # Build graph
    G = nx.Graph()
    all_users = user_manager.get_all_users()
    for user in all_users:
        G.add_node(user['id'], label=user['name'])
    
    friendships = friend_graph.get_all_friendships()
    for u1, u2 in friendships:
        G.add_edge(u1, u2)
    
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    labels = {user['id']: user['name'] for user in all_users}
    
    # Color nodes
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if node == alice:
            node_colors.append('red')
            node_sizes.append(1000)
        elif node in rec_ids:
            node_colors.append('orange')
            node_sizes.append(500 + 50 * rec_scores[node])
        elif node in friend_graph.get_friends(alice):
            node_colors.append('lightblue')
            node_sizes.append(350)
        else:
            node_colors.append('lightgray')
            node_sizes.append(250)
    
    # Draw
    plt.figure(figsize=(14, 10))
    
    nx.draw_networkx_edges(G, pos, alpha=0.2, edge_color='gray')
    
    # Highlight edges to recommendations
    for rec_id in rec_ids:
        nx.draw_networkx_edges(G, pos, [(alice, rec_id)], 
                               edge_color='orange', width=3, style='dashed')
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_sizes=node_sizes)
    nx.draw_networkx_labels(G, pos, labels, font_size=11, font_weight='bold')
    
    rec_names = [user_manager.get_user(mid)['name'] for mid in rec_ids]
    rec_names_str = ', '.join(rec_names) if rec_names else 'None'
    plt.title(f"Friend Recommendations for Alice\nRecommended: {rec_names_str}", 
              fontsize=14, fontweight='bold')
    
    # Legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
                   markersize=15, label='Alice'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', 
                   markersize=15, label='Recommended Friends'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', 
                   markersize=15, label='Current Friends'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgray', 
                   markersize=15, label='Other Users'),
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def main():
    """Main function"""
    print("=" * 60)
    print("📊 SOCIAL NETWORK VISUALIZATION")
    print("   Using your existing friend_graph.py")
    print("=" * 60)
    
    while True:
        print("\nChoose visualization type:")
        print("1. Complete Social Network Graph")
        print("2. Mutual Friends (Alice & Bob)")
        print("3. Friend Recommendations (Alice)")
        print("4. All Visualizations")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            create_and_visualize()
        elif choice == '2':
            visualize_mutual_friends()
        elif choice == '3':
            visualize_recommendations()
        elif choice == '4':
            create_and_visualize()
            visualize_mutual_friends()
            visualize_recommendations()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
