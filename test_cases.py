# test_cases.py
# 15 comprehensive test cases including edge cases

class TestRunner:
    def __init__(self, social_network):
        self.sn = social_network
        self.passed = 0
        self.failed = 0
    
    def run_all_tests(self):
        print("=" * 60)
        print("RUNNING 15 TEST CASES - SOCIAL NETWORK")
        print("=" * 60)
        
        self.test_1_add_user()
        self.test_2_add_friend()
        self.test_3_duplicate_friend()
        self.test_4_remove_friend()
        self.test_5_undo_add_friend()
        self.test_6_undo_remove_friend()
        self.test_7_mutual_friends()
        self.test_8_no_mutual_friends()
        self.test_9_recommendations()
        self.test_10_empty_recommendations()
        self.test_11_sorted_friends()
        self.test_12_binary_search_found()
        self.test_13_binary_search_not_found()
        self.test_14_bfs_shortest_path()
        self.test_15_edge_case_empty_graph()
        
        print("\n" + "=" * 60)
        print(f"RESULTS: {self.passed} passed, {self.failed} failed")
        print("=" * 60)
        return self.failed == 0
    
    def assert_equal(self, actual, expected, test_name):
        if actual == expected:
            print(f"  ✓ {test_name}")
            self.passed += 1
            return True
        else:
            print(f"  ✗ {test_name} - Expected {expected}, got {actual}")
            self.failed += 1
            return False
    
    def assert_true(self, condition, test_name):
        if condition:
            print(f"  ✓ {test_name}")
            self.passed += 1
            return True
        else:
            print(f"  ✗ {test_name} - Condition false")
            self.failed += 1
            return False
    
    def test_1_add_user(self):
        # Reset
        self.sn.user_manager.users.clear()
        self.sn.user_manager.next_id = 1
        uid = self.sn.user_manager.add_user("Alice")
        self.assert_equal(uid, 1, "Test 1: Add user returns correct ID")
    
    def test_2_add_friend(self):
        alice = self.sn.user_manager.get_user_by_name("Alice")[0]
        bob = self.sn.user_manager.add_user("Bob")
        self.sn.friend_graph.add_friend(alice, bob)
        self.assert_true(self.sn.friend_graph.are_friends(alice, bob), "Test 2: Add friend creates friendship")
    
    def test_3_duplicate_friend(self):
        alice = self.sn.user_manager.get_user_by_name("Alice")[0]
        bob = self.sn.user_manager.get_user_by_name("Bob")[0]
        self.sn.friend_graph.add_friend(alice, bob)
        self.sn.friend_graph.add_friend(alice, bob)
        self.assert_equal(len(self.sn.friend_graph.get_friends(alice)), 1, "Test 3: Duplicate friend doesn't duplicate")
    
    def test_4_remove_friend(self):
        alice = self.sn.user_manager.get_user_by_name("Alice")[0]
        bob = self.sn.user_manager.get_user_by_name("Bob")[0]
        self.sn.friend_graph.remove_friend(alice, bob)
        self.assert_false = not self.sn.friend_graph.are_friends(alice, bob)
        self.assert_true(self.assert_false, "Test 4: Remove friend deletes friendship")
    
    def test_5_undo_add_friend(self):
        alice = self.sn.user_manager.get_user_by_name("Alice")[0]
        bob = self.sn.user_manager.get_user_by_name("Bob")[0]
        self.sn.friend_graph.add_friend(alice, bob)
        self.sn.undo_stack.push_action('add', alice, bob)
        self.sn.undo_stack.undo()
        self.assert_false = not self.sn.friend_graph.are_friends(alice, bob)
        self.assert_true(self.assert_false, "Test 5: Undo reverses add friend")
    
    def test_6_undo_remove_friend(self):
        alice = self.sn.user_manager.get_user_by_name("Alice")[0]
        bob = self.sn.user_manager.get_user_by_name("Bob")[0]
        self.sn.friend_graph.add_friend(alice, bob)
        self.sn.friend_graph.remove_friend(alice, bob)
        self.sn.undo_stack.push_action('remove', alice, bob)
        self.sn.undo_stack.undo()
        self.assert_true(self.sn.friend_graph.are_friends(alice, bob), "Test 6: Undo reverses remove friend")
    
    def test_7_mutual_friends(self):
        alice = self.sn.user_manager.get_user_by_name("Alice")[0]
        bob = self.sn.user_manager.get_user_by_name("Bob")[0]
        charlie = self.sn.user_manager.add_user("Charlie")
        self.sn.friend_graph.add_friend(alice, bob)
        self.sn.friend_graph.add_friend(alice, charlie)
        self.sn.friend_graph.add_friend(bob, charlie)
        mutual = self.sn.bfs_finder.find_mutual_friends(bob, charlie)
        self.assert_equal(alice in mutual, True, "Test 7: Mutual friends correctly identified")
    
    def test_8_no_mutual_friends(self):
        david = self.sn.user_manager.add_user("David")
        eve = self.sn.user_manager.add_user("Eve")
        mutual = self.sn.bfs_finder.find_mutual_friends(david, eve)
        self.assert_equal(len(mutual), 0, "Test 8: No mutual friends returns empty list")
    
    def test_9_recommendations(self):
        alice = self.sn.user_manager.get_user_by_name("Alice")[0]
        recommendations = self.sn.recommendation_engine.recommend_friends(alice, top_k=3)
        self.assert_true(isinstance(recommendations, list), "Test 9: Recommendations return list")
    
    def test_10_empty_recommendations(self):
        frank = self.sn.user_manager.add_user("Frank")
        recommendations = self.sn.recommendation_engine.recommend_friends(frank, top_k=5)
        self.assert_equal(len(recommendations), 0, "Test 10: Isolated user gets no recommendations")
    
    def test_11_sorted_friends(self):
        alice = self.sn.user_manager.get_user_by_name("Alice")[0]
        sorted_friends = self.sn.sorting_utils.get_sorted_friends(alice)
        names = [f['name'] for f in sorted_friends]
        self.assert_equal(names == sorted(names), True, "Test 11: Friends sorted alphabetically")
    
    def test_12_binary_search_found(self):
        alice = self.sn.user_manager.get_user_by_name("Alice")[0]
        result = self.sn.sorting_utils.binary_search_friend(alice, "Bob")
        self.assert_true(result is not None, "Test 12: Binary search finds existing friend")
    
    def test_13_binary_search_not_found(self):
        alice = self.sn.user_manager.get_user_by_name("Alice")[0]
        result = self.sn.sorting_utils.binary_search_friend(alice, "ZZZ_NotExist")
        self.assert_equal(result, None, "Test 13: Binary search returns None for non-friend")
    
    def test_14_bfs_shortest_path(self):
        alice = self.sn.user_manager.get_user_by_name("Alice")[0]
        charlie = self.sn.user_manager.get_user_by_name("Charlie")[0]
        path = self.sn.bfs_finder.bfs_shortest_path(alice, charlie)
        self.assert_true(path is not None, "Test 14: BFS finds shortest path")
    
    def test_15_edge_case_empty_graph(self):
        from main import SocialNetwork
        empty_sn = SocialNetwork()
        result = empty_sn.bfs_finder.find_mutual_friends(999, 888)
        self.assert_equal(len(result), 0, "Test 15: Empty graph handles invalid IDs gracefully")