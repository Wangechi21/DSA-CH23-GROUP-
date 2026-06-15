# main.py
# Main entry point with CLI interface
# Integrates all data structures and algorithms

import sys

class SocialNetwork:
    def __init__(self):
        from user_manager import UserManager
        from friend_graph import FriendGraph
        from undo_stack import UndoStack
        from bfs_queue import BFSFriendFinder
        from recommendation_heap import RecommendationEngine
        from sorting_searching import SortingSearchingUtils
        
        self.user_manager = UserManager()
        self.friend_graph = FriendGraph(self.user_manager)
        self.undo_stack = UndoStack(self.friend_graph)
        self.bfs_finder = BFSFriendFinder(self.friend_graph)
        self.recommendation_engine = RecommendationEngine(self.friend_graph)
        self.sorting_utils = SortingSearchingUtils(self.friend_graph, self.user_manager)
    
    def run_cli(self):
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
                    uid = self.user_manager.add_user(cmd[1])
                    print(f"  ✓ Added user '{cmd[1]}' with ID {uid}")
                
                elif cmd[0] == 'add_friend' and len(cmd) == 3:
                    u1_id, u1_data = self.user_manager.get_user_by_name(cmd[1])
                    u2_id, u2_data = self.user_manager.get_user_by_name(cmd[2])
                    if u1_id and u2_id:
                        self.friend_graph.add_friend(u1_id, u2_id)
                        self.undo_stack.push_action('add', u1_id, u2_id)
                        print(f"  ✓ {cmd[1]} and {cmd[2]} are now friends")
                    else:
                        print("  ✗ User not found")
                
                elif cmd[0] == 'remove_friend' and len(cmd) == 3:
                    u1_id, u1_data = self.user_manager.get_user_by_name(cmd[1])
                    u2_id, u2_data = self.user_manager.get_user_by_name(cmd[2])
                    if u1_id and u2_id:
                        if self.friend_graph.are_friends(u1_id, u2_id):
                            self.friend_graph.remove_friend(u1_id, u2_id)
                            self.undo_stack.push_action('remove', u1_id, u2_id)
                            print(f"  ✓ {cmd[1]} and {cmd[2]} are no longer friends")
                        else:
                            print(f"  ✗ {cmd[1]} and {cmd[2]} are not friends")
                    else:
                        print("  ✗ User not found")
                
                elif cmd[0] == 'undo':
                    _, msg = self.undo_stack.undo()
                    print(f"  ✓ {msg}")
                
                elif cmd[0] == 'mutual' and len(cmd) == 3:
                    u1_id, u1_data = self.user_manager.get_user_by_name(cmd[1])
                    u2_id, u2_data = self.user_manager.get_user_by_name(cmd[2])
                    if u1_id and u2_id:
                        mutual_ids = self.bfs_finder.find_mutual_friends(u1_id, u2_id)
                        names = []
                        for mid in mutual_ids:
                            user = self.user_manager.get_user(mid)
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
                    u_id, u_data = self.user_manager.get_user_by_name(name)
                    if u_id:
                        recs = self.recommendation_engine.recommend_friends(u_id, top_k)
                        if recs:
                            print(f"  Top {top_k} recommendations for {name}:")
                            for friend_id, score in recs:
                                friend = self.user_manager.get_user(friend_id)
                                if friend:
                                    print(f"    - {friend['name']} ({score} mutual friends)")
                        else:
                            print(f"  No recommendations available for {name}")
                    else:
                        print("  ✗ User not found")
                
                elif cmd[0] == 'friends' and len(cmd) == 2:
                    u_id, u_data = self.user_manager.get_user_by_name(cmd[1])
                    if u_id:
                        sorted_friends = self.sorting_utils.get_sorted_friends(u_id)
                        if sorted_friends:
                            print(f"  Friends of {cmd[1]} (sorted by name):")
                            for f in sorted_friends:
                                print(f"    - {f['name']}")
                        else:
                            print(f"  {cmd[1]} has no friends yet")
                    else:
                        print("  ✗ User not found")
                
                elif cmd[0] == 'search' and len(cmd) == 3:
                    u_id, u_data = self.user_manager.get_user_by_name(cmd[1])
                    if u_id:
                        result = self.sorting_utils.binary_search_friend(u_id, cmd[2])
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
                    print(f"  Total users: {self.user_manager.get_user_count()}")
                    friendships = self.friend_graph.get_all_friendships()
                    print(f"  Total friendships: {len(friendships)}")
                    print(f"  Undo stack size: {self.undo_stack.get_history_size()}")
                    print(f"  Average friends per user: {sum(self.friend_graph.get_friend_count(uid) for uid in self.user_manager.users) / max(1, self.user_manager.get_user_count()):.2f}")
                
                else:
                    print("  Unknown command. Type 'exit' to quit.")
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"  Error: {e}")

def main():
    sn = SocialNetwork()
    
    # Add demo data
    print("\nLoading demo data...")
    alice = sn.user_manager.add_user("Alice")
    bob = sn.user_manager.add_user("Bob")
    charlie = sn.user_manager.add_user("Charlie")
    diana = sn.user_manager.add_user("Diana")
    eve = sn.user_manager.add_user("Eve")
    
    sn.friend_graph.add_friend(alice, bob)
    sn.friend_graph.add_friend(alice, charlie)
    sn.friend_graph.add_friend(bob, charlie)
    sn.friend_graph.add_friend(diana, eve)
    print("Demo data loaded: Alice, Bob, Charlie, Diana, Eve")
    print("Alice is friends with Bob and Charlie")
    print("Bob and Charlie are friends")
    print("Diana and Eve are friends")
    
    sn.run_cli()

if __name__ == "__main__":
    main()
