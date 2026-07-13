# main.py
# Main entry point with CLI interface
# Integrates all data structures and algorithms

import sys
import time
import random

# Make sure all imports work properly
from user_manager import UserManager
from friend_graph import FriendGraph
from undo_stack import UndoStack
from bfs_queue import BFSFriendFinder
from recommendation_heap import RecommendationEngine
from sorting_searching import SortingSearchingUtils


class SocialNetwork:
    def __init__(self):
        """Initialize all data structures"""
        self.user_manager = UserManager()
        self.friend_graph = FriendGraph(self.user_manager)
        self.undo_stack = UndoStack(self.friend_graph)
        self.bfs_finder = BFSFriendFinder(self.friend_graph)
        self.recommendation_engine = RecommendationEngine(self.friend_graph)
        self.sorting_utils = SortingSearchingUtils(self.friend_graph, self.user_manager)
    
    # ========== USER OPERATIONS ==========
    
    def add_user(self, name):
        """Add a new user - O(1)"""
        return self.user_manager.add_user(name)
    
    def get_user(self, user_id):
        """Get user by ID - O(1)"""
        return self.user_manager.get_user(user_id)
    
    def get_user_by_name(self, name):
        """Get user by name - O(n)"""
        return self.user_manager.get_user_by_name(name)
    
    def get_all_users(self):
        """Get all users - O(n)"""
        return self.user_manager.get_all_users()
    
    def get_user_count(self):
        """Get total users - O(1)"""
        return self.user_manager.get_user_count()
    
    # ========== FRIEND OPERATIONS ==========
    
    def add_friend(self, user1_id, user2_id):
        """Add friendship - O(1)"""
        result = self.friend_graph.add_friend(user1_id, user2_id)
        if result:
            self.undo_stack.push_action('add', user1_id, user2_id)
        return result
    
    def remove_friend(self, user1_id, user2_id):
        """Remove friendship - O(1)"""
        result = self.friend_graph.remove_friend(user1_id, user2_id)
        if result:
            self.undo_stack.push_action('remove', user1_id, user2_id)
        return result
    
    def are_friends(self, user1_id, user2_id):
        """Check if two users are friends - O(1)"""
        return self.friend_graph.are_friends(user1_id, user2_id)
    
    def get_friends(self, user_id):
        """Get all friends of a user - O(1)"""
        return self.friend_graph.get_friends(user_id)
    
    def get_friend_count(self, user_id):
        """Get number of friends - O(1)"""
        return self.friend_graph.get_friend_count(user_id)
    
    def get_all_friendships(self):
        """Get all friendships - O(E)"""
        return self.friend_graph.get_all_friendships()
    
    # ========== BFS OPERATIONS ==========
    
    def find_mutual_friends(self, user1_id, user2_id):
        """Find mutual friends using BFS + hash map - O(V+E)"""
        return self.bfs_finder.find_mutual_friends(user1_id, user2_id)
    
    def bfs_shortest_path(self, start_id, target_id):
        """Find shortest path using BFS - O(V+E)"""
        return self.bfs_finder.bfs_shortest_path(start_id, target_id)
    
    def get_friends_at_distance(self, start_id, distance):
        """Get friends at exact distance - O(V+E)"""
        return self.bfs_finder.get_friends_at_distance(start_id, distance)
    
    def are_connected(self, user1_id, user2_id):
        """Check if two users are connected - O(V+E)"""
        return self.bfs_finder.are_connected(user1_id, user2_id)
    
    # ========== RECOMMENDATION OPERATIONS ==========
    
    def recommend_friends(self, user_id, top_k=5):
        """Get top-K friend recommendations using heap - O(n log k)"""
        return self.recommendation_engine.recommend_friends(user_id, top_k)
    
    def get_top_k_friends(self, user_id, top_k=10):
        """Get top-K friends by popularity - O(n log k)"""
        return self.recommendation_engine.get_top_k_friends(user_id, top_k)
    
    # ========== SORTING & SEARCHING OPERATIONS ==========
    
    def get_sorted_friends(self, user_id):
        """Get friends sorted alphabetically - O(m log m)"""
        return self.sorting_utils.get_sorted_friends(user_id)
    
    def binary_search_friend(self, user_id, target_name):
        """Binary search for a friend by name - O(log m)"""
        return self.sorting_utils.binary_search_friend(user_id, target_name)
    
    def sort_users_by_friend_count(self):
        """Sort users by friend count - O(n log n)"""
        return self.sorting_utils.sort_users_by_friend_count()
    
    def linear_search_user_by_name(self, name_partial):
        """Linear search for users by partial name - O(n)"""
        return self.sorting_utils.linear_search_user_by_name(name_partial)
    
    def get_sorted_all_users(self):
        """Get all users sorted alphabetically - O(n log n)"""
        return self.sorting_utils.get_sorted_all_users()
    
    # ========== UNDO OPERATIONS ==========
    
    def undo(self):
        """Undo last action - O(1)"""
        return self.undo_stack.undo()
    
    def redo(self):
        """Redo last undone action - O(1)"""
        return self.undo_stack.redo()
    
    def get_undo_history_size(self):
        """Get undo history size - O(1)"""
        return self.undo_stack.get_history_size()
    
    def clear_undo_history(self):
        """Clear undo history - O(1)"""
        return self.undo_stack.clear_history()
    
    # ========== BULK OPERATIONS FOR BENCHMARKING ==========
    
    def bulk_add_users(self, count):
        """Add multiple users for benchmarking"""
        user_ids = []
        for i in range(count):
            uid = self.add_user(f"BenchUser_{i}")
            user_ids.append(uid)
        return user_ids
    
    def bulk_add_friendships(self, user_ids, count):
        """Add multiple friendships for benchmarking"""
        friendships = 0
        for i in range(count):
            u1 = random.choice(user_ids)
            u2 = random.choice(user_ids)
            if u1 != u2 and not self.are_friends(u1, u2):
                self.add_friend(u1, u2)
                friendships += 1
        return friendships
    
    def bulk_mutual_friends(self, user_ids, count):
        """Run multiple mutual friend queries"""
        results = []
        for i in range(count):
            u1 = random.choice(user_ids)
            u2 = random.choice(user_ids)
            if u1 != u2:
                results.append(self.find_mutual_friends(u1, u2))
        return results
    
    def bulk_recommendations(self, user_ids, count, top_k=5):
        """Run multiple recommendation queries"""
        results = []
        for i in range(count):
            u = random.choice(user_ids)
            results.append(self.recommend_friends(u, top_k))
        return results
    
    def bulk_sort_friends(self, user_ids, count):
        """Run multiple sort operations"""
        results = []
        for i in range(count):
            u = random.choice(user_ids)
            results.append(self.get_sorted_friends(u))
        return results
    
    def bulk_binary_search(self, user_ids, count):
        """Run multiple binary searches"""
        results = []
        for i in range(count):
            u = random.choice(user_ids)
            results.append(self.binary_search_friend(u, "NonExistentUser"))
        return results
    
    # ========== RESET FOR BENCHMARKING ==========
    
    def reset(self):
        """Reset the entire system for clean benchmarking"""
        self.user_manager = UserManager()
        self.friend_graph = FriendGraph(self.user_manager)
        self.undo_stack = UndoStack(self.friend_graph)
        self.bfs_finder = BFSFriendFinder(self.friend_graph)
        self.recommendation_engine = RecommendationEngine(self.friend_graph)
        self.sorting_utils = SortingSearchingUtils(self.friend_graph, self.user_manager)
    
    # ========== CLI INTERFACE ==========
    
    def run_cli(self):
        """Run the command-line interface"""
        print("\n" + "=" * 60)
        print("SOCIAL NETWORK DEMO SYSTEM - THEME A1")
        print("Data Structures: Hash Map, Graph, Stack, Queue, Heap")
        print("Algorithms: BFS, Sort (O(n log n)), Binary Search")
        print("=" * 60)
        print("\nCommands:")
        print("  add_user <name>                    - Add new user")
        print("  add_friend <name1> <name2>         - Make two users friends")
        print("  remove_friend <name1> <name2>      - Remove friendship")
        print("  undo                               - Undo last action (stack)")
        print("  redo                               - Redo last undone action")
        print("  mutual <name1> <name2>             - Find mutual friends (BFS+queue)")
        print("  recommend <name> [top_k]           - Get friend recommendations (heap)")
        print("  friends <name>                     - List friends (sorted)")
        print("  search <name> <friend_name>        - Search friend (binary search)")
        print("  benchmark                          - Run performance tests")
        print("  test                               - Run all test cases")
        print("  stats                              - Show system statistics")
        print("  exit                               - Exit program")
        print("-" * 60)
        
        while True:
            try:
                cmd = input("\n> ").strip().split()
                if not cmd:
                    continue
                
                if cmd[0] == 'exit':
                    print("Goodbye!")
                    break
                
                elif cmd[0] == 'add_user' and len(cmd) == 2:
                    uid = self.add_user(cmd[1])
                    print(f"  ✓ Added user '{cmd[1]}' with ID {uid}")
                
                elif cmd[0] == 'add_friend' and len(cmd) == 3:
                    u1_id, u1_data = self.get_user_by_name(cmd[1])
                    u2_id, u2_data = self.get_user_by_name(cmd[2])
                    if u1_id and u2_id:
                        self.add_friend(u1_id, u2_id)
                        print(f"  ✓ {cmd[1]} and {cmd[2]} are now friends")
                    else:
                        print("  ✗ User not found")
                
                elif cmd[0] == 'remove_friend' and len(cmd) == 3:
                    u1_id, u1_data = self.get_user_by_name(cmd[1])
                    u2_id, u2_data = self.get_user_by_name(cmd[2])
                    if u1_id and u2_id:
                        if self.are_friends(u1_id, u2_id):
                            self.remove_friend(u1_id, u2_id)
                            print(f"  ✓ {cmd[1]} and {cmd[2]} are no longer friends")
                        else:
                            print(f"  ✗ {cmd[1]} and {cmd[2]} are not friends")
                    else:
                        print("  ✗ User not found")
                
                elif cmd[0] == 'undo':
                    _, msg = self.undo()
                    print(f"  ✓ {msg}")
                
                elif cmd[0] == 'redo':
                    _, msg = self.redo()
                    print(f"  ✓ {msg}")
                
                elif cmd[0] == 'mutual' and len(cmd) == 3:
                    u1_id, u1_data = self.get_user_by_name(cmd[1])
                    u2_id, u2_data = self.get_user_by_name(cmd[2])
                    if u1_id and u2_id:
                        mutual_ids = self.find_mutual_friends(u1_id, u2_id)
                        names = []
                        for mid in mutual_ids:
                            user = self.get_user(mid)
                            if user:
                                names.append(user['name'])
                        if names:
                            print(f"  Mutual friends of {cmd[1]} and {cmd[2]}: {names}")
                        else:
                            print(f"  No mutual friends found")
                    else:
                        print("  ✗ User not found")
                
                elif cmd[0] == 'recommend':
                    if len(cmd) < 2:
                        print("  Usage: recommend <name> [top_k]")
                        continue
                    name = cmd[1]
                    top_k = int(cmd[2]) if len(cmd) > 2 else 5
                    u_id, u_data = self.get_user_by_name(name)
                    if u_id:
                        recs = self.recommend_friends(u_id, top_k)
                        if recs:
                            print(f"  Top {top_k} recommendations for {name}:")
                            for friend_id, score in recs:
                                friend = self.get_user(friend_id)
                                if friend:
                                    print(f"    - {friend['name']} ({score} mutual friends)")
                        else:
                            print(f"  No recommendations available for {name}")
                    else:
                        print("  ✗ User not found")
                
                elif cmd[0] == 'friends' and len(cmd) == 2:
                    u_id, u_data = self.get_user_by_name(cmd[1])
                    if u_id:
                        sorted_friends = self.get_sorted_friends(u_id)
                        if sorted_friends:
                            print(f"  Friends of {cmd[1]} (sorted by name):")
                            for f in sorted_friends:
                                print(f"    - {f['name']}")
                        else:
                            print(f"  {cmd[1]} has no friends yet")
                    else:
                        print("  ✗ User not found")
                
                elif cmd[0] == 'search' and len(cmd) == 3:
                    u_id, u_data = self.get_user_by_name(cmd[1])
                    if u_id:
                        result = self.binary_search_friend(u_id, cmd[2])
                        if result:
                            print(f"  ✓ Found: {cmd[2]} is a friend of {cmd[1]}")
                        else:
                            print(f"  ✗ {cmd[2]} is not a friend of {cmd[1]}")
                    else:
                        print("  ✗ User not found")
                
                elif cmd[0] == 'benchmark':
                    from benchmark import Benchmark
                    bm = Benchmark(self)
                    bm.run_all_benchmarks()
                
                elif cmd[0] == 'test':
                    from test_cases import TestRunner
                    tr = TestRunner(self)
                    tr.run_all_tests()
                
                elif cmd[0] == 'stats':
                    print("\n=== SYSTEM STATISTICS ===")
                    print(f"  Total users: {self.get_user_count()}")
                    friendships = self.get_all_friendships()
                    print(f"  Total friendships: {len(friendships)}")
                    print(f"  Undo stack size: {self.get_undo_history_size()}")
                    avg_friends = 0
                    for uid in self.user_manager.users:
                        avg_friends += self.get_friend_count(uid)
                    avg_friends = avg_friends / max(1, self.get_user_count())
                    print(f"  Average friends per user: {avg_friends:.2f}")
                
                else:
                    print("  Unknown command. Type 'exit' to quit.")
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"  Error: {e}")


def main():
    """Main entry point"""
    sn = SocialNetwork()
    
    # Add demo data
    print("\nLoading demo data...")
    alice = sn.add_user("Alice")
    bob = sn.add_user("Bob")
    charlie = sn.add_user("Charlie")
    diana = sn.add_user("Diana")
    eve = sn.add_user("Eve")
    
    sn.add_friend(alice, bob)
    sn.add_friend(alice, charlie)
    sn.add_friend(bob, charlie)
    sn.add_friend(diana, eve)
    
    print("Demo data loaded: Alice, Bob, Charlie, Diana, Eve")
    print("Alice is friends with Bob and Charlie")
    print("Bob and Charlie are friends")
    print("Diana and Eve are friends")
    
    sn.run_cli()


if __name__ == "__main__":
    main()