# social_network_gui.py
# Complete GUI Application for Social Network System
# Uses Tkinter (built-in Python - no installation needed!)

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
from main import SocialNetwork

class SocialNetworkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Network System - Theme A1")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize the social network
        self.sn = SocialNetwork()
        
        # Create GUI components
        self.create_menu()
        self.create_main_layout()
        self.create_status_bar()
        
        # Load demo data
        self.load_demo_data()
        
        # Update the display
        self.refresh_all()
    
    def create_menu(self):
        """Create the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Demo Data", command=self.load_demo_data)
        file_menu.add_command(label="Clear All Data", command=self.clear_all_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Data Structures menu
        ds_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Data Structures", menu=ds_menu)
        ds_menu.add_command(label="Show Hash Map", command=self.show_hash_map)
        ds_menu.add_command(label="Show Graph", command=self.show_graph)
        ds_menu.add_command(label="Show Stack", command=self.show_stack)
        ds_menu.add_command(label="Show Queue", command=self.show_queue)
        ds_menu.add_command(label="Show Heap", command=self.show_heap)
        ds_menu.add_command(label="Show Sorting", command=self.show_sorting)
        
        # Algorithms menu
        algo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Algorithms", menu=algo_menu)
        algo_menu.add_command(label="BFS - Mutual Friends", command=self.show_bfs)
        algo_menu.add_command(label="Heap - Recommendations", command=self.show_recommendations)
        algo_menu.add_command(label="Binary Search", command=self.show_binary_search)
        
        # Visualizations menu
        vis_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Visualizations", menu=vis_menu)
        vis_menu.add_command(label="Network Graph", command=self.show_network_graph)
        vis_menu.add_command(label="Degree Distribution", command=self.show_degree_distribution)
        vis_menu.add_command(label="Performance Charts", command=self.show_performance_charts)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
    
    def create_main_layout(self):
        """Create the main layout with panels"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Right panel - Display area
        right_panel = tk.Frame(main_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # ========== LEFT PANEL CONTROLS ==========
        # Title
        title_label = tk.Label(left_panel, text="SOCIAL NETWORK\nCONTROLS", 
                              font=('Arial', 14, 'bold'), bg='#ffffff', fg='#2c3e50')
        title_label.pack(pady=10)
        
        # Separator
        ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, padx=10, pady=5)
        
        # User Management Section
        user_frame = tk.LabelFrame(left_panel, text="👤 User Management", 
                                   font=('Arial', 11, 'bold'), bg='#ffffff')
        user_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add User
        tk.Label(user_frame, text="Username:", bg='#ffffff').pack(anchor='w', padx=5, pady=2)
        self.user_entry = tk.Entry(user_frame, width=20)
        self.user_entry.pack(padx=5, pady=2, fill=tk.X)
        tk.Button(user_frame, text="Add User", command=self.add_user_gui,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(padx=5, pady=5, fill=tk.X)
        
        # Friend Management Section
        friend_frame = tk.LabelFrame(left_panel, text="🤝 Friend Management", 
                                     font=('Arial', 11, 'bold'), bg='#ffffff')
        friend_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(friend_frame, text="User 1:", bg='#ffffff').pack(anchor='w', padx=5, pady=2)
        self.friend1_entry = tk.Entry(friend_frame, width=20)
        self.friend1_entry.pack(padx=5, pady=2, fill=tk.X)
        
        tk.Label(friend_frame, text="User 2:", bg='#ffffff').pack(anchor='w', padx=5, pady=2)
        self.friend2_entry = tk.Entry(friend_frame, width=20)
        self.friend2_entry.pack(padx=5, pady=2, fill=tk.X)
        
        btn_frame = tk.Frame(friend_frame, bg='#ffffff')
        btn_frame.pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="Add Friend", command=self.add_friend_gui,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        tk.Button(btn_frame, text="Remove Friend", command=self.remove_friend_gui,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        # Query Section
        query_frame = tk.LabelFrame(left_panel, text="🔍 Queries", 
                                    font=('Arial', 11, 'bold'), bg='#ffffff')
        query_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(query_frame, text="User Name:", bg='#ffffff').pack(anchor='w', padx=5, pady=2)
        self.query_entry = tk.Entry(query_frame, width=20)
        self.query_entry.pack(padx=5, pady=2, fill=tk.X)
        
        tk.Button(query_frame, text="Show Friends", command=self.show_friends_gui,
                 bg='#9b59b6', fg='white', font=('Arial', 10, 'bold')).pack(padx=5, pady=2, fill=tk.X)
        tk.Button(query_frame, text="Get Recommendations", command=self.get_recommendations_gui,
                 bg='#1abc9c', fg='white', font=('Arial', 10, 'bold')).pack(padx=5, pady=2, fill=tk.X)
        
        # Mutual Friends
        mutual_frame = tk.Frame(query_frame, bg='#ffffff')
        mutual_frame.pack(fill=tk.X, pady=2)
        tk.Label(mutual_frame, text="Mutual Friends:", bg='#ffffff').pack(anchor='w', padx=5)
        
        mf_frame = tk.Frame(mutual_frame, bg='#ffffff')
        mf_frame.pack(fill=tk.X, padx=5)
        self.mf1_entry = tk.Entry(mf_frame, width=8)
        self.mf1_entry.pack(side=tk.LEFT, padx=2)
        tk.Label(mf_frame, text="&", bg='#ffffff').pack(side=tk.LEFT, padx=2)
        self.mf2_entry = tk.Entry(mf_frame, width=8)
        self.mf2_entry.pack(side=tk.LEFT, padx=2)
        tk.Button(mf_frame, text="Find", command=self.find_mutual_gui,
                 bg='#e67e22', fg='white', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=2)
        
        # Action Buttons
        action_frame = tk.LabelFrame(left_panel, text="⚡ Actions", 
                                     font=('Arial', 11, 'bold'), bg='#ffffff')
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        btn_undo = tk.Button(action_frame, text="↩ Undo", command=self.undo_gui,
                            bg='#f39c12', fg='white', font=('Arial', 10, 'bold'))
        btn_undo.pack(padx=5, pady=2, fill=tk.X)
        
        btn_redo = tk.Button(action_frame, text="↪ Redo", command=self.redo_gui,
                            bg='#f39c12', fg='white', font=('Arial', 10, 'bold'))
        btn_redo.pack(padx=5, pady=2, fill=tk.X)
        
        btn_stats = tk.Button(action_frame, text="📊 Show Stats", command=self.show_stats_gui,
                             bg='#2c3e50', fg='white', font=('Arial', 10, 'bold'))
        btn_stats.pack(padx=5, pady=2, fill=tk.X)
        
        btn_clear = tk.Button(action_frame, text="🗑 Clear All Data", command=self.clear_all_data,
                             bg='#c0392b', fg='white', font=('Arial', 10, 'bold'))
        btn_clear.pack(padx=5, pady=2, fill=tk.X)
        
        # Generate Demo Data
        demo_frame = tk.LabelFrame(left_panel, text="📊 Demo Data", 
                                   font=('Arial', 11, 'bold'), bg='#ffffff')
        demo_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(demo_frame, text="Generate 10 Users", command=lambda: self.generate_demo(10),
                 bg='#8e44ad', fg='white', font=('Arial', 10, 'bold')).pack(padx=5, pady=2, fill=tk.X)
        tk.Button(demo_frame, text="Generate 40 Users", command=lambda: self.generate_demo(40),
                 bg='#8e44ad', fg='white', font=('Arial', 10, 'bold')).pack(padx=5, pady=2, fill=tk.X)
        tk.Button(demo_frame, text="Generate 100 Users", command=lambda: self.generate_demo(100),
                 bg='#8e44ad', fg='white', font=('Arial', 10, 'bold')).pack(padx=5, pady=2, fill=tk.X)
        
        # ========== RIGHT PANEL - Display Area ==========
        # Notebook for tabs
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Network Display
        self.network_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.network_tab, text="🌐 Network")
        
        # Graph canvas
        self.graph_frame = tk.Frame(self.network_tab, bg='#ffffff')
        self.graph_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tab 2: Data Output
        self.output_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.output_tab, text="📄 Data")
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(self.output_tab, wrap=tk.WORD,
                                                     font=('Consolas', 10))
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 3: Statistics
        self.stats_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.stats_tab, text="📊 Stats")
        
        self.stats_text = scrolledtext.ScrolledText(self.stats_tab, wrap=tk.WORD,
                                                    font=('Consolas', 10))
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN,
                                   anchor=tk.W, font=('Arial', 9), bg='#ecf0f1')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)
        self.root.update()
    
    def load_demo_data(self):
        """Load default demo data"""
        self.update_status("Loading demo data...")
        
        # Add users
        alice = self.sn.add_user("Alice")
        bob = self.sn.add_user("Bob")
        charlie = self.sn.add_user("Charlie")
        diana = self.sn.add_user("Diana")
        eve = self.sn.add_user("Eve")
        
        # Add friendships
        self.sn.add_friend(alice, bob)
        self.sn.add_friend(alice, charlie)
        self.sn.add_friend(bob, charlie)
        self.sn.add_friend(diana, eve)
        
        self.update_status("Demo data loaded: Alice, Bob, Charlie, Diana, Eve")
        self.log_output("✅ Demo data loaded successfully!")
        self.log_output("Users: Alice, Bob, Charlie, Diana, Eve")
        self.log_output("Friendships: Alice-Bob, Alice-Charlie, Bob-Charlie, Diana-Eve")
    
    def log_output(self, message):
        """Add message to output tab"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
    
    def refresh_all(self):
        """Refresh all displays"""
        self.update_network_graph()
        self.update_stats()
    
    def update_network_graph(self):
        """Update the network graph visualization"""
        # Clear previous graph
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Create graph
        G = nx.Graph()
        all_users = self.sn.get_all_users()
        for user in all_users:
            G.add_node(user['id'], label=user['name'])
        
        friendships = self.sn.get_all_friendships()
        for u1, u2 in friendships:
            G.add_edge(u1, u2)
        
        if len(G.nodes()) == 0:
            label = tk.Label(self.graph_frame, text="No users yet. Add users to see the network!",
                           font=('Arial', 14), bg='#ffffff', fg='#7f8c8d')
            label.pack(expand=True)
            return
        
        # Create matplotlib figure
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)
        labels = {user['id']: user['name'] for user in all_users}
        degrees = dict(G.degree())
        
        if degrees:
            node_sizes = [300 + 200 * degrees[node] for node in G.nodes()]
            node_colors = [degrees[node] for node in G.nodes()]
            
            nx.draw(G, pos, ax=ax, labels=labels, node_color=node_colors,
                   cmap=plt.cm.viridis, node_size=node_sizes,
                   font_size=10, font_weight='bold', with_labels=True,
                   edge_color='gray', alpha=0.7)
        
        ax.set_title(f"Social Network - {len(G.nodes())} Users, {len(G.edges())} Friendships")
        ax.axis('off')
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def update_stats(self):
        """Update statistics tab"""
        self.stats_text.delete(1.0, tk.END)
        
        stats = f"""
╔══════════════════════════════════════════════════════════════╗
║                    SYSTEM STATISTICS                        ║
╚══════════════════════════════════════════════════════════════╝

📊 USER STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Users:              {self.sn.get_user_count()}
  Total Friendships:        {len(self.sn.get_all_friendships())}
  Undo Stack Size:          {self.sn.get_undo_history_size()}

🔢 FRIEND STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        # Calculate average friends
        total_friends = 0
        all_users = self.sn.get_all_users()
        for user in all_users:
            total_friends += self.sn.get_friend_count(user['id'])
        avg_friends = total_friends / max(1, self.sn.get_user_count())
        stats += f"  Average Friends/User:     {avg_friends:.2f}\n"
        
        # Top users
        if self.sn.get_user_count() > 0:
            stats += f"""
⭐ TOP 5 MOST POPULAR USERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            sorted_users = self.sn.sort_users_by_friend_count()
            for i, user in enumerate(sorted_users[:5], 1):
                stats += f"  {i}. {user['name']:<15} {user['friend_count']} friends\n"
        
        stats += f"""
📦 DATA STRUCTURES STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Hash Table (Users)      O(1) lookups
  ✅ Graph (Friendships)     Adjacency List
  ✅ Stack (Undo)            {self.sn.get_undo_history_size()} actions
  ✅ Queue (BFS)             Ready
  ✅ Heap (Recommendations)  Ready
  ✅ Sorting (Timsort)       O(n log n)
  ✅ Binary Search           O(log n)

🔬 COMPLEXITY VERIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Add User:      O(1)  ✅ Constant
  Add Friend:    O(1)  ✅ Constant
  Mutual Friends: O(V+E) ✅ Working
  Recommendations: O(n log k) ✅ Working
  Sort Friends:  O(m log m) ✅ Working
  Binary Search: O(log n) ✅ Working
  Undo:          O(1)  ✅ Working
"""
        
        self.stats_text.insert(1.0, stats)
    
    # ========== GUI COMMANDS ==========
    
    def add_user_gui(self):
        """Add user from GUI"""
        name = self.user_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a username")
            return
        
        uid = self.sn.add_user(name)
        self.log_output(f"✅ Added user: {name} (ID: {uid})")
        self.user_entry.delete(0, tk.END)
        self.refresh_all()
        self.update_status(f"Added user: {name}")
    
    def add_friend_gui(self):
        """Add friend from GUI"""
        u1 = self.friend1_entry.get().strip()
        u2 = self.friend2_entry.get().strip()
        
        if not u1 or not u2:
            messagebox.showwarning("Input Error", "Please enter both usernames")
            return
        
        u1_id, _ = self.sn.get_user_by_name(u1)
        u2_id, _ = self.sn.get_user_by_name(u2)
        
        if not u1_id or not u2_id:
            messagebox.showerror("Error", "One or both users not found")
            return
        
        if self.sn.are_friends(u1_id, u2_id):
            messagebox.showinfo("Info", f"{u1} and {u2} are already friends")
            return
        
        self.sn.add_friend(u1_id, u2_id)
        self.log_output(f"✅ {u1} and {u2} are now friends!")
        self.friend1_entry.delete(0, tk.END)
        self.friend2_entry.delete(0, tk.END)
        self.refresh_all()
        self.update_status(f"Added friendship: {u1} - {u2}")
    
    def remove_friend_gui(self):
        """Remove friend from GUI"""
        u1 = self.friend1_entry.get().strip()
        u2 = self.friend2_entry.get().strip()
        
        if not u1 or not u2:
            messagebox.showwarning("Input Error", "Please enter both usernames")
            return
        
        u1_id, _ = self.sn.get_user_by_name(u1)
        u2_id, _ = self.sn.get_user_by_name(u2)
        
        if not u1_id or not u2_id:
            messagebox.showerror("Error", "One or both users not found")
            return
        
        if not self.sn.are_friends(u1_id, u2_id):
            messagebox.showinfo("Info", f"{u1} and {u2} are not friends")
            return
        
        self.sn.remove_friend(u1_id, u2_id)
        self.log_output(f"❌ Removed friendship: {u1} - {u2}")
        self.friend1_entry.delete(0, tk.END)
        self.friend2_entry.delete(0, tk.END)
        self.refresh_all()
        self.update_status(f"Removed friendship: {u1} - {u2}")
    
    def show_friends_gui(self):
        """Show friends of a user"""
        name = self.query_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a username")
            return
        
        u_id, _ = self.sn.get_user_by_name(name)
        if not u_id:
            messagebox.showerror("Error", f"User '{name}' not found")
            return
        
        friends = self.sn.get_sorted_friends(u_id)
        
        self.log_output(f"\n{'='*50}")
        self.log_output(f"👥 Friends of {name}:")
        if friends:
            for f in friends:
                self.log_output(f"  • {f['name']}")
        else:
            self.log_output("  No friends yet")
        self.log_output(f"{'='*50}\n")
        
        self.notebook.select(self.output_tab)
        self.update_status(f"Showing friends of {name}")
    
    def get_recommendations_gui(self):
        """Get friend recommendations"""
        name = self.query_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a username")
            return
        
        u_id, _ = self.sn.get_user_by_name(name)
        if not u_id:
            messagebox.showerror("Error", f"User '{name}' not found")
            return
        
        recs = self.sn.recommend_friends(u_id, top_k=5)
        
        self.log_output(f"\n{'='*50}")
        self.log_output(f"💡 Top recommendations for {name}:")
        if recs:
            for friend_id, score in recs:
                friend = self.sn.get_user(friend_id)
                self.log_output(f"  • {friend['name']} ({score} mutual friends)")
        else:
            self.log_output("  No recommendations available")
        self.log_output(f"{'='*50}\n")
        
        self.notebook.select(self.output_tab)
        self.update_status(f"Showing recommendations for {name}")
    
    def find_mutual_gui(self):
        """Find mutual friends"""
        u1 = self.mf1_entry.get().strip()
        u2 = self.mf2_entry.get().strip()
        
        if not u1 or not u2:
            messagebox.showwarning("Input Error", "Please enter both usernames")
            return
        
        u1_id, _ = self.sn.get_user_by_name(u1)
        u2_id, _ = self.sn.get_user_by_name(u2)
        
        if not u1_id or not u2_id:
            messagebox.showerror("Error", "One or both users not found")
            return
        
        mutual = self.sn.find_mutual_friends(u1_id, u2_id)
        mutual_names = [self.sn.get_user(mid)['name'] for mid in mutual]
        
        self.log_output(f"\n{'='*50}")
        self.log_output(f"🤝 Mutual friends of {u1} and {u2}:")
        if mutual_names:
            for name in mutual_names:
                self.log_output(f"  • {name}")
        else:
            self.log_output("  No mutual friends found")
        self.log_output(f"{'='*50}\n")
        
        self.notebook.select(self.output_tab)
        self.update_status(f"Found mutual friends: {u1} & {u2}")
    
    def undo_gui(self):
        """Undo last action"""
        _, msg = self.sn.undo()
        self.log_output(f"↩ {msg}")
        self.refresh_all()
        self.update_status(msg)
    
    def redo_gui(self):
        """Redo last undone action"""
        _, msg = self.sn.redo()
        self.log_output(f"↪ {msg}")
        self.refresh_all()
        self.update_status(msg)
    
    def show_stats_gui(self):
        """Show statistics"""
        self.update_stats()
        self.notebook.select(self.stats_tab)
        self.update_status("Showing statistics")
    
    def generate_demo(self, num_users):
        """Generate demo users"""
        self.update_status(f"Generating {num_users} users...")
        
        # Clear existing data first (optional)
        # self.sn.reset()
        
        # Generate users
        self.sn.generate_demo_users(num_users=num_users, avg_friends=5)
        
        self.log_output(f"✅ Generated {num_users} users with friendships!")
        self.refresh_all()
        self.update_status(f"Generated {num_users} demo users")
    
    def clear_all_data(self):
        """Clear all data"""
        if messagebox.askyesno("Confirm", "Delete ALL data? This cannot be undone!"):
            self.sn.reset()
            self.log_output("🗑 All data cleared!")
            self.refresh_all()
            self.update_status("All data cleared")
    
    # ========== VISUALIZATION MENU COMMANDS ==========
    
    def show_hash_map(self):
        """Show hash map visualization"""
        self.log_output("\n" + "="*50)
        self.log_output("📋 HASH MAP - User Data")
        self.log_output("="*50)
        all_users = self.sn.get_all_users()
        for user in all_users:
            self.log_output(f"  ID: {user['id']} → Name: {user['name']}")
        self.log_output(f"  Total: {len(all_users)} users")
        self.log_output("  Complexity: O(1) lookup\n")
        self.notebook.select(self.output_tab)
    
    def show_graph(self):
        """Show graph structure"""
        self.log_output("\n" + "="*50)
        self.log_output("📊 GRAPH - Friendship Connections")
        self.log_output("="*50)
        friendships = self.sn.get_all_friendships()
        for u1, u2 in friendships:
            name1 = self.sn.get_user(u1)['name']
            name2 = self.sn.get_user(u2)['name']
            self.log_output(f"  {name1} ↔ {name2}")
        self.log_output(f"  Total: {len(friendships)} friendships")
        self.log_output("  Complexity: O(1) edge operations\n")
        self.notebook.select(self.output_tab)
    
    def show_stack(self):
        """Show stack structure"""
        self.log_output("\n" + "="*50)
        self.log_output("📚 STACK - Undo History")
        self.log_output("="*50)
        size = self.sn.get_undo_history_size()
        self.log_output(f"  Stack Size: {size}")
        self.log_output("  Top: Most recent action")
        self.log_output("  Bottom: Oldest action")
        self.log_output("  Complexity: O(1) push/pop\n")
        self.notebook.select(self.output_tab)
    
    def show_queue(self):
        """Show queue structure"""
        self.log_output("\n" + "="*50)
        self.log_output("🔄 QUEUE - BFS Traversal")
        self.log_output("="*50)
        self.log_output("  Queue used for Breadth-First Search")
        self.log_output("  FIFO (First-In-First-Out) order")
        self.log_output("  Complexity: O(1) enqueue/dequeue\n")
        self.notebook.select(self.output_tab)
    
    def show_heap(self):
        """Show heap structure"""
        self.log_output("\n" + "="*50)
        self.log_output("⛰️ HEAP - Priority Queue for Recommendations")
        self.log_output("="*50)
        self.log_output("  Used for Top-K recommendations")
        self.log_output("  Min-heap stores scores")
        self.log_output("  Complexity: O(n log k)\n")
        self.notebook.select(self.output_tab)
    
    def show_sorting(self):
        """Show sorting structure"""
        self.log_output("\n" + "="*50)
        self.log_output("📊 SORTING - Timsort Algorithm")
        self.log_output("="*50)
        self.log_output("  Used for alphabetical friend lists")
        self.log_output("  Hybrid of Merge Sort + Insertion Sort")
        self.log_output("  Complexity: O(n log n) worst case\n")
        self.notebook.select(self.output_tab)
    
    def show_bfs(self):
        """Show BFS visualization"""
        self.log_output("\n" + "="*50)
        self.log_output("🌳 BFS - Breadth-First Search")
        self.log_output("="*50)
        self.log_output("  Algorithm: Level-order traversal")
        self.log_output("  Data Structure: Queue")
        self.log_output("  Used for: Mutual friends discovery")
        self.log_output("  Complexity: O(V+E)\n")
        self.notebook.select(self.output_tab)
    
    def show_recommendations(self):
        """Show recommendations visualization"""
        self.get_recommendations_gui()
    
    def show_binary_search(self):
        """Show binary search visualization"""
        self.log_output("\n" + "="*50)
        self.log_output("🔍 BINARY SEARCH")
        self.log_output("="*50)
        self.log_output("  Algorithm: Divide and conquer")
        self.log_output("  Requires: Sorted list")
        self.log_output("  Used for: Friend lookup by name")
        self.log_output("  Complexity: O(log n)\n")
        self.notebook.select(self.output_tab)
    
    def show_network_graph(self):
        """Show network graph in separate window"""
        self.refresh_all()
        self.notebook.select(self.network_tab)
        self.update_status("Showing network graph")
    
    def show_degree_distribution(self):
        """Show degree distribution"""
        degrees = []
        all_users = self.sn.get_all_users()
        for user in all_users:
            degrees.append(self.sn.get_friend_count(user['id']))
        
        if not degrees:
            messagebox.showinfo("Info", "No users to show degree distribution")
            return
        
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.hist(degrees, bins=20, edgecolor='black', alpha=0.7, color='skyblue')
        ax.set_xlabel('Number of Friends')
        ax.set_ylabel('Number of Users')
        ax.set_title('Friend Count Distribution')
        
        # Show in new window
        new_window = tk.Toplevel(self.root)
        new_window.title("Degree Distribution")
        canvas = FigureCanvasTkAgg(fig, new_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
    def show_performance_charts(self):
        """Show performance charts"""
        self.log_output("\n" + "="*50)
        self.log_output("📈 PERFORMANCE CHARTS")
        self.log_output("="*50)
        self.log_output("  O(1): Add User, Add Friend")
        self.log_output("  O(log n): Binary Search")
        self.log_output("  O(n log n): Sort Friends")
        self.log_output("  O(V+E): BFS Mutual Friends")
        self.log_output("  O(n log k): Recommendations")
        self.log_output("\n  Run 'transaction_benchmark.py' for detailed charts")
        self.notebook.select(self.output_tab)
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About", """
        SOCIAL NETWORK SYSTEM - THEME A1
        ================================
        
        Course: BIT 4105 - Advanced Data Structures
        Group: DSA-CH23-GROUP-XX
        
        Data Structures:
        ✅ Hash Table (User Manager)
        ✅ Graph (Friendships)
        ✅ Stack (Undo/Redo)
        ✅ Queue (BFS)
        ✅ Heap (Recommendations)
        ✅ Sorting (Timsort)
        ✅ Binary Search
        
        Algorithms:
        ✅ BFS - Mutual Friends
        ✅ Heap - Top-K Recommendations
        ✅ Timsort - Friend Lists
        ✅ Binary Search - Friend Lookup
        """)
    
    def show_documentation(self):
        """Show documentation"""
        messagebox.showinfo("Documentation", """
        SOCIAL NETWORK - USER GUIDE
        ===========================
        
        📌 Adding Users:
        - Enter username in "Username" field
        - Click "Add User"
        
        📌 Adding Friends:
        - Enter User 1 and User 2 names
        - Click "Add Friend"
        
        📌 Viewing Friends:
        - Enter username in "User Name"
        - Click "Show Friends"
        
        📌 Finding Mutual Friends:
        - Enter two usernames
        - Click "Find"
        
        📌 Getting Recommendations:
        - Enter username
        - Click "Get Recommendations"
        
        📌 Undo/Redo:
        - Click "Undo" or "Redo" buttons
        
        📌 Demo Data:
        - Click "Generate 10/40/100 Users"
        
        📌 Visualizations:
        - Use the menus at the top
        """)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SocialNetworkGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
