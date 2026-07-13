# visualize_all.py
# Complete visualization for ALL data structures and algorithms
# Includes: Graph, BFS, Heap, Sorting, Benchmark Results

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
import numpy as np
from user_manager import UserManager
from friend_graph import FriendGraph
from bfs_queue import BFSFriendFinder
from recommendation_heap import RecommendationEngine
from sorting_searching import SortingSearchingUtils


# ============================================================
# 1. GRAPH VISUALIZATION (Already have this)
# ============================================================

def visualize_graph(sn, title="Social Network Graph"):
    """Visualize the social network graph"""
    G = nx.Graph()
    all_users = sn.get_all_users()
    for user in all_users:
        G.add_node(user['id'], label=user['name'])
    
    friendships = sn.get_all_friendships()
    for u1, u2 in friendships:
        G.add_edge(u1, u2)
    
    pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)
    labels = {user['id']: user['name'] for user in all_users}
    degrees = dict(G.degree())
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    node_sizes = [300 + 200 * degrees[node] for node in G.nodes()]
    node_colors = [degrees[node] for node in G.nodes()]
    
    nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                                   cmap=plt.cm.viridis, node_size=node_sizes,
                                   alpha=0.9, ax=ax)
    nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color='gray', width=1.5, ax=ax)
    nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight='bold', ax=ax)
    
    if nodes is not None:
        sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis,
                                   norm=plt.Normalize(vmin=min(node_colors),
                                                      vmax=max(node_colors)))
        sm.set_array([])
        plt.colorbar(sm, ax=ax, label='Number of Friends (Degree)')
    
    ax.set_title(f"{title}\nUsers: {len(G.nodes())}, Friendships: {len(G.edges())}",
                 fontsize=16, fontweight='bold')
    ax.axis('off')
    plt.tight_layout()
    plt.show()


# ============================================================
# 2. BFS VISUALIZATION - Mutual Friends Search
# ============================================================

def visualize_bfs_mutual_friends(sn, user1_name, user2_name):
    """
    Visualize BFS traversal for finding mutual friends
    Shows the BFS queue and visited nodes
    """
    from collections import deque
    
    u1_id, u1_data = sn.get_user_by_name(user1_name)
    u2_id, u2_data = sn.get_user_by_name(user2_name)
    
    if not u1_id or not u2_id:
        print(f"User not found: {user1_name} or {user2_name}")
        return
    
    print(f"\n🔍 BFS TRAVERSAL - Finding mutual friends of {user1_name} and {user2_name}")
    print("=" * 60)
    
    # Get all friends
    friends1 = sn.get_friends(u1_id)
    friends2 = sn.get_friends(u2_id)
    
    # BFS from user1
    print(f"\n📌 BFS Level 0: Start at {user1_name}")
    print(f"   Friends of {user1_name}: {[sn.get_user(fid)['name'] for fid in friends1]}")
    
    # Level 1 - Friends of friends
    level_1 = []
    for friend in friends1:
        for friend_of_friend in sn.get_friends(friend):
            if friend_of_friend != u1_id:
                level_1.append(friend_of_friend)
    
    print(f"\n📌 BFS Level 1: Friends of friends")
    level_1_names = [sn.get_user(fid)['name'] for fid in level_1]
    print(f"   Candidates: {level_1_names}")
    
    # Mutual friends (intersection)
    mutual = friends1.intersection(friends2)
    mutual_names = [sn.get_user(mid)['name'] for mid in mutual]
    
    print(f"\n✅ MUTUAL FRIENDS FOUND: {mutual_names}")
    
    # Create visualization
    G = nx.Graph()
    all_users = sn.get_all_users()
    for user in all_users:
        G.add_node(user['id'], label=user['name'])
    
    friendships = sn.get_all_friendships()
    for u1, u2 in friendships:
        G.add_edge(u1, u2)
    
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    labels = {user['id']: user['name'] for user in all_users}
    
    # Color nodes by BFS level
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if node == u1_id:
            node_colors.append('red')
            node_sizes.append(1000)
        elif node == u2_id:
            node_colors.append('blue')
            node_sizes.append(1000)
        elif node in mutual:
            node_colors.append('gold')
            node_sizes.append(700)
        elif node in friends1:
            node_colors.append('lightgreen')
            node_sizes.append(400)
        elif node in level_1:
            node_colors.append('lightyellow')
            node_sizes.append(300)
        else:
            node_colors.append('lightgray')
            node_sizes.append(200)
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    nx.draw_networkx_edges(G, pos, alpha=0.2, edge_color='gray', ax=ax)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, ax=ax)
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold', ax=ax)
    
    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
               markersize=15, label=f'{user1_name} (Start)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', 
               markersize=15, label=f'{user2_name} (Target)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gold', 
               markersize=15, label='Mutual Friends Found!'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgreen', 
               markersize=15, label='Level 1: Direct Friends'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='lightyellow', 
               markersize=15, label='Level 2: Friends of Friends'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgray', 
               markersize=15, label='Unvisited'),
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    ax.set_title(f"BFS - Finding Mutual Friends: {user1_name} and {user2_name}\n"
                 f"Mutual Friends: {', '.join(mutual_names) if mutual_names else 'None found'}",
                 fontsize=14, fontweight='bold')
    ax.axis('off')
    plt.tight_layout()
    plt.show()
    
    return mutual


# ============================================================
# 3. HEAP VISUALIZATION - Recommendation Algorithm
# ============================================================

def visualize_heap_recommendations(sn, user_name, top_k=5):
    """
    Visualize how the heap works for top-K recommendations
    Shows the heap structure and scores
    """
    u_id, u_data = sn.get_user_by_name(user_name)
    if not u_id:
        print(f"User not found: {user_name}")
        return
    
    print(f"\n🔄 HEAP ALGORITHM - Finding top {top_k} recommendations for {user_name}")
    print("=" * 60)
    
    # Get recommendations (this uses the heap internally)
    recs = sn.recommend_friends(u_id, top_k)
    
    print(f"\n📊 Top {len(recs)} Recommendations (Heap Top-K):")
    for i, (friend_id, score) in enumerate(recs, 1):
        friend = sn.get_user(friend_id)
        print(f"   {i}. {friend['name']} - {score} mutual friends")
    
    # Visualize the heap structure as a tree
    if recs:
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create a simple tree visualization of the heap
        scores = [score for _, score in recs]
        names = [sn.get_user(fid)['name'] for fid, _ in recs]
        
        # Draw as horizontal bar chart (showing heap scores)
        y_pos = np.arange(len(scores))
        bars = ax.barh(y_pos, scores, color=plt.cm.viridis(np.linspace(0.3, 0.9, len(scores))))
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels([f"{name} ({score})" for name, score in zip(names, scores)])
        ax.invert_yaxis()  # Highest score at top
        ax.set_xlabel('Mutual Friend Score', fontsize=12)
        ax.set_title(f'Heap - Top {len(recs)} Recommendations for {user_name}\n'
                     f'Each bar shows mutual friends count', fontsize=14, fontweight='bold')
        
        # Add value labels on bars
        for bar, score in zip(bars, scores):
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                    f'{score}', va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    return recs


# ============================================================
# 4. SORTING VISUALIZATION - Friends List Sort
# ============================================================

def visualize_sorting_algorithm(sn, user_name):
    """
    Visualize how friends are sorted alphabetically
    Shows before/after sorting
    """
    u_id, u_data = sn.get_user_by_name(user_name)
    if not u_id:
        print(f"User not found: {user_name}")
        return
    
    friends = sn.get_friends(u_id)
    if not friends:
        print(f"{user_name} has no friends to sort")
        return
    
    print(f"\n📊 TIMSORT - Sorting friends of {user_name} alphabetically")
    print("=" * 60)
    
    # Get unsorted and sorted lists
    unsorted = [sn.get_user(fid)['name'] for fid in friends]
    sorted_friends = sn.get_sorted_friends(u_id)
    sorted_names = [f['name'] for f in sorted_friends]
    
    print(f"\n📌 UNSORTED: {unsorted}")
    print(f"✅ SORTED:   {sorted_names}")
    print(f"\n   Algorithm: Timsort (O(n log n))")
    
    # Visualize before/after sorting
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Before sorting
    y_pos1 = np.arange(len(unsorted))
    ax1.barh(y_pos1, [1] * len(unsorted), color='lightcoral')
    ax1.set_yticks(y_pos1)
    ax1.set_yticklabels(unsorted)
    ax1.set_title(f'BEFORE SORTING (Unsorted)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Position in List')
    ax1.invert_yaxis()
    
    # After sorting
    y_pos2 = np.arange(len(sorted_names))
    ax2.barh(y_pos2, [1] * len(sorted_names), color='lightgreen')
    ax2.set_yticks(y_pos2)
    ax2.set_yticklabels(sorted_names)
    ax2.set_title(f'AFTER SORTING (Alphabetical)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Position in List')
    ax2.invert_yaxis()
    
    plt.suptitle(f'Timsort O(n log n) - Sorting friends of {user_name}',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


# ============================================================
# 5. BINARY SEARCH VISUALIZATION
# ============================================================

def visualize_binary_search(sn, user_name, search_name):
    """
    Visualize binary search steps
    """
    u_id, u_data = sn.get_user_by_name(user_name)
    if not u_id:
        print(f"User not found: {user_name}")
        return
    
    sorted_friends = sn.get_sorted_friends(u_id)
    names = [f['name'] for f in sorted_friends]
    
    if not names:
        print(f"{user_name} has no friends to search")
        return
    
    print(f"\n🔍 BINARY SEARCH - Looking for '{search_name}' in friends of {user_name}")
    print("=" * 60)
    print(f"   Sorted friend list: {names}")
    
    # Perform binary search manually to show steps
    left, right = 0, len(names) - 1
    steps = []
    found = False
    
    while left <= right:
        mid = (left + right) // 2
        steps.append({
            'left': left,
            'right': right,
            'mid': mid,
            'value': names[mid],
            'searching_for': search_name
        })
        
        if names[mid] == search_name:
            found = True
            break
        elif names[mid] < search_name:
            left = mid + 1
        else:
            right = mid - 1
    
    print(f"\n📌 Search Steps:")
    for i, step in enumerate(steps, 1):
        print(f"   Step {i}: Check position {step['mid']} → '{step['value']}'")
        if step['value'] == search_name:
            print(f"   ✅ FOUND!")
        elif step['value'] < search_name:
            print(f"   → Search RIGHT half")
        else:
            print(f"   → Search LEFT half")
    
    if found:
        print(f"\n✅ FOUND '{search_name}' in {len(steps)} steps!")
    else:
        print(f"\n❌ '{search_name}' not found. Searched {len(steps)} positions.")
    
    # Visualize the search process
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create array visualization
    colors = ['lightgray'] * len(names)
    for step in steps:
        colors[step['mid']] = 'gold'
    
    # Highlight found element
    if found:
        for i, name in enumerate(names):
            if name == search_name:
                colors[i] = 'lightgreen'
    
    bars = ax.bar(range(len(names)), [1] * len(names), color=colors, edgecolor='black')
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha='right')
    ax.set_title(f'Binary Search - Looking for "{search_name}" in friends of {user_name}\n'
                 f'Gold = Checked positions, Green = Found!',
                 fontsize=14, fontweight='bold')
    ax.set_ylabel('Search Position')
    ax.set_xlabel('Friend Names (Sorted Alphabetically)')
    ax.set_ylim(0, 1.5)
    ax.set_yticks([])
    
    # Add step numbers on bars
    for i, name in enumerate(names):
        for step in steps:
            if step['mid'] == i:
                ax.text(i, 0.75, f"Step {steps.index(step)+1}", ha='center', 
                       fontweight='bold', color='darkblue')
    
    # Add result text
    result_text = f"✅ FOUND in {len(steps)} steps!" if found else f"❌ NOT FOUND after {len(steps)} steps"
    ax.text(0.5, 1.4, result_text, ha='center', fontsize=14, fontweight='bold',
           color='green' if found else 'red',
           transform=ax.transAxes)
    
    plt.tight_layout()
    plt.show()


# ============================================================
# 6. BENCHMARK RESULTS VISUALIZATION
# ============================================================

def visualize_benchmark_results():
    """
    Visualize benchmark results as charts
    """
    print("\n📊 BENCHMARK RESULTS VISUALIZATION")
    print("=" * 60)
    
    # Sample benchmark data (you can replace with your actual results)
    operations = ['Add User', 'Add Friend', 'Mutual Friends', 'Recommendations', 'Sort Friends', 'Binary Search']
    
    level_1 = [1.2, 0.9, 234, 156, 45, 1.5]      # 1,000 users (microseconds)
    level_2 = [1.2, 0.9, 456, 345, 89, 1.6]      # 10,000 users
    level_3 = [1.2, 0.9, 1234, 987, 156, 1.7]    # 50,000 users
    
    # Create grouped bar chart
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Chart 1: Per-Transaction Comparison
    x = np.arange(len(operations))
    width = 0.25
    
    ax1.bar(x - width, level_1, width, label='Level 1 (1,000)', color='lightgreen')
    ax1.bar(x, level_2, width, label='Level 2 (10,000)', color='gold')
    ax1.bar(x + width, level_3, width, label='Level 3 (50,000)', color='lightcoral')
    
    ax1.set_xlabel('Operation', fontsize=12)
    ax1.set_ylabel('Time (microseconds)', fontsize=12)
    ax1.set_title('Per-Transaction Performance at Different Scales', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(operations, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Chart 2: Scalability - O(1) vs O(n) operations
    # Show how different algorithms scale
    scales = ['1,000', '10,000', '50,000']
    
    # O(1) operations (constant)
    o1_data = [1.2, 1.2, 1.2]  # Add User
    
    # O(log n) operations (logarithmic)
    log_data = [1.5, 1.6, 1.7]  # Binary Search
    
    # O(n log n) operations
    nlogn_data = [45, 89, 156]  # Sort Friends
    
    # O(V+E) operations (linear)
    linear_data = [234, 456, 1234]  # Mutual Friends
    
    ax2.plot(scales, o1_data, 'o-', label='O(1) - Add User', linewidth=2, markersize=8)
    ax2.plot(scales, log_data, 's-', label='O(log n) - Binary Search', linewidth=2, markersize=8)
    ax2.plot(scales, nlogn_data, '^-', label='O(n log n) - Sort Friends', linewidth=2, markersize=8)
    ax2.plot(scales, linear_data, 'd-', label='O(V+E) - Mutual Friends', linewidth=2, markersize=8)
    
    ax2.set_xlabel('Number of Users', fontsize=12)
    ax2.set_ylabel('Time (microseconds)', fontsize=12)
    ax2.set_title('Scalability - How Operations Grow with Users', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Print summary
    print("\n📊 SCALABILITY SUMMARY:")
    print("-" * 50)
    print("✅ O(1) operations: Constant time (Add User, Add Friend)")
    print("✅ O(log n): Slight increase (Binary Search)")
    print("✅ O(n log n): Moderate increase (Sort Friends)")
    print("⚠️  O(V+E): Linear increase (Mutual Friends - biggest concern!)")
    print("   → Need caching and optimization for 1M+ users")


# ============================================================
# 7. DATA STRUCTURE VISUALIZATION
# ============================================================

def visualize_data_structures():
    """
    Visualize the 5 mandatory data structures
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # 1. Hash Table (User Manager)
    ax1 = axes[0, 0]
    ax1.set_title('1. Hash Table - User Manager', fontsize=12, fontweight='bold')
    
    # Draw hash table
    table_data = [
        ['ID:1', 'Alice'],
        ['ID:2', 'Bob'],
        ['ID:3', 'Charlie'],
        ['...', '...'],
        ['ID:N', 'User N']
    ]
    
    table = ax1.table(cellText=table_data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    ax1.axis('off')
    ax1.text(0.5, -0.1, 'O(1) Lookup', ha='center', transform=ax1.transAxes, fontweight='bold')
    
    # 2. Graph (Friend Graph)
    ax2 = axes[0, 1]
    ax2.set_title('2. Graph - Friend Connections', fontsize=12, fontweight='bold')
    
    G = nx.Graph()
    G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'C'), ('C', 'D'), ('D', 'E')])
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, ax=ax2, with_labels=True, node_color='lightblue',
            node_size=500, font_weight='bold', font_size=12)
    ax2.set_title('Adjacency List: O(1) edges')
    
    # 3. Stack (Undo)
    ax3 = axes[0, 2]
    ax3.set_title('3. Stack - Undo History', fontsize=12, fontweight='bold')
    
    stack_items = ['Action 3 (top)', 'Action 2', 'Action 1 (bottom)']
    for i, item in enumerate(stack_items):
        rect = Rectangle((0.3, 0.7 - i*0.25), 0.4, 0.2, facecolor='lightcoral', edgecolor='black')
        ax3.add_patch(rect)
        ax3.text(0.5, 0.8 - i*0.25, item, ha='center', va='center', fontsize=10)
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.axis('off')
    ax3.text(0.5, -0.1, 'LIFO: O(1) Push/Pop', ha='center', transform=ax3.transAxes, fontweight='bold')
    
    # 4. Queue (BFS)
    ax4 = axes[1, 0]
    ax4.set_title('4. Queue - BFS Traversal', fontsize=12, fontweight='bold')
    
    queue_items = ['Front →', 'A', 'B', 'C', '← Back']
    for i, item in enumerate(queue_items):
        rect = Rectangle((0.1 + i*0.15, 0.4), 0.12, 0.2, facecolor='lightgreen', edgecolor='black')
        ax4.add_patch(rect)
        ax4.text(0.16 + i*0.15, 0.5, item, ha='center', va='center', fontsize=9)
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    ax4.text(0.5, -0.1, 'FIFO: O(1) Enqueue/Dequeue', ha='center', transform=ax4.transAxes, fontweight='bold')
    
    # 5. Heap (Recommendations)
    ax5 = axes[1, 1]
    ax5.set_title('5. Heap - Top-K Recommendations', fontsize=12, fontweight='bold')
    
    # Draw min-heap as tree
    heap_data = ['(3, UserC)', '(4, UserA)', '(5, UserB)']
    # Simple tree visualization
    ax5.text(0.5, 0.8, heap_data[0], ha='center', va='center', 
            bbox=dict(boxstyle='round', facecolor='gold', edgecolor='black'))
    ax5.text(0.3, 0.5, heap_data[1], ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='gold', edgecolor='black'))
    ax5.text(0.7, 0.5, heap_data[2], ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='gold', edgecolor='black'))
    
    # Draw edges
    ax5.plot([0.5, 0.3], [0.75, 0.55], 'k-')
    ax5.plot([0.5, 0.7], [0.75, 0.55], 'k-')
    
    ax5.set_xlim(0, 1)
    ax5.set_ylim(0, 1)
    ax5.axis('off')
    ax5.text(0.5, -0.1, 'O(n log k) for Top-K', ha='center', transform=ax5.transAxes, fontweight='bold')
    
    # 6. Sorting (Timsort)
    ax6 = axes[1, 2]
    ax6.set_title('6. Timsort - Sorted Friends', fontsize=12, fontweight='bold')
    
    sorted_items = ['A', 'B', 'C', 'D', 'E']
    for i, item in enumerate(sorted_items):
        rect = Rectangle((0.1 + i*0.15, 0.4), 0.12, 0.2, facecolor='lightblue', edgecolor='black')
        ax6.add_patch(rect)
        ax6.text(0.16 + i*0.15, 0.5, item, ha='center', va='center', fontsize=12, fontweight='bold')
    ax6.set_xlim(0, 1)
    ax6.set_ylim(0, 1)
    ax6.axis('off')
    ax6.text(0.5, -0.1, 'O(n log n) Sorting + O(log n) Search', ha='center', transform=ax6.transAxes, fontweight='bold')
    
    plt.suptitle('6 Mandatory Data Structures in Social Network', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()


# ============================================================
# 8. MAIN VISUALIZATION FUNCTION
# ============================================================

def create_demo_network():
    """Create a demo network with realistic data"""
    user_manager = UserManager()
    friend_graph = FriendGraph(user_manager)
    
    # Add users
    names = [
        "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry",
        "Ivy", "Jack", "Kevin", "Lisa", "Mike", "Nancy", "Oscar", "Patty"
    ]
    
    user_ids = {}
    for name in names:
        user_ids[name] = user_manager.add_user(name)
    
    # Add friendships (creating a realistic network)
    friendships = [
        ("Alice", "Bob"), ("Alice", "Charlie"), ("Alice", "Diana"),
        ("Bob", "Charlie"), ("Bob", "Eve"), ("Bob", "Frank"),
        ("Charlie", "Diana"), ("Charlie", "Grace"), ("Charlie", "Henry"),
        ("Diana", "Eve"), ("Diana", "Ivy"), ("Diana", "Jack"),
        ("Eve", "Frank"), ("Eve", "Grace"), ("Eve", "Kevin"),
        ("Frank", "Lisa"), ("Frank", "Mike"), ("Frank", "Nancy"),
        ("Grace", "Henry"), ("Grace", "Oscar"), ("Grace", "Patty"),
        ("Henry", "Ivy"), ("Henry", "Jack"), ("Henry", "Kevin"),
        ("Ivy", "Lisa"), ("Ivy", "Mike"), ("Ivy", "Nancy"),
        ("Jack", "Oscar"), ("Jack", "Patty"), ("Jack", "Kevin"),
        ("Lisa", "Mike"), ("Lisa", "Nancy"), ("Lisa", "Oscar"),
        ("Mike", "Patty"), ("Mike", "Kevin"), ("Mike", "Lisa"),
        ("Nancy", "Oscar"), ("Nancy", "Patty"), ("Nancy", "Kevin"),
        ("Oscar", "Patty"), ("Oscar", "Kevin"), ("Patty", "Kevin")
    ]
    
    for name1, name2 in friendships:
        friend_graph.add_friend(user_ids[name1], user_ids[name2])
    
    # Create social network object
    class SocialNetworkWrapper:
        def __init__(self):
            self.user_manager = user_manager
            self.friend_graph = friend_graph
            self.bfs_finder = BFSFriendFinder(friend_graph)
            self.recommendation_engine = RecommendationEngine(friend_graph)
            self.sorting_utils = SortingSearchingUtils(friend_graph, user_manager)
        
        def get_all_users(self):
            return user_manager.get_all_users()
        
        def get_user(self, user_id):
            return user_manager.get_user(user_id)
        
        def get_user_by_name(self, name):
            return user_manager.get_user_by_name(name)
        
        def get_friends(self, user_id):
            return friend_graph.get_friends(user_id)
        
        def get_all_friendships(self):
            return friend_graph.get_all_friendships()
        
        def find_mutual_friends(self, u1, u2):
            return self.bfs_finder.find_mutual_friends(u1, u2)
        
        def recommend_friends(self, user_id, top_k=5):
            return self.recommendation_engine.recommend_friends(user_id, top_k)
        
        def get_sorted_friends(self, user_id):
            return self.sorting_utils.get_sorted_friends(user_id)
        
        def binary_search_friend(self, user_id, target_name):
            return self.sorting_utils.binary_search_friend(user_id, target_name)
    
    return SocialNetworkWrapper()


# ============================================================
# 9. RUN ALL VISUALIZATIONS
# ============================================================

def run_all_visualizations():
    """Run all visualizations"""
    print("=" * 70)
    print("🎨 COMPLETE VISUALIZATION SUITE")
    print("   Visualizing ALL Data Structures and Algorithms")
    print("=" * 70)
    
    # Create demo network
    print("\nCreating demo network...")
    sn = create_demo_network()
    
    while True:
        print("\n" + "=" * 70)
        print("📊 VISUALIZATION MENU")
        print("=" * 70)
        print("1. Graph Visualization - Complete Network")
        print("2. BFS Visualization - Mutual Friends Search")
        print("3. Heap Visualization - Friend Recommendations")
        print("4. Sorting Visualization - Timsort (Friends List)")
        print("5. Binary Search Visualization")
        print("6. Benchmark Results Charts")
        print("7. Data Structure Diagrams (All 6)")
        print("8. RUN ALL VISUALIZATIONS")
        print("9. Exit")
        print("-" * 70)
        
        choice = input("\nEnter choice (1-9): ").strip()
        
        if choice == '1':
            visualize_graph(sn, "Social Network Graph")
        
        elif choice == '2':
            print("\n📌 BFS - Find mutual friends between two users")
            user1 = input("Enter first user name (e.g., Alice): ").strip()
            user2 = input("Enter second user name (e.g., Bob): ").strip()
            visualize_bfs_mutual_friends(sn, user1, user2)
        
        elif choice == '3':
            print("\n📌 Heap - Get friend recommendations")
            user = input("Enter user name (e.g., Alice): ").strip()
            top_k = int(input("Enter top-K (e.g., 5): ").strip() or "5")
            visualize_heap_recommendations(sn, user, top_k)
        
        elif choice == '4':
            print("\n📌 Sorting - Show friends sorted")
            user = input("Enter user name (e.g., Alice): ").strip()
            visualize_sorting_algorithm(sn, user)
        
        elif choice == '5':
            print("\n📌 Binary Search - Find a friend")
            user = input("Enter user name (e.g., Alice): ").strip()
            search = input("Enter friend name to search: ").strip()
            visualize_binary_search(sn, user, search)
        
        elif choice == '6':
            visualize_benchmark_results()
        
        elif choice == '7':
            visualize_data_structures()
        
        elif choice == '8':
            print("\n🎨 Running ALL visualizations...")
            visualize_graph(sn, "Social Network Graph")
            visualize_bfs_mutual_friends(sn, "Alice", "Bob")
            visualize_heap_recommendations(sn, "Alice", 5)
            visualize_sorting_algorithm(sn, "Alice")
            visualize_binary_search(sn, "Alice", "Charlie")
            visualize_benchmark_results()
            visualize_data_structures()
            print("\n✅ ALL visualizations complete!")
        
        elif choice == '9':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    run_all_visualizations()