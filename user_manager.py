# user_manager.py
# Handles user creation, lookup, and deletion using hash map
# Data structure: Hash Table (Python dict) for O(1) lookups

class UserManager:
    def __init__(self):
        # Hash map: user_id -> user_data (fast O(1) lookup)
        self.users = {}
        self.next_id = 1
    
    def add_user(self, name):
        """Add a new user. Returns user_id."""
        user_id = self.next_id
        self.users[user_id] = {
            'id': user_id,
            'name': name,
            'created_at': None
        }
        self.next_id += 1
        return user_id
    
    def get_user(self, user_id):
        """O(1) hash map lookup"""
        return self.users.get(user_id)
    
    def get_user_by_name(self, name):
        """O(n) search by name (linear scan)"""
        for user_id, data in self.users.items():
            if data['name'] == name:
                return user_id, data
        return None, None
    
    def delete_user(self, user_id):
        """Remove user from hash map"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    def get_all_users(self):
        """Return list of all users"""
        return list(self.users.values())
    
    def get_user_count(self):
        """Return total number of users"""
        return len(self.users)
