import tkinter as tk
import winsound
import sys

WORK_MINUTES = 20
REST_SECONDS = 20

class EyeRestTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("VisionCare™ - Ocular Protection System")
        self.root.geometry("540x460")
        self.root.configure(bg="#F0F4F8")  # Premium clinical light blue-gray
        self.root.resizable(False, False)
        
        self.work_ms = WORK_MINUTES * 60 * 1000
        self.rest_ms = REST_SECONDS * 1000
        self.is_working = True
        self.is_paused = False
        self.time_left_ms = self.work_ms
        self.timer_id = None
        
        # Header Frame
        header_frame = tk.Frame(root, bg="#0D3B66", height=75)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="V I S I O N C A R E ™", font=("Segoe UI", 16, "bold"), fg="#FFFFFF", bg="#0D3B66").pack(pady=(12, 0))
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
        
        self.start_work_timer()
        self.update_status_loop()

    def toggle_pause(self):
        if self.is_paused:
            self.start_work_timer(reset=False)
        else:
            self.is_paused = True
            self.btn_pause.config(text="Lanjutkan Pemantauan", bg="#0D3B66", fg="#FFFFFF", activebackground="#155591")
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
            self.status_label.config(text="Status: SIAGA (Pemantauan Dijeda)", fg="#D90429")

    def force_overlay(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
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
            
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.timer_id = self.root.after(self.time_left_ms, self.show_overlay)

    def update_status_loop(self):
        if self.is_working and not self.is_paused:
            mins = (self.time_left_ms // 1000) // 60
            secs = (self.time_left_ms // 1000) % 60
            self.status_label.config(text=f"Waktu menuju sesi relaksasi: {mins:02d}:{secs:02d}", fg="#005B9F")
            self.time_left_ms -= 1000
        self.root.after(1000, self.update_status_loop)

    def show_overlay(self):
        self.is_working = False
        self.status_label.config(text="Sesi relaksasi sedang berlangsung...", fg="#28A745")
        
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

        tk.Label(frame, text="V I S I O N C A R E ™   P R O T O C O L", font=("Segoe UI", 16, "bold"), fg="#52B788", bg="#081C15").pack(pady=(0, 15))
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
