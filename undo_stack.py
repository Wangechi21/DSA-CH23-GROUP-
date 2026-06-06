# undo_stack.py
# Stack implementation for undo/redo functionality
# Data structure: Stack (LIFO) for action history

class UndoStack:
    def __init__(self, friend_graph):
        self.friend_graph = friend_graph

        # Stack (LIFO) for undo actions
        self.stack = []

        # Stack for redo actions
        self.redo_stack = []

    def push_action(self, action_type, user1_id, user2_id):
        """Push an action onto the undo stack"""
        action = {
            'type': action_type,  # 'add' or 'remove'
            'user1': user1_id,
            'user2': user2_id
        }

        self.stack.append(action)

        # Clear redo history when a new action is performed
        self.redo_stack.clear()

    def undo(self):
        """Undo the last action (LIFO)"""
        if not self.stack:
            return None, "Nothing to undo"

        action = self.stack.pop()

        if action['type'] == 'add':
            # Undo adding a friendship
            self.friend_graph.remove_friend(
                action['user1'],
                action['user2']
            )

        elif action['type'] == 'remove':
            # Undo removing a friendship
            self.friend_graph.add_friend(
                action['user1'],
                action['user2']
            )

        # Store the original action for redo
        self.redo_stack.append(action.copy())

        return action, (
            f"Undid {action['type']} action "
            f"between users {action['user1']} and {action['user2']}"
        )

    def redo(self):
        """Redo a previously undone action"""
        if not self.redo_stack:
            return None, "Nothing to redo"

        action = self.redo_stack.pop()

        if action['type'] == 'add':
            self.friend_graph.add_friend(
                action['user1'],
                action['user2']
            )

        elif action['type'] == 'remove':
            self.friend_graph.remove_friend(
                action['user1'],
                action['user2']
            )

        # Put action back into undo history
        self.stack.append(action.copy())

        return action, (
            f"Redid {action['type']} action "
            f"between users {action['user1']} and {action['user2']}"
        )

    def get_history_size(self):
        """Return number of actions in undo stack"""
        return len(self.stack)

    def clear_history(self):
        """Clear undo and redo history"""
        self.stack.clear()
        self.redo_stack.clear()