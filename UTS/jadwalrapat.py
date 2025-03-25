import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import json
import os
from tkcalendar import Calendar

class Meeting:
    def __init__(self, title, start_time, end_time, teams, room):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.teams = teams  # List of team IDs
        self.room = room
    
    def to_dict(self):
        return {
            'title': self.title,
            'start_time': self.start_time.strftime('%H:%M'),
            'end_time': self.end_time.strftime('%H:%M'),
            'teams': self.teams,
            'room': self.room
        }
    
    @classmethod
    def from_dict(cls, data):
        start_time = datetime.datetime.strptime(data['start_time'], '%H:%M').time()
        end_time = datetime.datetime.strptime(data['end_time'], '%H:%M').time()
        return cls(data['title'], start_time, end_time, data['teams'], data['room'])

class Team:
    def __init__(self, id, name, available_times):
        self.id = id
        self.name = name
        self.available_times = available_times  # List of (start_time, end_time) tuples
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'available_times': [(t[0].strftime('%H:%M'), t[1].strftime('%H:%M')) for t in self.available_times]
        }
    
    @classmethod
    def from_dict(cls, data):
        available_times = [(datetime.datetime.strptime(t[0], '%H:%M').time(), 
                           datetime.datetime.strptime(t[1], '%H:%M').time()) 
                          for t in data['available_times']]
        return cls(data['id'], data['name'], available_times)

class Room:
    def __init__(self, id, name, capacity):
        self.id = id
        self.name = name
        self.capacity = capacity
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'capacity': self.capacity
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['id'], data['name'], data['capacity'])

class MeetingScheduler:
    def __init__(self):
        self.meetings = []
        self.teams = []
        self.rooms = []
        self.selected_date = datetime.date.today()
        
        # Load data if exists
        self.data_file = "meeting_data.json"
        self.load_data()
        
        self.setup_gui()
    
    def save_data(self):
        data = {
            'meetings': {self.selected_date.strftime('%Y-%m-%d'): [m.to_dict() for m in self.meetings]},
            'teams': [t.to_dict() for t in self.teams],
            'rooms': [r.to_dict() for r in self.rooms]
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                # Load teams
                self.teams = [Team.from_dict(t) for t in data.get('teams', [])]
                
                # Load rooms
                self.rooms = [Room.from_dict(r) for r in data.get('rooms', [])]
                
                # Load meetings for selected date
                date_str = self.selected_date.strftime('%Y-%m-%d')
                if 'meetings' in data and date_str in data['meetings']:
                    self.meetings = [Meeting.from_dict(m) for m in data['meetings'][date_str]]
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {str(e)}")
                self.initialize_sample_data()
        else:
            self.initialize_sample_data()
    
    def initialize_sample_data(self):
        # Sample teams
        team1 = Team(1, "Tim Pengembangan", [
            (datetime.time(9, 0), datetime.time(12, 0)),
            (datetime.time(14, 0), datetime.time(17, 0))
        ])
        team2 = Team(2, "Tim Pemasaran", [
            (datetime.time(10, 0), datetime.time(15, 0))
        ])
        team3 = Team(3, "Tim Keuangan", [
            (datetime.time(8, 0), datetime.time(11, 0)),
            (datetime.time(13, 0), datetime.time(16, 0))
        ])
        
        self.teams = [team1, team2, team3]
        
        # Sample rooms
        room1 = Room(1, "Ruang Rapat A", 10)
        room2 = Room(2, "Ruang Rapat B", 5)
        room3 = Room(3, "Ruang Konferensi", 20)
        
        self.rooms = [room1, room2, room3]
    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Sistem Penjadwalan Rapat")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Configure the grid
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(0, weight=1)
        
        # Create frames
        self.sidebar_frame = ttk.Frame(self.root, padding=10)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        
        # Setup the sidebar
        self.setup_sidebar()
        
        # Setup the main content
        self.setup_main_content()
        
        # Tambahkan tombol hapus di bawah daftar rapat
        self.delete_button = ttk.Button(self.main_frame, text="Hapus Rapat", command=self.delete_selected_meeting)
        self.delete_button.pack(pady=10)

        
        # Refresh the displayed data
        self.refresh_schedule_view()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def setup_sidebar(self):
        # Calendar for date selection
        ttk.Label(self.sidebar_frame, text="Pilih Tanggal:").pack(pady=(0, 5), anchor="w")
        self.calendar = Calendar(self.sidebar_frame, selectmode="day", 
                               year=self.selected_date.year, 
                               month=self.selected_date.month,
                               day=self.selected_date.day)
        self.calendar.pack(fill="x", pady=(0, 10))
        
        # Button to load schedule for selected date
        ttk.Button(self.sidebar_frame, text="Muat Jadwal", 
                 command=self.load_selected_date).pack(fill="x", pady=(0, 20))
        
        # Management section
        manage_frame = ttk.LabelFrame(self.sidebar_frame, text="Manajemen")
        manage_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(manage_frame, text="Tambah Rapat", 
                 command=self.add_meeting_dialog).pack(fill="x", pady=5)
        
        ttk.Button(manage_frame, text="Kelola Tim", 
                 command=self.manage_teams).pack(fill="x", pady=5)
        
        ttk.Button(manage_frame, text="Kelola Ruangan", 
                 command=self.manage_rooms).pack(fill="x", pady=5)
        
        # Tools section
        tools_frame = ttk.LabelFrame(self.sidebar_frame, text="Alat")
        tools_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(tools_frame, text="Verifikasi Jadwal", 
                 command=self.verify_schedule).pack(fill="x", pady=5)
        
        ttk.Button(tools_frame, text="Jadwal Otomatis", 
                 command=self.auto_schedule).pack(fill="x", pady=5)
        
        ttk.Button(tools_frame, text="Ekspor Jadwal", 
                 command=self.export_schedule).pack(fill="x", pady=5)
    
    def setup_main_content(self):
        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        self.date_label = ttk.Label(header_frame, text=f"Jadwal Rapat: {self.selected_date.strftime('%d %B %Y')}", 
                                 font=("Arial", 14, "bold"))
        self.date_label.pack(side="left")
        
        # Schedule view (Treeview)
        self.setup_schedule_treeview()
        
        # Timeline view
        self.setup_timeline_view()
    
    def setup_schedule_treeview(self):
        frame = ttk.LabelFrame(self.main_frame, text="Daftar Rapat")
        frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Setup treeview with scrollbar
        self.tree_scroll = ttk.Scrollbar(frame)
        self.tree_scroll.pack(side="right", fill="y")
        
        self.schedule_tree = ttk.Treeview(frame, 
                                        columns=("Waktu", "Judul", "Tim", "Ruangan", "Durasi"), 
                                        show="headings",
                                        yscrollcommand=self.tree_scroll.set)
        
        self.schedule_tree.heading("Waktu", text="Waktu")
        self.schedule_tree.heading("Judul", text="Judul Rapat")
        self.schedule_tree.heading("Tim", text="Tim")
        self.schedule_tree.heading("Ruangan", text="Ruangan")
        self.schedule_tree.heading("Durasi", text="Durasi")
        
        self.schedule_tree.column("Waktu", width=120)
        self.schedule_tree.column("Judul", width=200)
        self.schedule_tree.column("Tim", width=200)
        self.schedule_tree.column("Ruangan", width=100)
        self.schedule_tree.column("Durasi", width=80)
        
        self.schedule_tree.pack(fill="both", expand=True)
        self.tree_scroll.config(command=self.schedule_tree.yview)
        
        # Bind the double-click event to edit meeting
        self.schedule_tree.bind("<Double-1>", self.edit_meeting)
        
        # Context menu
        self.tree_context_menu = tk.Menu(self.root, tearoff=0)
        self.tree_context_menu.add_command(label="Edit", command=self.edit_selected_meeting)
        self.tree_context_menu.add_command(label="Hapus", command=self.delete_selected_meeting)
        
        self.schedule_tree.bind("<Button-3>", self.show_context_menu)
    
    def setup_timeline_view(self):
        self.timeline_frame = ttk.LabelFrame(self.main_frame, text="Timeline Rapat")
        self.timeline_frame.pack(fill="both", expand=True)
        
        # Canvas for timeline
        self.timeline_canvas = tk.Canvas(self.timeline_frame, bg="white")
        self.timeline_canvas.pack(fill="both", expand=True, padx=5, pady=5)
    
    def refresh_schedule_view(self):
        # Update date label
        self.date_label.config(text=f"Jadwal Rapat: {self.selected_date.strftime('%d %B %Y')}")
        
        # Clear current entries
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)
        
        # Sort meetings by start time
        sorted_meetings = sorted(self.meetings, key=lambda m: m.start_time)
        
        # Add meetings to treeview
        for meeting in sorted_meetings:
            team_names = [self.get_team_name(team_id) for team_id in meeting.teams]
            room_name = self.get_room_name(meeting.room)
            
            # Calculate duration in minutes
            start_minutes = meeting.start_time.hour * 60 + meeting.start_time.minute
            end_minutes = meeting.end_time.hour * 60 + meeting.end_time.minute
            duration = end_minutes - start_minutes
            
            self.schedule_tree.insert("", "end", 
                                  values=(f"{meeting.start_time.strftime('%H:%M')} - {meeting.end_time.strftime('%H:%M')}",
                                         meeting.title,
                                         ", ".join(team_names),
                                         room_name,
                                         f"{duration} menit"))
        
        # Refresh timeline view
        self.draw_timeline()
    
    def draw_timeline(self):
        # Clear canvas
        self.timeline_canvas.delete("all")
        
        # Draw timeline from 8:00 to 18:00
        canvas_width = self.timeline_canvas.winfo_width() or 800
        canvas_height = self.timeline_canvas.winfo_height() or 400
        
        # Hours in the day (8:00 - 18:00)
        hours = list(range(8, 19))
        hour_width = canvas_width / (len(hours) - 1)
        
        # Draw time axis
        y_axis = canvas_height - 30
        self.timeline_canvas.create_line(50, y_axis, canvas_width - 50, y_axis, width=2)
        
        # Draw hour marks and labels
        for i, hour in enumerate(hours):
            x = 50 + i * hour_width
            self.timeline_canvas.create_line(x, y_axis - 5, x, y_axis + 5, width=2)
            self.timeline_canvas.create_text(x, y_axis + 15, text=f"{hour}:00")
        
        # Get room count for spacing
        room_count = len(self.rooms)
        room_height = (y_axis - 50) / (room_count if room_count > 0 else 1)
        
        # Draw room labels
        for i, room in enumerate(self.rooms):
            y = 50 + i * room_height
            self.timeline_canvas.create_text(25, y + room_height/2, text=room.name, anchor="e")
            
            # Draw room separator lines
            self.timeline_canvas.create_line(50, y, canvas_width - 50, y, fill="lightgray", dash=(4, 2))
        
        # Draw meetings as rectangles
        minutes_in_day = (hours[-1] - hours[0]) * 60
        pixel_per_minute = (canvas_width - 100) / minutes_in_day
        
        colors = ["#FFD700", "#FF6347", "#9370DB", "#20B2AA", "#3CB371", "#FF7F50"]
        
        for i, meeting in enumerate(self.meetings):
            room_index = next((i for i, r in enumerate(self.rooms) if r.id == meeting.room), 0)
            
            start_min = (meeting.start_time.hour - hours[0]) * 60 + meeting.start_time.minute
            end_min = (meeting.end_time.hour - hours[0]) * 60 + meeting.end_time.minute
            
            x1 = 50 + start_min * pixel_per_minute
            y1 = 50 + room_index * room_height + 5
            x2 = 50 + end_min * pixel_per_minute
            y2 = 50 + (room_index + 1) * room_height - 5
            
            color_index = i % len(colors)
            
            # Draw meeting rectangle
            meeting_id = self.timeline_canvas.create_rectangle(x1, y1, x2, y2, 
                                                           fill=colors[color_index], 
                                                           outline="black",
                                                           width=1)
            
            # Draw meeting title
            text_x = (x1 + x2) / 2
            text_y = (y1 + y2) / 2
            self.timeline_canvas.create_text(text_x, text_y, text=meeting.title, anchor="center")
            
            # Bind click event
            self.timeline_canvas.tag_bind(meeting_id, "<Button-1>", 
                                       lambda e, m=meeting: self.show_meeting_details(m))
    
    def load_selected_date(self):
        date_str = self.calendar.get_date()
        self.selected_date = datetime.datetime.strptime(date_str, "%m/%d/%y").date()
        self.load_data()  # Reload data for the selected date
        self.refresh_schedule_view()
    
    def add_meeting_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Tambah Rapat Baru")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text="Judul Rapat:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Waktu Mulai:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        start_hour = ttk.Spinbox(dialog, from_=8, to=17, width=5)
        start_hour.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        ttk.Label(dialog, text=":").grid(row=1, column=1, padx=(60, 0), pady=5)
        start_minute = ttk.Spinbox(dialog, from_=0, to=59, width=5)
        start_minute.grid(row=1, column=1, padx=(70, 0), sticky="w", pady=5)
        
        ttk.Label(dialog, text="Waktu Selesai:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        end_hour = ttk.Spinbox(dialog, from_=9, to=18, width=5)
        end_hour.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        ttk.Label(dialog, text=":").grid(row=2, column=1, padx=(60, 0), pady=5)
        end_minute = ttk.Spinbox(dialog, from_=0, to=59, width=5)
        end_minute.grid(row=2, column=1, padx=(70, 0), sticky="w", pady=5)
        
        ttk.Label(dialog, text="Ruangan:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        room_var = tk.StringVar()
        room_combo = ttk.Combobox(dialog, textvariable=room_var, width=38)
        room_combo['values'] = [f"{room.name} (Kapasitas: {room.capacity})" for room in self.rooms]
        room_combo.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        
        # Team selection (multiple)
        ttk.Label(dialog, text="Tim:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        
        team_frame = ttk.Frame(dialog)
        team_frame.grid(row=4, column=1, sticky="w", padx=10, pady=5)
        
        team_vars = []
        for i, team in enumerate(self.teams):
            var = tk.BooleanVar()
            team_vars.append(var)
            ttk.Checkbutton(team_frame, text=team.name, variable=var).grid(row=i, column=0, sticky="w")
        
        # Availability information
        ttk.Label(dialog, text="Ketersediaan Tim:", font=("Arial", 10, "bold")).grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=(20, 5))
        
        availability_text = tk.Text(dialog, height=10, width=50)
        availability_text.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
        
        # Show availability information
        availability_info = "Informasi Ketersediaan Tim:\n\n"
        for team in self.teams:
            availability_info += f"{team.name}:\n"
            for time_slot in team.available_times:
                availability_info += f"  {time_slot[0].strftime('%H:%M')} - {time_slot[1].strftime('%H:%M')}\n"
            availability_info += "\n"
        
        availability_text.insert(tk.END, availability_info)
        availability_text.config(state="disabled")
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Batalkan", 
                 command=dialog.destroy).grid(row=0, column=0, padx=10)
        
        def save_meeting():
            # Validate inputs
            if not title_entry.get().strip():
                messagebox.showerror("Error", "Judul rapat tidak boleh kosong")
                return
            
            try:
                start = datetime.time(int(start_hour.get()), int(start_minute.get()))
                end = datetime.time(int(end_hour.get()), int(end_minute.get()))
                
                if start >= end:
                    messagebox.showerror("Error", "Waktu selesai harus setelah waktu mulai")
                    return
            except ValueError:
                messagebox.showerror("Error", "Format waktu tidak valid")
                return
            
            if not room_var.get():
                messagebox.showerror("Error", "Silakan pilih ruangan")
                return
            
            selected_teams = [self.teams[i].id for i, var in enumerate(team_vars) if var.get()]
            if not selected_teams:
                messagebox.showerror("Error", "Silakan pilih minimal satu tim")
                return
            
            # Get room ID from selection
            room_name = room_var.get().split(" (")[0]
            room_id = next((room.id for room in self.rooms if room.name == room_name), None)
            
            # Create new meeting
            new_meeting = Meeting(
                title=title_entry.get().strip(),
                start_time=start,
                end_time=end,
                teams=selected_teams,
                room=room_id
            )
            
            # Add meeting and save
            self.meetings.append(new_meeting)
            self.save_data()
            self.refresh_schedule_view()
            dialog.destroy()
            
            messagebox.showinfo("Sukses", "Rapat berhasil ditambahkan ke jadwal")
        
        ttk.Button(button_frame, text="Simpan", 
                 command=save_meeting).grid(row=0, column=1, padx=10)
        
    def find_available_room(self, start_time, end_time, exclude_meeting=None):
        """Find an available room for the given time slot"""
        for room in self.rooms:
            is_available = True
            for meeting in self.meetings:
                if exclude_meeting and meeting == exclude_meeting:
                    continue
                if meeting.room == room.id:
                    if (start_time < meeting.end_time and end_time > meeting.start_time):
                        is_available = False
                        break
            if is_available:
                return room.id
        return None
    
    def check_meeting_conflicts(self, new_meeting, exclude_meeting=None):
        for meeting in self.meetings:
            if exclude_meeting and meeting == exclude_meeting:
                continue
            
            if meeting.room == new_meeting.room:
                if (new_meeting.start_time < meeting.end_time and 
                    new_meeting.end_time > meeting.start_time):
                    messagebox.showwarning("Konflik Jadwal", 
                        f"Rapat '{new_meeting.title}' bentrok dengan '{meeting.title}'. Gunakan 'Jadwal Otomatis' untuk mencari solusi.")
        
        # Check team availability conflicts
        for team_id in new_meeting.teams:
            team = next((t for t in self.teams if t.id == team_id), None)
            if team:
                is_available = False
                for time_slot in team.available_times:
                    if (new_meeting.start_time >= time_slot[0] and 
                        new_meeting.end_time <= time_slot[1]):
                        is_available = True
                        break
                
                if not is_available:
                    messagebox.showerror("Konflik Ketersediaan", 
                                     f"Tim {team.name} tidak tersedia pada waktu yang dipilih.")
                    return True
        
        # Check team schedule conflicts
        for team_id in new_meeting.teams:
            for meeting in self.meetings:
                # Skip the meeting being edited
                if exclude_meeting and meeting == exclude_meeting:
                    continue
                    
                if team_id in meeting.teams:
                    # Check if times overlap
                    if (new_meeting.start_time < meeting.end_time and 
                        new_meeting.end_time > meeting.start_time):
                        messagebox.showerror("Konflik Tim", 
                                         f"Tim {self.get_team_name(team_id)} sudah memiliki rapat '{meeting.title}' pada waktu yang sama.")
                        return True
        
        return False
    
    def edit_meeting(self, event):
        """Edit meeting on double-click"""
        selected_item = self.schedule_tree.selection()
        if not selected_item:
            return
        
        # Get the meeting index based on the selected row
        meeting_index = self.schedule_tree.index(selected_item[0])
        if meeting_index < len(self.meetings):
            meeting = sorted(self.meetings, key=lambda m: m.start_time)[meeting_index]
            self.edit_meeting_dialog(meeting)
    
    def edit_selected_meeting(self):
        """Edit meeting from context menu"""
        selected_item = self.schedule_tree.selection()
        if not selected_item:
            return
        
        # Get the meeting index based on the selected row
        meeting_index = self.schedule_tree.index(selected_item[0])
        if meeting_index < len(self.meetings):
            meeting = sorted(self.meetings, key=lambda m: m.start_time)[meeting_index]
            self.edit_meeting_dialog(meeting)
    
    def delete_selected_meeting(self):
        """Delete meeting from context menu"""
        selected_item = self.schedule_tree.selection()
        if not selected_item:
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus rapat ini?"):
            return
        
        
        # Dapatkan indeks rapat berdasarkan item yang dipilih
        meeting_index = self.schedule_tree.index(selected_item[0])
        if meeting_index < len(self.meetings):
            meeting = sorted(self.meetings, key=lambda m: m.start_time)[meeting_index]
            self.meetings.remove(meeting)
            self.save_data()
            self.refresh_schedule_view()

            messagebox.showinfo("Sukses", "Rapat berhasil dihapus.")
        
        
        
        # Get the meeting index based on the selected row
        meeting_index = self.schedule_tree.index(selected_item[0])
        if meeting_index < len(self.meetings):
            meeting = sorted(self.meetings, key=lambda m: m.start_time)[meeting_index]
            self.meetings.remove(meeting)
            self.save_data()
            self.refresh_schedule_view()
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        selected_item = self.schedule_tree.identify_row(event.y)
        if selected_item:
            self.schedule_tree.selection_set(selected_item)
            self.tree_context_menu.post(event.x_root, event.y_root)
    
    def edit_meeting_dialog(self, meeting):
        """Open dialog to edit meeting"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Rapat")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text="Judul Rapat:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.insert(0, meeting.title)
        title_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Waktu Mulai:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        start_hour = ttk.Spinbox(dialog, from_=8, to=17, width=5)
        start_hour.insert(0, meeting.start_time.hour)
        start_hour.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        ttk.Label(dialog, text=":").grid(row=1, column=1, padx=(60, 0), pady=5)
        start_minute = ttk.Spinbox(dialog, from_=0, to=59, width=5)
        start_minute.insert(0, meeting.start_time.minute)
        start_minute.grid(row=1, column=1, padx=(70, 0), sticky="w", pady=5)
        
        ttk.Label(dialog, text="Waktu Selesai:").grid(row=2, column=0, sticky="w", padx=10, pady=5)

        end_hour = ttk.Spinbox(dialog, from_=9, to=18, width=5)
        end_hour.insert(0, meeting.end_time.hour)
        end_hour.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        ttk.Label(dialog, text=":").grid(row=2, column=2, pady=5)  # Kolom 2 untuk ":" agar tata letak lebih rapi

        end_minute = ttk.Spinbox(dialog, from_=0, to=59, width=5)
        end_minute.insert(0, meeting.end_time.minute)
        end_minute.grid(row=2, column=3, sticky="w", padx=10, pady=5)  # Kolom 3 agar tidak bertumpuk dengan `end_hour`

                
        ttk.Label(dialog, text="Ruangan:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        room_var = tk.StringVar()
        room_combo = ttk.Combobox(dialog, textvariable=room_var, width=38)
        room_combo['values'] = [f"{room.name} (Kapasitas: {room.capacity})" for room in self.rooms]
        room_combo.current(next((i for i, room in enumerate(self.rooms) if room.id == meeting.room), 0))
        room_combo.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        
        # Team selection (multiple)
        ttk.Label(dialog, text="Tim:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        
        team_frame = ttk.Frame(dialog)
        team_frame.grid(row=4, column=1, sticky="w", padx=10, pady=5)
        
        team_vars = []
        for i, team in enumerate(self.teams):
            var = tk.BooleanVar(value=team.id in meeting.teams)
            team_vars.append(var)
            ttk.Checkbutton(team_frame, text=team.name, variable=var).grid(row=i, column=0, sticky="w")
        
        # Availability information
        ttk.Label(dialog, text="Ketersediaan Tim:", font=("Arial", 10, "bold")).grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=(20, 5))
        
        availability_text = tk.Text(dialog, height=10, width=50)
        availability_text.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
        
        # Show availability information
        availability_info = "Informasi Ketersediaan Tim:\n\n"
        for team in self.teams:
            availability_info += f"{team.name}:\n"
            for time_slot in team.available_times:
                availability_info += f"  {time_slot[0].strftime('%H:%M')} - {time_slot[1].strftime('%H:%M')}\n"
            availability_info += "\n"
        
        availability_text.insert(tk.END, availability_info)
        availability_text.config(state="disabled")
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Batalkan", 
                 command=dialog.destroy).grid(row=0, column=0, padx=10)
        
        def update_meeting():
            # Validate inputs
            if not title_entry.get().strip():
                messagebox.showerror("Error", "Judul rapat tidak boleh kosong")
                return
            
            try:
                start = datetime.time(int(start_hour.get()), int(start_minute.get()))
                end = datetime.time(int(end_hour.get()), int(end_minute.get()))
                
                if start >= end:
                    messagebox.showerror("Error", "Waktu selesai harus setelah waktu mulai")
                    return
            except ValueError:
                messagebox.showerror("Error", "Format waktu tidak valid")
                return
            
            if not room_var.get():
                messagebox.showerror("Error", "Silakan pilih ruangan")
                return
            
            selected_teams = [self.teams[i].id for i, var in enumerate(team_vars) if var.get()]
            if not selected_teams:
                messagebox.showerror("Error", "Silakan pilih minimal satu tim")
                return
            
            # Get room ID from selection
            room_name = room_var.get().split(" (")[0]
            room_id = next((room.id for room in self.rooms if room.name == room_name), None)
            
            # Create updated meeting
            updated_meeting = Meeting(
                title=title_entry.get().strip(),
                start_time=start,
                end_time=end,
                teams=selected_teams,
                room=room_id
            )
            
            # Check for conflicts (excluding the current meeting)
            if self.check_meeting_conflicts(updated_meeting, exclude_meeting=meeting):
                return
            
            # Update meeting attributes
            meeting.title = updated_meeting.title
            meeting.start_time = updated_meeting.start_time
            meeting.end_time = updated_meeting.end_time
            meeting.teams = updated_meeting.teams
            meeting.room = updated_meeting.room
            
            # Save and refresh
            self.save_data()
            self.refresh_schedule_view()
            dialog.destroy()
            
            messagebox.showinfo("Sukses", "Rapat berhasil diperbarui")
        
        ttk.Button(button_frame, text="Simpan", 
                 command=update_meeting).grid(row=0, column=1, padx=10)
    
    def show_meeting_details(self, meeting):
        """Show meeting details in a popup"""
        details = tk.Toplevel(self.root)
        details.title("Detail Rapat")
        details.geometry("400x300")
        details.transient(self.root)
        
        # Meeting info
        ttk.Label(details, text="Detail Rapat", font=("Arial", 12, "bold")).pack(pady=(10, 20))
        
        info_frame = ttk.Frame(details)
        info_frame.pack(fill="both", expand=True, padx=20)
        
        ttk.Label(info_frame, text="Judul:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        ttk.Label(info_frame, text=meeting.title).grid(row=0, column=1, sticky="w", pady=5)
        
        ttk.Label(info_frame, text="Waktu:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        ttk.Label(info_frame, text=f"{meeting.start_time.strftime('%H:%M')} - {meeting.end_time.strftime('%H:%M')}").grid(row=1, column=1, sticky="w", pady=5)
        
        ttk.Label(info_frame, text="Ruangan:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        ttk.Label(info_frame, text=self.get_room_name(meeting.room)).grid(row=2, column=1, sticky="w", pady=5)
        
        ttk.Label(info_frame, text="Tim:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="nw", pady=5)
        team_names = [self.get_team_name(team_id) for team_id in meeting.teams]
        ttk.Label(info_frame, text="\n".join(team_names)).grid(row=3, column=1, sticky="w", pady=5)
        
        # Buttons
        button_frame = ttk.Frame(details)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Tutup", command=details.destroy).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Edit", command=lambda: [details.destroy(), self.edit_meeting_dialog(meeting)]).grid(row=0, column=1, padx=10)
    
    def manage_teams(self):
        """Open dialog to manage teams"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Kelola Tim")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Team list (left side)
        list_frame = ttk.Frame(dialog)
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ttk.Label(list_frame, text="Daftar Tim", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 10))
        
        # Treeview for teams
        team_tree_scroll = ttk.Scrollbar(list_frame)
        team_tree_scroll.pack(side="right", fill="y")
        
        team_tree = ttk.Treeview(list_frame, columns=("ID", "Nama"), show="headings", 
                                yscrollcommand=team_tree_scroll.set)
        team_tree.heading("ID", text="ID")
        team_tree.heading("Nama", text="Nama Tim")
        
        team_tree.column("ID", width=50)
        team_tree.column("Nama", width=200)
        
        team_tree.pack(fill="both", expand=True)
        team_tree_scroll.config(command=team_tree.yview)
        
        # Buttons for team management
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill="x", pady=10)
        
        ttk.Button(button_frame, text="Tambah Tim", 
                 command=lambda: self.add_team_dialog(dialog, team_tree)).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Edit Tim", 
                 command=lambda: self.edit_team_dialog(dialog, team_tree)).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Hapus Tim", 
                 command=lambda: self.delete_team(team_tree)).pack(side="left", padx=5)
        
        # Right side (team details)
        detail_frame = ttk.LabelFrame(dialog, text="Detail Ketersediaan")
        detail_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        detail_text = tk.Text(detail_frame, width=30, height=20)
        detail_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Populate team list
        self.refresh_team_list(team_tree)
        
        # Bind selection event
        def on_team_select(event):
            selected = team_tree.selection()
            if selected:
                team_id = team_tree.item(selected[0])['values'][0]
                team = next((t for t in self.teams if t.id == team_id), None)
                if team:
                    detail_text.config(state="normal")
                    detail_text.delete(1.0, tk.END)
                    
                    detail_text.insert(tk.END, f"Tim: {team.name}\n\n")
                    detail_text.insert(tk.END, "Waktu Ketersediaan:\n")
                    
                    for i, time_slot in enumerate(team.available_times):
                        detail_text.insert(tk.END, f"{i+1}. {time_slot[0].strftime('%H:%M')} - {time_slot[1].strftime('%H:%M')}\n")
                    
                    detail_text.config(state="disabled")
        
        team_tree.bind("<<TreeviewSelect>>", on_team_select)
    
    def refresh_team_list(self, tree):
        """Refresh team list in treeview"""
        # Clear current entries
        for item in tree.get_children():
            tree.delete(item)
        
        # Add teams to treeview
        for team in self.teams:
            tree.insert("", "end", values=(team.id, team.name))
    
    def add_team_dialog(self, parent, tree):
        """Dialog to add a new team"""
        dialog = tk.Toplevel(parent)
        dialog.title("Tambah Tim Baru")
        dialog.geometry("500x400")
        dialog.transient(parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Nama Tim:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        # Frame for time slots
        ttk.Label(dialog, text="Waktu Ketersediaan:", font=("Arial", 10, "bold")).grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(20, 5))
        
        slots_frame = ttk.Frame(dialog)
        slots_frame.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        
        time_slots = []
        
        def add_time_slot_row():
            slot_index = len(time_slots)
            slot_frame = ttk.Frame(slots_frame)
            slot_frame.grid(row=slot_index, column=0, sticky="w", pady=2)
            
            start_hour = ttk.Spinbox(slot_frame, from_=8, to=17, width=5)
            start_hour.grid(row=0, column=0)
            ttk.Label(slot_frame, text=":").grid(row=0, column=1)
            start_minute = ttk.Spinbox(slot_frame, from_=0, to=59, width=5)
            start_minute.grid(row=0, column=2)
            
            ttk.Label(slot_frame, text=" - ").grid(row=0, column=3)
            
            end_hour = ttk.Spinbox(slot_frame, from_=9, to=18, width=5)
            end_hour.grid(row=0, column=4)
            ttk.Label(slot_frame, text=":").grid(row=0, column=5)
            end_minute = ttk.Spinbox(slot_frame, from_=0, to=59, width=5)
            end_minute.grid(row=0, column=6)
            
            ttk.Button(slot_frame, text="Hapus", width=5,
                     command=lambda: [slot_frame.destroy(), time_slots.remove(slot_entry)]).grid(row=0, column=7, padx=5)
            
            slot_entry = {
                'frame': slot_frame,
                'start_hour': start_hour,
                'start_minute': start_minute,
                'end_hour': end_hour,
                'end_minute': end_minute
            }
            
            time_slots.append(slot_entry)
        
        # Add initial time slot
        add_time_slot_row()
        
        ttk.Button(slots_frame, text="Tambah Slot Waktu", 
                 command=add_time_slot_row).grid(row=100, column=0, sticky="w", pady=10)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Batalkan", 
                 command=dialog.destroy).grid(row=0, column=0, padx=10)
        
        def save_team():
            # Validate inputs
            if not name_entry.get().strip():
                messagebox.showerror("Error", "Nama tim tidak boleh kosong")
                return
            
            # Get next available ID
            next_id = max([team.id for team in self.teams], default=0) + 1
            
            # Parse time slots
            availability = []
            for slot in time_slots:
                try:
                    start = datetime.time(int(slot['start_hour'].get()), int(slot['start_minute'].get()))
                    end = datetime.time(int(slot['end_hour'].get()), int(slot['end_minute'].get()))
                    
                    if start >= end:
                        messagebox.showerror("Error", "Waktu selesai harus setelah waktu mulai")
                        return
                    
                    availability.append((start, end))
                except ValueError:
                    messagebox.showerror("Error", "Format waktu tidak valid")
                    return
            
            if not availability:
                messagebox.showerror("Error", "Minimal satu slot waktu harus ditambahkan")
                return
            
            # Create new team
            new_team = Team(
                id=next_id,
                name=name_entry.get().strip(),
                available_times=availability
            )
            
            # Add team and save
            self.teams.append(new_team)
            self.save_data()
            self.refresh_team_list(tree)
            dialog.destroy()
            
            messagebox.showinfo("Sukses", "Tim berhasil ditambahkan")
        
        ttk.Button(button_frame, text="Simpan", 
                 command=save_team).grid(row=0, column=1, padx=10)
    
    def edit_team_dialog(self, parent, tree):
        """Dialog to edit an existing team"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Perhatian", "Silakan pilih tim terlebih dahulu")
            return
        
        team_id = tree.item(selected[0])['values'][0]
        team = next((t for t in self.teams if t.id == team_id), None)
        
        if not team:
            return
        
        dialog = tk.Toplevel(parent)
        dialog.title(f"Edit Tim: {team.name}")
        dialog.geometry("500x400")
        dialog.transient(parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Nama Tim:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.insert(0, team.name)
        name_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        # Frame for time slots
        ttk.Label(dialog, text="Waktu Ketersediaan:", font=("Arial", 10, "bold")).grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(20, 5))
        
        slots_frame = ttk.Frame(dialog)
        slots_frame.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        
        time_slots = []
        
        def add_time_slot_row(start_time=None, end_time=None):
            slot_index = len(time_slots)
            slot_frame = ttk.Frame(slots_frame)
            slot_frame.grid(row=slot_index, column=0, sticky="w", pady=2)
            
            start_hour = ttk.Spinbox(slot_frame, from_=8, to=17, width=5)
            if start_time:
                start_hour.insert(0, start_time.hour)
            start_hour.grid(row=0, column=0)
            
            ttk.Label(slot_frame, text=":").grid(row=0, column=1)
            
            start_minute = ttk.Spinbox(slot_frame, from_=0, to=59, width=5)
            if start_time:
                start_minute.insert(0, start_time.minute)
            start_minute.grid(row=0, column=2)
            
            ttk.Label(slot_frame, text=" - ").grid(row=0, column=3)
            
            end_hour = ttk.Spinbox(slot_frame, from_=9, to=18, width=5)
            if end_time:
                end_hour.insert(0, end_time.hour)
            end_hour.grid(row=0, column=4)
            
            ttk.Label(slot_frame, text=":").grid(row=0, column=5)
            
            end_minute = ttk.Spinbox(slot_frame, from_=0, to=59, width=5)
            if end_time:
                end_minute.insert(0, end_time.minute)
            end_minute.grid(row=0, column=6)
            
            ttk.Button(slot_frame, text="Hapus", width=5,
                     command=lambda: [slot_frame.destroy(), time_slots.remove(slot_entry)]).grid(row=0, column=7, padx=5)
            
            slot_entry = {
                'frame': slot_frame,
                'start_hour': start_hour,
                'start_minute': start_minute,
                'end_hour': end_hour,
                'end_minute': end_minute
            }
            
            time_slots.append(slot_entry)
        
        # Add existing time slots
        for time_slot in team.available_times:
            add_time_slot_row(time_slot[0], time_slot[1])
        
        if not time_slots:
            add_time_slot_row()  # Add at least one row
        
        ttk.Button(slots_frame, text="Tambah Slot Waktu", 
                 command=lambda: add_time_slot_row()).grid(row=100, column=0, sticky="w", pady=10)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Batalkan", 
                 command=dialog.destroy).grid(row=0, column=0, padx=10)
        
        def update_team():
            # Validate inputs
            if not name_entry.get().strip():
                messagebox.showerror("Error", "Nama tim tidak boleh kosong")
                return
            
            # Parse time slots
            availability = []
            for slot in time_slots:
                try:
                    start = datetime.time(int(slot['start_hour'].get()), int(slot['start_minute'].get()))
                    end = datetime.time(int(slot['end_hour'].get()), int(slot['end_minute'].get()))
                    
                    if start >= end:
                        messagebox.showerror("Error", "Waktu selesai harus setelah waktu mulai")
                        return
                    
                    availability.append((start, end))
                except ValueError:
                    messagebox.showerror("Error", "Format waktu tidak valid")
                    return
            
            if not availability:
                messagebox.showerror("Error", "Minimal satu slot waktu harus ditambahkan")
                return
            
            # Update team
            team.name = name_entry.get().strip()
            team.available_times = availability
            
            # Save and refresh
            self.save_data()
            self.refresh_team_list(tree)
            dialog.destroy()
            
            messagebox.showinfo("Sukses", "Tim berhasil diperbarui")
        
        ttk.Button(button_frame, text="Simpan", 
                 command=update_team).grid(row=0, column=1, padx=10)
    
    def delete_team(self, tree):
        """Delete a team"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Perhatian", "Silakan pilih tim terlebih dahulu")
            return
        
        team_id = tree.item(selected[0])['values'][0]
        team = next((t for t in self.teams if t.id == team_id), None)
        
        if not team:
            return
        
        # Check if team is used in any meetings
        used_in_meetings = any(team.id in meeting.teams for meeting in self.meetings)
        
        if used_in_meetings:
            messagebox.showerror("Error", f"Tim '{team.name}' digunakan dalam jadwal rapat yang ada. "
                              "Hapus atau modifikasi rapat tersebut terlebih dahulu.")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus tim '{team.name}'?"):
            return
        
        # Delete team
        self.teams.remove(team)
        self.save_data()
        self.refresh_team_list(tree)
        
        messagebox.showinfo("Sukses", "Tim berhasil dihapus")
    
    def manage_rooms(self):
        """Open dialog to manage rooms"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Kelola Ruangan")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Room list
        ttk.Label(dialog, text="Daftar Ruangan", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        # Treeview for rooms
        room_tree_frame = ttk.Frame(dialog)
        room_tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        room_tree_scroll = ttk.Scrollbar(room_tree_frame)
        room_tree_scroll.pack(side="right", fill="y")
        
        room_tree = ttk.Treeview(room_tree_frame, columns=("ID", "Nama", "Kapasitas"), 
                                show="headings", yscrollcommand=room_tree_scroll.set)
        room_tree.heading("ID", text="ID")
        room_tree.heading("Nama", text="Nama Ruangan")
        room_tree.heading("Kapasitas", text="Kapasitas")
        
        room_tree.column("ID", width=50)
        room_tree.column("Nama", width=250)
        room_tree.column("Kapasitas", width=100)
        
        room_tree.pack(fill="both", expand=True)
        room_tree_scroll.config(command=room_tree.yview)
        
        # Buttons for room management
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="Tambah Ruangan", 
                 command=lambda: self.add_room_dialog(dialog, room_tree)).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Edit Ruangan", 
                 command=lambda: self.edit_room_dialog(dialog, room_tree)).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Hapus Ruangan", 
                 command=lambda: self.delete_room(room_tree)).pack(side="left", padx=5)
        
        # Populate room list
        self.refresh_room_list(room_tree)
    
    def refresh_room_list(self, tree):
        """Refresh room list in treeview"""
        # Clear current entries
        for item in tree.get_children():
            tree.delete(item)
        
        # Add rooms to treeview
        for room in self.rooms:
            tree.insert("", "end", values=(room.id, room.name, room.capacity))
    
    def add_room_dialog(self, parent, tree):
        """Dialog to add a new room"""
        dialog = tk.Toplevel(parent)
        dialog.title("Tambah Ruangan Baru")
        dialog.geometry("400x200")
        dialog.transient(parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Nama Ruangan:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        ttk.Label(dialog, text="Kapasitas:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        capacity_entry = ttk.Spinbox(dialog, from_=1, to=100, width=10)
        capacity_entry.insert(0, "10")
        capacity_entry.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Batalkan", 
                 command=dialog.destroy).grid(row=0, column=0, padx=10)
        
        def save_room():
            # Validate inputs
            if not name_entry.get().strip():
                messagebox.showerror("Error", "Nama ruangan tidak boleh kosong")
                return
            
            try:
                capacity = int(capacity_entry.get())
                if capacity <= 0:
                    messagebox.showerror("Error", "Kapasitas harus lebih dari 0")
                    return
            except ValueError:
                messagebox.showerror("Error", "Kapasitas harus berupa angka")
                return
            
            # Get next available ID
            next_id = max([room.id for room in self.rooms], default=0) + 1
            
            # Create new room
            new_room = Room(
                id=next_id,
                name=name_entry.get().strip(),
                capacity=capacity
            )
            
            # Add room and save
            self.rooms.append(new_room)
            self.save_data()
            self.refresh_room_list(tree)
            dialog.destroy()
            
            messagebox.showinfo("Sukses", "Ruangan berhasil ditambahkan")
        
        ttk.Button(button_frame, text="Simpan", 
                 command=save_room).grid(row=0, column=1, padx=10)
    
    def edit_room_dialog(self, parent, tree):
        """Dialog to edit an existing room"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Perhatian", "Silakan pilih ruangan terlebih dahulu")
            return
        
        room_id = tree.item(selected[0])['values'][0]
        room = next((r for r in self.rooms if r.id == room_id), None)
        
        if not room:
            return
        
        dialog = tk.Toplevel(parent)
        dialog.title(f"Edit Ruangan: {room.name}")
        dialog.geometry("400x200")
        dialog.transient(parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Nama Ruangan:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.insert(0, room.name)
        name_entry.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        ttk.Label(dialog, text="Kapasitas:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        capacity_entry = ttk.Spinbox(dialog, from_=1, to=100, width=10)
        capacity_entry.insert(0, room.capacity)
        capacity_entry.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Batalkan", 
                 command=dialog.destroy).grid(row=0, column=0, padx=10)
        
        def update_room():
            # Validate inputs
            if not name_entry.get().strip():
                messagebox.showerror("Error", "Nama ruangan tidak boleh kosong")
                return
            
            try:
                capacity = int(capacity_entry.get())
                if capacity <= 0:
                    messagebox.showerror("Error", "Kapasitas harus lebih dari 0")
                    return
            except ValueError:
                messagebox.showerror("Error", "Kapasitas harus berupa angka")
                return
            
            # Update room
            room.name = name_entry.get().strip()
            room.capacity = capacity
            
            # Save and refresh
            self.save_data()
            self.refresh_room_list(tree)
            dialog.destroy()
            
            messagebox.showinfo("Sukses", "Ruangan berhasil diperbarui")
        
        ttk.Button(button_frame, text="Simpan", 
                 command=update_room).grid(row=0, column=1, padx=10)
    
    def delete_room(self, tree):
        """Delete a room"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Perhatian", "Silakan pilih ruangan terlebih dahulu")
            return
        
        room_id = tree.item(selected[0])['values'][0]
        room = next((r for r in self.rooms if r.id == room_id), None)
        
        if not room:
            return
        
        # Check if room is used in any meetings
        used_in_meetings = any(meeting.room == room.id for meeting in self.meetings)
        
        if used_in_meetings:
            messagebox.showerror("Error", f"Ruangan '{room.name}' digunakan dalam jadwal rapat yang ada. "
                              "Hapus atau modifikasi rapat tersebut terlebih dahulu.")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus ruangan '{room.name}'?"):
            return
        
        # Delete room
        self.rooms.remove(room)
        self.save_data()
        self.refresh_room_list(tree)
        
        messagebox.showinfo("Sukses", "Ruangan berhasil dihapus")
    
    def verify_schedule(self):
        """Verify the schedule for conflicts"""
        conflicts = []
        for i, meeting in enumerate(self.meetings):
            for j, other_meeting in enumerate(self.meetings):
                if i != j:
                    # Check for room conflicts
                    if meeting.room == other_meeting.room:
                        if (meeting.start_time < other_meeting.end_time and 
                            meeting.end_time > other_meeting.start_time):
                            conflicts.append(f"Konflik Ruang: Rapat '{meeting.title}' dan '{other_meeting.title}' menggunakan ruangan yang sama pada waktu yang sama.")
                    
                    # Check for team conflicts
                    for team in meeting.teams:
                        if team in other_meeting.teams:
                            if (meeting.start_time < other_meeting.end_time and 
                                meeting.end_time > other_meeting.start_time):
                                conflicts.append(f"Konflik Tim: Tim '{self.get_team_name(team)}' memiliki rapat '{meeting.title}' dan '{other_meeting.title}' pada waktu yang sama.")
        
        if conflicts:
            messagebox.showerror("Konflik Ditemukan", "\n".join(conflicts))
        else:
            messagebox.showinfo("Verifikasi Berhasil", "Tidak ada konflik dalam jadwal.")
    
    def auto_schedule(self):
        """Automatically schedule meetings to avoid conflicts"""
        sorted_meetings = sorted(self.meetings, key=lambda m: (m.end_time.hour * 60 + m.end_time.minute) - (m.start_time.hour * 60 + m.start_time.minute))
        
        for meeting in sorted_meetings:
            for room in self.rooms:
                for start_hour in range(8, 18):
                    for start_minute in range(0, 60, 15):
                        start_time = datetime.time(start_hour, start_minute)
                        end_time = datetime.time(start_hour + (meeting.end_time.hour - meeting.start_time.hour), start_minute + (meeting.end_time.minute - meeting.start_time.minute))
                        
                        new_meeting = Meeting(
                            title=meeting.title,
                            start_time=start_time,
                            end_time=end_time,
                            teams=meeting.teams,
                            room=room.id
                        )
                        
                        if not self.check_meeting_conflicts(new_meeting):
                            meeting.start_time = start_time
                            meeting.end_time = end_time
                            meeting.room = room.id
                            break
                    else:
                        continue
                    break
        
        self.save_data()
        self.refresh_schedule_view()
        messagebox.showinfo("Jadwal Otomatis", "Proses penjadwalan otomatis selesai.")
        
        for meeting in self.meetings:
            new_room = self.find_available_room(meeting.start_time, meeting.end_time, exclude_meeting=meeting)
            if new_room:
                meeting.room = new_room
        
        self.save_data()
        self.refresh_schedule_view()
        messagebox.showinfo("Jadwal Otomatis", "Konflik telah diselesaikan dengan mengganti ruangan tanpa mengubah waktu.")
    
        
    def auto_reschedule_conflicts(self):
        for i, meeting in enumerate(self.meetings):
            for j, other_meeting in enumerate(self.meetings):
                if i != j and meeting.room == other_meeting.room:
                    if (meeting.start_time < other_meeting.end_time and 
                        meeting.end_time > other_meeting.start_time):
                        
                        # Coba cari ruangan lain yang kosong
                        new_room = self.find_available_room(meeting.start_time, meeting.end_time, exclude_meeting=meeting)
                        if new_room:
                            meeting.room = new_room
                        else:
                            messagebox.showwarning("Konflik Tidak Teratasi", 
                                f"Rapat '{meeting.title}' tidak dapat dipindahkan karena tidak ada ruangan yang tersedia.")

        self.save_data()
        self.refresh_schedule_view()

    
    def export_schedule(self):
        """Export the current schedule to a file"""
        filename = f"jadwal_rapat_{self.selected_date.strftime('%Y%m%d')}.txt"
        with open(filename, 'w') as f:
            for meeting in self.meetings:
                team_names = [self.get_team_name(team_id) for team_id in meeting.teams]
                room_name = self.get_room_name(meeting.room)
                f.write(f"Judul: {meeting.title}\n")
                f.write(f"Waktu: {meeting.start_time.strftime('%H:%M')} - {meeting.end_time.strftime('%H:%M')}\n")
                f.write(f"Tim: {', '.join(team_names)}\n")
                f.write(f"Ruangan: {room_name}\n")
                f.write("\n")
        
        messagebox.showinfo("Ekspor Jadwal", f"Jadwal berhasil diekspor ke file '{filename}'")
    
    def on_closing(self):
        """Handle the window close event"""
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar?"):
            self.root.destroy()
    
    def get_team_name(self, team_id):
        team = next((t for t in self.teams if t.id == team_id), None)
        return team.name if team else "Unknown Team"
    
    def get_room_name(self, room_id):
        room = next((r for r in self.rooms if r.id == room_id), None)
        return room.name if room else "Unknown Room"

if __name__ == "__main__":
    MeetingScheduler()
