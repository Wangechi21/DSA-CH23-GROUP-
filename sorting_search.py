# sorting_searching.py
# Sorting (O(n log n)) and binary search (O(log n)) implementations

import bisect

class SortingSearchingUtils:
    def __init__(self, friend_graph, user_manager):
        self.friend_graph = friend_graph
        self.user_manager = user_manager

    def get_sorted_friends(self, user_id):
        """
        Return friends sorted alphabetically by name.
        Uses Python's Timsort = O(n log n)
        """
        friends_set = self.friend_graph.get_friends(user_id)
        friends_with_names = []

        for friend_id in friends_set:
            user_data = self.user_manager.get_user(friend_id)
            if user_data:
                friends_with_names.append({
                    'id': friend_id,
                    'name': user_data['name']
                })

        # O(n log n) sort by name (Timsort)
        friends_with_names.sort(key=lambda x: x['name'])
        return friends_with_names

    def binary_search_friend(self, user_id, target_name):
        """
        Binary search O(log n) to find if a friend exists by name.
        Requires sorted list first.
        """
        sorted_friends = self.get_sorted_friends(user_id)

        # Extract just the names for binary search
        names = [f['name'] for f in sorted_friends]

        # Using bisect for O(log n) binary search
        index = bisect.bisect_left(names, target_name)

        if index < len(names) and names[index] == target_name:
            return sorted_friends[index]
        return None

    def sort_users_by_friend_count(self):
        """
        Sort all users by number of friends (descending).
        O(n log n) sort.
        """
        users = self.user_manager.get_all_users()
        user_stats = []

        for user in users:
            user_id = user['id']
            friend_count = self.friend_graph.get_friend_count(user_id)
            user_stats.append({
                'id': user_id,
                'name': user['name'],
                'friend_count': friend_count
            })

        # Sort by friend_count descending O(n log n)
        user_stats.sort(key=lambda x: x['friend_count'], reverse=True)
        return user_stats

    def linear_search_user_by_name(self, name_partial):
        """
        Linear search O(n) for partial name match.
        """
        all_users = self.user_manager.get_all_users()
        matches = []

        for user in all_users:
            if name_partial.lower() in user['name'].lower():
                matches.append(user)

        return matches

    def get_sorted_all_users(self):
        """
        Return all users sorted alphabetically by name.
        """
        users = self.user_manager.get_all_users()
        users.sort(key=lambda x: x['name'])
        return users
