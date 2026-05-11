import tkinter as tk
import winsound
import sys
import threading

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    pystray = None

WORK_MINUTES = 20
REST_SECONDS = 20

class EyeRestTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("OculusCare™ - Ocular Protection System")
        self.root.geometry("540x460")
        self.root.configure(bg="#F0F4F8")  # Premium clinical light blue-gray
        self.root.resizable(False, False)
        
        self.work_ms = WORK_MINUTES * 60 * 1000
        self.rest_ms = REST_SECONDS * 1000
        self.is_working = True
        self.is_paused = False
        self.time_left_ms = self.work_ms
        
        # Header Frame
        header_frame = tk.Frame(root, bg="#0D3B66", height=75)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="O C U L U S C A R E ™", font=("Segoe UI", 16, "bold"), fg="#FFFFFF", bg="#0D3B66").pack(pady=(12, 0))
        tk.Label(header_frame, text="Ocular Protection Protocol", font=("Segoe UI", 9), fg="#A0C4FF", bg="#0D3B66").pack()
        
        # Content Frame
        content_frame = tk.Frame(root, bg="#FFFFFF", highlightbackground="#E1E8ED", highlightthickness=1)
        content_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Dashboard Title
        tk.Label(content_frame, text="Sistem Pemantauan Klinis", font=("Segoe UI", 13, "bold"), fg="#2B2D42", bg="#FFFFFF").pack(pady=(20, 5))
        
        desc_text = ("Protokol 20-20-20 direkomendasikan secara global untuk\n"
                     "mencegah Sindrom Kelelahan Mata Digital (CVS).\n"
                     "Setiap 20 menit, alihkan fokus ke jarak 6 meter selama 20 detik.")
        tk.Label(content_frame, text=desc_text, font=("Segoe UI", 10), fg="#6C757D", bg="#FFFFFF", justify="center").pack(pady=(0, 20))

        # Status Display (Like a digital monitor)
        status_bg = tk.Frame(content_frame, bg="#F8F9FA", highlightbackground="#DEE2E6", highlightthickness=1)
        status_bg.pack(fill="x", padx=30, pady=5)
        
        self.status_label = tk.Label(status_bg, text="Menginisialisasi...", font=("Segoe UI", 12, "bold"), fg="#005B9F", bg="#F8F9FA")
        self.status_label.pack(pady=12)
        
        # Button Frame
        btn_frame = tk.Frame(content_frame, bg="#FFFFFF")
        btn_frame.pack(pady=20)
        
        self.btn_pause = tk.Button(btn_frame, text="Jeda Pemantauan", command=self.toggle_pause, font=("Segoe UI", 9, "bold"), bg="#E9ECEF", fg="#495057", relief="flat", padx=15, pady=6, cursor="hand2", activebackground="#DDE2E5")
        self.btn_pause.pack(side="left", padx=8)
        
        self.btn_force = tk.Button(btn_frame, text="Mulai Sesi Relaksasi", command=self.force_overlay, font=("Segoe UI", 9, "bold"), bg="#0D3B66", fg="#FFFFFF", relief="flat", padx=15, pady=6, cursor="hand2", activebackground="#155591", activeforeground="white")
        self.btn_force.pack(side="left", padx=8)
        
        tk.Label(root, text="System running actively. Please minimize this window.", font=("Segoe UI", 8, "italic"), fg="#ADB5BD", bg="#F0F4F8").pack(side="bottom", pady=10)
        
        self.side_panel = None
        self.root.bind("<Unmap>", self.on_unmap)
        self.root.bind("<Map>", self.on_map)
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        
        self.start_work_timer()
        self.update_status_loop()

    def toggle_pause(self):
        if self.is_paused:
            self.start_work_timer(reset=False)
        else:
            self.is_paused = True
            self.btn_pause.config(text="Lanjutkan Pemantauan", bg="#0D3B66", fg="#FFFFFF", activebackground="#155591")
            self.status_label.config(text="Status: SIAGA (Pemantauan Dijeda)", fg="#D90429")

    def force_overlay(self):
        self.is_paused = False
        if hasattr(self, 'btn_pause'):
            self.btn_pause.config(text="Jeda Pemantauan", bg="#E9ECEF", fg="#495057", activebackground="#DDE2E5")
        self.show_overlay()

    def start_work_timer(self, reset=True):
        self.is_working = True
        self.is_paused = False
        if hasattr(self, 'btn_pause'):
            self.btn_pause.config(text="Jeda Pemantauan", bg="#E9ECEF", fg="#495057", activebackground="#DDE2E5")
            
        if reset:
            self.time_left_ms = self.work_ms

    def update_status_loop(self):
        if self.is_working and not self.is_paused:
            if self.time_left_ms <= 0:
                self.show_overlay()
            else:
                mins = (self.time_left_ms // 1000) // 60
                secs = (self.time_left_ms // 1000) % 60
                self.status_label.config(text=f"Waktu menuju sesi relaksasi: {mins:02d}:{secs:02d}", fg="#005B9F")
                self.time_left_ms -= 1000
        
        if hasattr(self, 'update_side_panel_timer'):
            self.update_side_panel_timer()
            
        self.root.after(1000, self.update_status_loop)

    def show_overlay(self):
        self.is_working = False
        self.status_label.config(text="Sesi relaksasi sedang berlangsung...", fg="#28A745")
        
        if hasattr(self, 'hide_side_panel'):
            self.hide_side_panel()
            
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
        
        self.overlay = tk.Toplevel(self.root)
        self.overlay.attributes("-fullscreen", True)
        self.overlay.attributes("-topmost", True)
        self.overlay.configure(bg="#081C15")  # Very dark clinical green/black
        self.overlay.attributes("-alpha", 0.96)
        
        self.overlay.protocol("WM_DELETE_WINDOW", self.do_nothing)
        
        # Center Frame
        frame = tk.Frame(self.overlay, bg="#081C15")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="O C U L U S C A R E ™   P R O T O C O L", font=("Segoe UI", 16, "bold"), fg="#52B788", bg="#081C15").pack(pady=(0, 15))
        tk.Label(frame, text="SESI RELAKSASI OKULER", font=("Segoe UI", 52, "bold"), fg="#FFFFFF", bg="#081C15").pack(pady=(0, 25))
        
        instruction = "Prosedur Klinis:\nAlihkan pandangan Anda dari layar. Tatap objek berjarak 6 meter."
        tk.Label(frame, text=instruction, font=("Segoe UI", 20), fg="#B7E4C7", bg="#081C15", justify="center").pack(pady=(0, 55))
        
        # Timer display
        timer_bg = tk.Frame(frame, bg="#1B4332", padx=50, pady=25)
        timer_bg.pack(pady=10)
        self.timer_label = tk.Label(timer_bg, text=str(REST_SECONDS), font=("Segoe UI", 120, "bold"), fg="#D8F3DC", bg="#1B4332")
        self.timer_label.pack()
        
        skip_btn = tk.Button(self.overlay, text="Abaikan (Tidak Disarankan Secara Medis)", command=self.skip_rest, font=("Segoe UI", 10), bg="#2D6A4F", fg="#D8F3DC", relief="flat", padx=20, pady=10, cursor="hand2", activebackground="#40916C", activeforeground="white")
        skip_btn.place(relx=0.5, rely=0.9, anchor="center")
        
        self.rest_time_left = REST_SECONDS
        self.update_countdown()

    def do_nothing(self):
        pass

    def update_countdown(self):
        if self.rest_time_left > 0:
            self.timer_label.config(text=str(self.rest_time_left))
            self.rest_time_left -= 1
            self.overlay.after(1000, self.update_countdown)
        else:
            self.end_rest()

    def skip_rest(self):
        self.end_rest()

    def end_rest(self):
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
        self.overlay.destroy()
        self.start_work_timer()
        if self.root.state() == 'iconic':
            self.show_side_panel()

    def on_unmap(self, event):
        if event.widget == self.root:
            if self.root.state() == 'iconic':
                self.show_side_panel()

    def on_map(self, event):
        if event.widget == self.root:
            if self.root.state() == 'normal':
                self.hide_side_panel()

    def show_side_panel(self):
        if self.side_panel is not None:
            return
            
        self.side_panel = tk.Toplevel(self.root)
        self.side_panel.overrideredirect(True)
        self.side_panel.attributes("-topmost", True)
        self.side_panel.attributes("-alpha", 0.95)
        self.side_panel.configure(bg="#0F172A", highlightthickness=1, highlightbackground="#1E293B")
        
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        # Positioned on the bottom right corner
        self.side_panel.geometry(f"200x70+{sw - 230}+{sh - 140}")
        
        def start_move(event):
            self.side_panel.x = event.x
            self.side_panel.y = event.y

        def do_move(event):
            x = self.side_panel.winfo_x() + event.x - getattr(self.side_panel, 'x', event.x)
            y = self.side_panel.winfo_y() + event.y - getattr(self.side_panel, 'y', event.y)
            self.side_panel.geometry(f"+{x}+{y}")

        container = tk.Frame(self.side_panel, bg="#0F172A")
        container.pack(fill="both", expand=True)

        # Left accent bar
        accent = tk.Frame(container, bg="#38BDF8", width=4)
        accent.pack(side="left", fill="y")

        content = tk.Frame(container, bg="#0F172A")
        content.pack(fill="both", expand=True, padx=12, pady=8)

        # Pulse indicator / Icon
        icon_lbl = tk.Label(content, text="◉", font=("Segoe UI", 16), bg="#0F172A", fg="#38BDF8")
        icon_lbl.pack(side="left", padx=(0, 12))

        # Middle column for texts
        txt_frame = tk.Frame(content, bg="#0F172A")
        txt_frame.pack(side="left", fill="both", expand=True)

        self.sp_timer_label = tk.Label(txt_frame, text="--:--", font=("Segoe UI", 16, "bold"), bg="#0F172A", fg="#F8FAFC")
        self.sp_timer_label.pack(anchor="w", pady=(0, 0))

        brand_lbl = tk.Label(txt_frame, text="O C U L U S C A R E", font=("Segoe UI", 6, "bold"), bg="#0F172A", fg="#94A3B8")
        brand_lbl.pack(anchor="w", pady=(2, 0))

        # Restore button (right aligned)
        btn_restore = tk.Button(content, text="⤢", font=("Segoe UI", 12), bg="#0F172A", fg="#64748B", relief="flat", command=self.restore_main, cursor="hand2", activebackground="#1E293B", activeforeground="#38BDF8", bd=0)
        btn_restore.pack(side="right", padx=(5, 0))
        
        drag_widgets = [self.side_panel, container, accent, content, icon_lbl, txt_frame, self.sp_timer_label, brand_lbl]
        for w in drag_widgets:
            w.bind("<Button-1>", start_move)
            w.bind("<B1-Motion>", do_move)
            w.bind("<Double-Button-1>", lambda e: self.restore_main())
        
        self.update_side_panel_timer()

    def hide_side_panel(self):
        if hasattr(self, 'side_panel') and self.side_panel is not None:
            self.side_panel.destroy()
            self.side_panel = None

    def restore_main(self):
        self.root.deiconify()
        self.root.state('normal')
        self.hide_side_panel()

    def update_side_panel_timer(self):
        if hasattr(self, 'side_panel') and self.side_panel is not None:
            if self.is_working and not self.is_paused:
                mins = (self.time_left_ms // 1000) // 60
                secs = (self.time_left_ms // 1000) % 60
                self.sp_timer_label.config(text=f"{mins:02d}:{secs:02d}", fg="#F8FAFC")
            elif self.is_paused:
                self.sp_timer_label.config(text="JEDA", fg="#F43F5E")

    def minimize_to_tray(self):
        if pystray is None:
            self.root.destroy()
            return
        self.root.withdraw()
        self.hide_side_panel()
        self.create_tray_icon()

    def create_tray_icon(self):
        image = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((8, 8, 56, 56), fill="#5BC0BE")
        draw.ellipse((20, 20, 44, 44), fill="#0B132B")
        
        menu = pystray.Menu(
            pystray.MenuItem("Buka / Show", self.restore_from_tray, default=True),
            pystray.MenuItem("Keluar / Exit", self.exit_app)
        )
        
        self.tray_icon = pystray.Icon("OculusCare", image, "OculusCare", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def restore_from_tray(self, icon=None, item=None):
        if hasattr(self, 'tray_icon') and self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None
        self.root.after(0, self._restore_main_window)

    def _restore_main_window(self):
        self.root.deiconify()
        self.root.state('normal')

    def exit_app(self, icon=None, item=None):
        if hasattr(self, 'tray_icon') and self.tray_icon:
            self.tray_icon.stop()
        self.root.after(0, self.root.destroy)

if __name__ == "__main__":
    # Ensure High DPI awareness for sharper UI on Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    root = tk.Tk()
    app = EyeRestTimer(root)
    root.mainloop()
