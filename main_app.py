import os
import tkinter as tk
from tkinter import ttk, messagebox
from manager import FamilyTreeManager
from PIL import Image, ImageTk
from tkinter import filedialog
# Buraya manager.py dosyasını import etmelisiniz, ancak şimdilik yorum satırı olarak bırakalım.
# from manager import FamilyTreeManager 

# --- KAYDIRMALI ANAHTAR SINIFI (ToggleSwitch) ---
class ToggleSwitch(tk.Canvas):
    def __init__(self, master, width=60, height=30, command=None, **kwargs):
        super().__init__(master, width=width, height=height, bd=0, highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.command = command
        self.is_on = False
        
        # Renkler (Optimize edilmiş yumuşak tonlar)
        self.on_color = "#4CAF50"  # Yeşil
        self.off_color = "#ccc"    # Gri
        self.handle_color = "white"
        handle_padding = 3 
        
        # Arka plan için ovali kullanmak daha iyi bir görünüm sağlar (Yumuşak kenarlar)
        self.bg_rect = self.create_oval(
            1, 1, width - 1, height - 1, 
            fill=self.off_color, 
            outline="",
        )
        
        # Düğme (Handle) için daire
        self.handle_circle = self.create_oval(
            handle_padding, handle_padding, 
            height - handle_padding, height - handle_padding, 
            fill=self.handle_color, 
            outline="",
        )

        self.bind("<Button-1>", self.toggle)
        self._move_handle()

    def _move_handle(self):
        """Anahtar düğmesini AÇIK veya KAPALI pozisyonuna hareket ettirir."""
        handle_size = self.height - 2 * 3 
        
        if self.is_on:
            x_start = self.width - handle_size - 3 # Sağ taraf
            self.itemconfig(self.bg_rect, fill=self.on_color)
        else:
            x_start = 3 # Sol taraf
            self.itemconfig(self.bg_rect, fill=self.off_color)
            
        x_end = x_start + handle_size
        y_start = 3
        y_end = self.height - 3
        
        self.coords(self.handle_circle, x_start, y_start, x_end, y_end)

    def toggle(self, event=None):
        """Anahtarın durumunu değiştirir."""
        self.is_on = not self.is_on
        self._move_handle()
        
        if self.command:
            self.command()
            
    def get_state(self):
        return self.is_on
# main_app.py dosyasına eklenecek yeni sınıf

class NewCharacterForm(tk.Toplevel):
    """Yeni karakter eklemek için kullanılan küçük pop-up pencere."""
    def __init__(self, master, manager=None):
        super().__init__(master)
        self.title("Yeni Karakter Oluştur")
        self.geometry("350x300")
        self.manager = manager # FamilyTreeManager'ı bağlamak için
        
        # Pencereyi kilitler: Kullanıcı bu pencereyi kapatmadan ana pencereye dönemez.
        self.transient(master) 
        self.grab_set() 
        
        self.create_widgets()
    
    def choose_image(self):
        filename = filedialog.askopenfilename(
            title="Resim Seç",
            filetypes=[("Resim Dosyaları", "*.png *.jpg *.jpeg *.gif")]
        )
        if filename:
            self.selected_image_path = filename
            self.img_label.config(text="Resim Seçildi ✅")






    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        # 1. İsim Alanı
        ttk.Label(main_frame, text="Ad/Soyad:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(main_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)

        # 2. Irk/Tür Alanı
        ttk.Label(main_frame, text="Irk/Tür:").grid(row=1, column=0, sticky="w", pady=5)
        self.species_entry = ttk.Entry(main_frame, width=30)
        self.species_entry.grid(row=1, column=1, pady=5, padx=5)

        # 3. Notlar Alanı
        ttk.Label(main_frame, text="Notlar:").grid(row=2, column=0, sticky="nw", pady=5)
        self.description_entry = tk.Text(main_frame, width=25, height=4)
        self.description_entry.grid(row=2, column=1, pady=5, padx=5)

        # 4. Resim Seçme Alanı
        self.selected_image_path = None
        ttk.Label(main_frame, text="Profil Resmi:").grid(row=3, column=0, pady=5, sticky="w")
        self.img_label = ttk.Label(main_frame, text="Varsayılan kullanılacak")
        self.img_label.grid(row=3, column=1, sticky="w", padx=5)
        
        ttk.Button(main_frame, text="Gözat...", command=self.choose_image).grid(row=4, column=1, sticky="w", padx=5)

        # 5. Kaydetme Butonu (Satır numarasını 6 yaptım ki diğerleriyle çakışmasın)
        save_button = ttk.Button(main_frame, text="Portre Oluştur", command=self.save_character)
        save_button.grid(row=6, column=0, columnspan=2, pady=20)


        
        
    def save_character(self):
        """Kullanıcının girdiği verileri ve seçtiği resmi alarak karakteri oluşturur."""
        # Kullanıcının girdiği verileri al
        name = self.name_entry.get().strip()
        species = self.species_entry.get().strip()
        description = self.description_entry.get("1.0", tk.END).strip()

        if not name:
            tk.messagebox.showerror("Hata", "Ad/Soyad alanı boş bırakılamaz!")
            return

        # 1. Veri Yöneticisine (Manager) gönderme
        if self.manager:
            # KRİTİK DÜZELTME: image_path parametresini buraya ekledik!
            new_char = self.manager.add_character(
                name=name, 
                species=species, 
                description=description, 
                image_path=self.selected_image_path # Seçilen resim yolunu gönderiyoruz
            )
            
            # 2. Ana uygulamada Canvas üzerine çizdir
            self.master.draw_character_on_canvas(new_char)
            print(f"SİSTEM: {name} karakteri özel resmiyle oluşturuldu.")
        
        # 3. Formu kapat
        self.destroy()

# ... NewCharacterForm sınıfı burada bitiyor.

# YENİ EKLENECEK SINIF BURAYA GELİYOR:

class CharacterEditForm(tk.Toplevel):
    """Mevcut karakterin bilgilerini görüntüleme ve düzenleme formu."""
    def __init__(self, master, manager, character_id):
        super().__init__(master)
        self.title("Karakter Bilgilerini Düzenle")
        self.geometry("350x260")
        self.manager = manager
        self.char_id = character_id
        self.character = manager.characters[character_id] 
        
        self.transient(master) 
        self.grab_set() 
        
        self.create_widgets()
        self.load_character_data() 

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # ID'yi gösterme
        ttk.Label(main_frame, text=f"ID: {self.char_id[:8]}...").grid(row=0, column=0, columnspan=2, sticky="w", pady=5)

        # 1. İsim Alanı
        ttk.Label(main_frame, text="Ad/Soyad:").grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(main_frame, width=30)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)

        # 2. Irk/Tür Alanı
        ttk.Label(main_frame, text="Irk/Tür:").grid(row=2, column=0, sticky="w", pady=5)
        self.species_entry = ttk.Entry(main_frame, width=30)
        self.species_entry.grid(row=2, column=1, pady=5, padx=5)

        # 3. Notlar Alanı
        ttk.Label(main_frame, text="Notlar:").grid(row=3, column=0, sticky="nw", pady=5)
        self.description_entry = tk.Text(main_frame, width=25, height=4)
        self.description_entry.grid(row=3, column=1, pady=5, padx=5)

        # Kaydetme Butonu
        save_button = ttk.Button(main_frame, text="Değişiklikleri Kaydet", command=self.save_changes)
        save_button.grid(row=4, column=0, columnspan=2, pady=10)
        
    def load_character_data(self):
        if self.character:
            self.name_entry.insert(0, self.character.name)
            self.species_entry.insert(0, self.character.species if self.character.species else "")
            self.description_entry.insert('1.0', self.character.description if self.character.description else "")

    def save_changes(self):
        name = self.name_entry.get().strip()
        species = self.species_entry.get().strip()
        description = self.description_entry.get("1.0", tk.END).strip()

        if not name:
            messagebox.showerror("Hata", "Ad/Soyad boş bırakılamaz!")
            return

        # Karakter objesini güncelle
        self.character.name = name
        self.character.species = species
        self.character.description = description
        
        # Canvas'taki portre ismini güncelle (Görsel geri bildirim)
        self.master.update_portrait_name(self.char_id, name)
        
        print(f"BİLGİ: Karakter {name} güncellendi.")
        self.destroy()

# ... FamilyTreeApp sınıfı başlıyor ...

class FamilyTreeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kurgusal Evren Soy Ağacı")
        self.geometry("1200x800")
        self.zoom_timer = None
        # Tema Ayarları
        self.is_dark_mode = False
        self.light_bg = "white"
        self.dark_bg = "#1E1E1E"
        self.light_fg = "gray"
        self.dark_fg = "#00FF00"
        self.is_disconnect_mode = False
        # Veri Yöneticisini Başlat (Bu, manager.py'den veriyi yükler)
        self.manager = FamilyTreeManager()
        
        # --- ÇİZİM VE DURUM DEĞİŞKENLERİ ---
        self.drawn_characters = {}      
        self.relationship_lines = {}
        
        # --- SÜRÜKLEME VE BAĞLANTI DEĞİŞKENLERİ ---
        self.drag_item_tag = None       
        self.last_x, self.last_y = 0, 0 
        self.is_connect_mode = False          
        self.first_clicked_char_id = None     
        self.selected_char_id = None    # Sağ tıklama için seçili karakter
        
        # --- ZOOM DEĞİŞKENLERİ ---
        self.zoom_level = 1.0 
        self.scale_factor = 1.1 

        # 1. Widget'ları Oluştur (self.canvas bu aşamada oluşturulur!)
        self.create_widgets() 
        
        # 2. Temayı Uygula
        self.apply_theme()
        
        # 3. Yüklenen Veriyi Çiz (Widget'lar oluştuktan sonra güvenle çizim başlar)
        # after(100) ile Canvas'ın tamamen oluşması için küçük bir gecikme eklenir.
        self.after(100, self.initial_draw)
        
        # 4. UYGULAMA KAPANMA OLAYINI BAĞLA (Veriyi Kaydetmek İçin)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # FamilyTreeApp sınıfı içinde

    def open_depo_window(self):
        """DepoWindow'u başlatır."""
        DepoWindow(self, manager=self.manager)

    def redraw_all_relationships(self):
        """Tüm mevcut ilişki çizgilerini Canvas'tan siler ve yeniden çizer.
           Bu, bir karakter geri alındığında ilişkileri güncellemek için kullanılır."""
        
        # 1. Önce mevcut tüm çizgileri Canvas'tan sil
        for line_id in self.relationship_lines.values():
            self.canvas.delete(line_id)
        self.relationship_lines = {} # Takip sözlüğünü sıfırla
        
        # 2. Tüm karakterler arasındaki ilişkileri yeniden çiz
        for char in self.manager.characters.values():
            for child_id in char.children:
                # Sadece hem ebeveyn hem çocuk Canvas'ta çiziliyorsa çiz
                if char.id in self.drawn_characters and child_id in self.drawn_characters:
                    # Yükleme bayrağı ile çağır, manager'a kaydetme yapma
                    self.draw_relationship_line(char.id, child_id, is_loading=True)

    def get_image(self, path, width=90, height=90):
        try:
            # Önce kullanıcın seçtiği özel yolu kontrol et
            if path and os.path.exists(path):
                img = Image.open(path)
            else:
                # EĞER ÖZEL RESİM YOKSA VARSAYILANI YÜKLE
                # Dosya yolunu garantilemek için tam yol alıyoruz
                base_dir = os.path.dirname(__file__)
                default_path = os.path.join(base_dir, "default_avatar.png")
                
                if os.path.exists(default_path):
                    img = Image.open(default_path)
                else:
                    print(f"HATA: {default_path} bulunamadı!")
                    return None
            
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Resim işleme hatası: {e}")
            return None




    def setup_panning_binding(self):
        """Kaydırma (Panning) olaylarını Canvas'a bağlar."""
        # Sol fare tuşu (<Button-1>) portre sürükleme ve bağlantı için kullanıldığı için,
        # Kaydırma için orta fare tuşunu (<Button-2> veya <Button-3>) kullanalım.
        
        # Windows/Linux'ta Orta Tuş (Genellikle tekerleğe basmak)
        self.canvas.bind("<Button-2>", self.start_pan)
        self.canvas.bind("<B2-Motion>", self.pan_canvas)
        self.canvas.bind("<ButtonRelease-2>", self.stop_pan)
        
        # Alternatif olarak, sağ tuş (<Button-3>) da kullanılabilir.

    def start_pan(self, event):
        """Kaydırma işlemini başlatır."""
        self.canvas.scan_mark(event.x, event.y)
        print("PANNING: Kaydırma işlemi başlatıldı (Orta Tuş).")
        
    def pan_canvas(self, event):
        """Fare hareket ettikçe Canvas'ı kaydırır."""
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        
    def stop_pan(self, event):
        """Kaydırma işlemini bitirir."""
        print("PANNING: Kaydırma durduruldu.")

    # FamilyTreeApp sınıfı içinde, diğer metotların arasına ekleyin:

    def open_edit_form(self):
        """Sağ tıklanan karakterin düzenleme formunu açar."""
        if self.selected_char_id:
            # KRİTİK DÜZELTME: CharacterEditForm çağrısı buraya geliyor
            CharacterEditForm(self, 
                              manager=self.manager, 
                              character_id=self.selected_char_id)
            
    def update_portrait_name(self, char_id, new_name):
        """Canvas üzerindeki portrenin ismini günceller."""
        if char_id in self.drawn_characters:
            text_id = self.drawn_characters[char_id]['text']
            self.canvas.itemconfig(text_id, text=new_name)


    # FamilyTreeApp sınıfı içinde, yeni metot

    def handle_triple_click_edit(self, event):
        """Üç kez tıklama olayıyla düzenleme formunu açar."""
        # Portre ID'sini bul
        item_id = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item_id)
        
        if "portre" in tags:
            char_id = tags[0]
            # Düzenleme formunu aç
            CharacterEditForm(self, 
                              manager=self.manager, 
                              character_id=char_id)

    # FamilyTreeApp sınıfı içinde

    def handle_double_click_edit(self, event):
        """Çift tıklama olayıyla düzenleme formunu açar."""
        
        # Tıklanan öğeyi bul
        item_id = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item_id)
        
        if "portre" in tags:
            char_id = tags[0]
            # Düzenleme formunu aç
            CharacterEditForm(self, 
                              manager=self.manager, 
                              character_id=char_id)
            print(f"ETKİLEŞİM: {self.manager.characters[char_id].name} için çift tıklama ile düzenleme formu açıldı.")

    # FamilyTreeApp sınıfı içinde, create_widgets metodu
    # FamilyTreeApp sınıfı içine yeni metot:

    def toggle_disconnect_mode(self):
        self.is_disconnect_mode = not self.is_disconnect_mode
        self.first_clicked_char_id = None # Seçimi sıfırla

        if self.is_disconnect_mode:
            # Diğer modları kapat ki çakışmasın
            self.is_connect_mode = False
            self.connect_button.config(text="İlişki Kur (Kapalı)", style='TButton')
            
            self.disconnect_button.config(text="İlişki Sil (AÇIK)", style='Connect.TButton')
            print("MODE: İlişki Silme modu aktif. Bağlantısını koparmak istediğiniz iki portreye tıklayın.")
        else:
            self.disconnect_button.config(text="İlişki Sil (Kapalı)", style='TButton')
 
    def create_widgets(self):
        # --- Ana Çerçeve ---
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Sol Panel (Kontroller) ---
        control_panel = ttk.Frame(main_frame, width=200, relief=tk.RAISED, borderwidth=1)
        control_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        # 1. + Butonu
        add_button = ttk.Button(control_panel, text="+ Yeni Portre", command=self.add_new_character)
        add_button.pack(pady=10, padx=10, fill=tk.X)
        
        # 2. KARANLIK MOD ANAHTARI
        dark_mode_label = ttk.Label(control_panel, text="Karanlık Mod:")
        dark_mode_label.pack(pady=(10, 0), padx=10)
        self.toggle_switch = ToggleSwitch(control_panel, command=self.toggle_dark_mode)
        self.toggle_switch.pack(pady=(0, 10), padx=10) 

        # 3. İLİŞKİ KURMA BUTONU
        s = ttk.Style()
        s.configure('Connect.TButton', background='red', foreground='black')
        self.connect_button = ttk.Button(control_panel, text="İlişki Kur (Kapalı)", command=self.toggle_connect_mode)
        self.connect_button.pack(pady=10, padx=10, fill=tk.X)


        # 3.5 İLİŞKİ SİLME BUTONU
        self.disconnect_button = ttk.Button(control_panel, text="İlişki Sil (Kapalı)", command=self.toggle_disconnect_mode)
        self.disconnect_button.pack(pady=5, padx=10, fill=tk.X)
        
        # 4. DEPO BUTONU (İŞLEVİ BURADAN GELİYOR)
        self.depo_button = ttk.Button(control_panel, text="Karakter Deposunu Aç", command=self.open_depo_window)
        self.depo_button.pack(pady=5, padx=10, fill=tk.X)

        # --- Merkez Alan (Canvas/Çalışma Alanı) ---
        self.canvas_frame = ttk.Frame(main_frame, relief=tk.SUNKEN, borderwidth=2)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=0)
        
        # 1. Kaydırma Çubuklarını Tanımla
        self.x_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)
        self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.y_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL)
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 2. Canvas'ı Tanımla ve Kaydırma Çubuklarına Bağla
        self.canvas = tk.Canvas(
            self.canvas_frame, 
            bg=self.light_bg,
            xscrollcommand=self.x_scrollbar.set,
            yscrollcommand=self.y_scrollbar.set
        ) 
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 3. Kaydırma Çubuklarını Canvas'a Bağla
        self.x_scrollbar.config(command=self.canvas.xview)
        self.y_scrollbar.config(command=self.canvas.yview)
        
        # Çalışma Alanı Boyutunu Ayarla
        self.canvas.config(scrollregion=(0, 0, 4000, 3000))
        
        # 4. Canvas Olaylarını Bağlama (TEMİZ ve SADE)
        
        # Başlangıç metni
        self.canvas_text_id = self.canvas.create_text(
            600, 400, text="BOŞ ÇALIŞMA ALANI (CANVAS)", font=("Arial", 24), fill=self.light_fg, tags="welcome_text" 
        )

        # Pencere boyutlandırma olayını bağla
        self.canvas.bind('<Configure>', self.recenter_canvas_text)
        
        # Zoom ve Kaydırma (Panning) olaylarını bağla
        self.setup_zoom_binding()
        self.setup_panning_binding() 

        # Portreye Çift Tıklama (Düzenleme Formu)
        self.canvas.tag_bind("portre", '<Double-1>', self.handle_double_click_edit)

        # Sağ Tıklama Menüsü Bağlantısı (Context Menu)
        self.canvas.bind('<Button-3>', self.show_context_menu)
        
        # NOT: Sürükleme işlevi (make_draggable) portre oluşturulduğunda zaten Button-1'e bağlanmıştır.
    
    def setup_zoom_binding(self):
        """Fare tekerleği olaylarını Canvas'a bağlar."""
        # Windows/Linux
        self.canvas.bind("<MouseWheel>", self.on_zoom)
        # MacOS
        self.canvas.bind("<Button-4>", self.on_zoom)
        self.canvas.bind("<Button-5>", self.on_zoom)
    
    def on_zoom(self, event):
        """Hızlı ve akıcı zoom için optimize edilmiş metot."""
        if event.num == 4 or event.delta > 0:
            if self.zoom_level >= 3.0: return
            new_scale = self.scale_factor
            self.zoom_level *= self.scale_factor
        elif event.num == 5 or event.delta < 0:
            if self.zoom_level <= 0.1: return
            new_scale = 1.0 / self.scale_factor
            self.zoom_level /= self.scale_factor
        else:
            return

        # 1. VEKTÖREL OBJELERİ ANINDA ÖLÇEKLENDİR (Bu çok hızlıdır)
        self.canvas.scale("all", event.x, event.y, new_scale, new_scale)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # 2. RESİMLERİ GECİKMELİ GÜNCELLE (FPS artırıcı kısım)
        # Eğer hali hazırda bekleyen bir güncelleme varsa iptal et
        if self.zoom_timer is not None:
            self.after_cancel(self.zoom_timer)
        
        # Zoom bittikten 150ms sonra resimleri güncelle
        self.zoom_timer = self.after(150, self.apply_image_zoom)

    def apply_image_zoom(self):
        """Zoom işlemi bittiğinde resimleri toplu ve tek seferde boyutlandırır."""
        base_size = 90
        new_size = int(base_size * self.zoom_level)
        
        if new_size > 5:
            for char_id, char in self.manager.characters.items():
                if char_id in self.drawn_characters:
                    new_photo = self.get_image(char.image_path, width=new_size, height=new_size)
                    self.image_refs[char_id] = new_photo
                    
                    img_items = self.canvas.find_withtag(f"portre_resim && {char_id}")
                    if img_items:
                        self.canvas.itemconfig(img_items[0], image=new_photo)
        
        self.zoom_timer = None
        print(f"SİSTEM: Resimler {new_size}px boyutuna güncellendi.")

    def get_all_drawn_positions(self):
        """Tüm portrelerin Canvas üzerindeki güncel pozisyonlarını toplar."""
        positions = {}
        for char_id, data in self.drawn_characters.items():
            # Dikdörtgenin (rect) koordinatlarını al [x1, y1, x2, y2]
            coords = self.canvas.coords(data['rect'])
            if coords:
                # Başlangıç x ve y koordinatlarını (sol üst köşe) kaydediyoruz
                positions[char_id] = {"x": coords[0], "y": coords[1]}
        return positions

    def initial_draw(self):
        """Uygulama başladığında, yüklenmiş veriye göre portreleri çizer."""
        if self.manager.characters:
            # Hoş geldin metnini sil
            if self.canvas_text_id:
                 self.canvas.delete(self.canvas_text_id)
                 self.canvas_text_id = None
                 
            # 1. Portreleri Pozisyonlarına göre çiz
            for char_id, character in self.manager.characters.items():
                
                pos = self.manager.drawn_characters_coords.get(char_id, {"x": 50, "y": 50})
                
                self.draw_character_on_canvas(character, initial_x=pos['x'], initial_y=pos['y'], is_loading=True)

            # 2. İlişki çizgilerini çiz (is_loading=True ile çağır)
            for char in self.manager.characters.values():
                for child_id in char.children:
                    if child_id in self.drawn_characters:
                        # YENİ: is_loading=True bayrağını ekledik!
                        self.draw_relationship_line(char.id, child_id, is_loading=True)
        
        # Yükleme sonrası Canvas boyutunu ayarla
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_close(self):
        """Uygulama kapanırken veriyi kaydeder."""
        # 1. Portrelerin güncel pozisyonlarını al
        current_positions = self.get_all_drawn_positions()
        
        # 2. Manager'a kaydetme komutu gönder
        self.manager.save_all_data(current_positions)
        
        # 3. Uygulamayı kapat
        self.destroy()

    def add_new_character(self):
        NewCharacterForm(self, manager=self.manager)

    def toggle_dark_mode(self):
        self.is_dark_mode = self.toggle_switch.get_state()
        self.apply_theme()

    # FamilyTreeApp sınıfı içinde, apply_theme metodu

    def apply_theme(self):
        if self.is_dark_mode:
            bg_color = self.dark_bg
            fg_color = self.dark_fg
        else:
            bg_color = self.light_bg
            fg_color = self.light_fg
            
        # KRİTİK KONTROL: self.canvas'ın varlığını kontrol et
        if hasattr(self, 'canvas') and self.canvas is not None: 
            self.canvas.config(bg=bg_color)
            
            if self.canvas_text_id:
                self.canvas.itemconfig(self.canvas_text_id, fill=fg_color)
        else:
            # Eğer Canvas henüz yoksa, temayı uygulamadan devam et
            print("TEMA: Canvas henüz oluşturulmadı. Tema ayarları atlandı.")
            pass
            
    def recenter_canvas_text(self, event):
        if self.canvas_text_id:
            width = event.width
            height = event.height
            self.canvas.coords(self.canvas_text_id, width / 2, height / 2)
            
    # FamilyTreeApp sınıfı içinde, draw_character_on_canvas metodu

    def draw_character_on_canvas(self, character, initial_x=50, initial_y=50, is_loading=False):
        """Karakter objesini resmi ve ismiyle beraber Canvas üzerine çizer."""
        
        # --- KRİTİK TEMİZLİK KONTROLÜ ---
        if character.id in self.drawn_characters:
            self.canvas.delete(character.id)

        # POZİSYON HESAPLAMA
        if is_loading:
            x, y = initial_x, initial_y
        else:
            x, y = initial_x, initial_y + len(self.drawn_characters) * 140 # Boşluk artırıldı
            
        # Portre Boyutları (Resim + İsim için dikey form)
        width, height = 110, 140 

        # 1. Portre Arka Planı (Kart yapısı)
        rect_id = self.canvas.create_rectangle(
            x, y, x + width, y + height, 
            fill="#ADD8E6", outline="black", width=2,
            tags=(character.id, "portre")
        )

        # 2. Resim Ekleme Bölümü
        # character.image_path varsa onu yükler, yoksa default_avatar.png kullanır
        image_path = getattr(character, 'image_path', None)
        photo = self.get_image(image_path, width=90, height=90)
        
        if photo:
            # Resim referansını sakla (Silinmemesi için şart)
            if not hasattr(self, 'image_refs'): self.image_refs = {}
            self.image_refs[character.id] = photo
            
            # Resmi kartın üst-orta kısmına yerleştir
            image_id = self.canvas.create_image(
                x + width/2, y + 55, 
                image=photo, tags=(character.id, "portre_resim")
            )

        # 3. İsim Etiketi (Resmin hemen altına)
        text_id = self.canvas.create_text(
            x + width/2, y + 120, 
            text=character.name, font=("Arial", 9, "bold"), 
            fill="black", tags=(character.id, "portre_isim"),
            width=100, justify="center"
        )
        
        # Karşılama metnini sil
        if self.canvas_text_id:
            self.canvas.delete(self.canvas_text_id)
            self.canvas_text_id = None
            
        # Takip listesine kaydet
        self.drawn_characters[character.id] = {
            'rect': rect_id,
            'text': text_id,
            'obj': character
        }
        
        # Tüm portreyi tek parça halinde sürüklenebilir yap
        self.make_draggable(character.id)

    def make_draggable(self, tag_or_id):
        self.canvas.tag_bind(tag_or_id, '<Button-1>', self.start_drag_or_connect)      
        self.canvas.tag_bind(tag_or_id, '<B1-Motion>', self.drag_portre)   
        self.canvas.tag_bind(tag_or_id, '<ButtonRelease-1>', self.stop_drag) 
        
    def start_drag_or_connect(self, event):
        """Tıklanan nesneyi tam isabetle tespit eder."""
        # 'current' etiketi, farenin tam altındaki nesneyi verir
        item_id = self.canvas.find_withtag("current")
        if not item_id:
            return
            
        item_id = item_id[0]
        tags = self.canvas.gettags(item_id)
        
        # Sadece geçerli portre öğelerini işleme al
        if "portre" not in tags and "portre_isim" not in tags:
            return

        char_id = tags[0] # Karakter ID'si her zaman ilk etikettir

        # 1. Bağlantı Modu Kontrolü
        if self.is_connect_mode:
            self.handle_connect_click(item_id)
            return
        elif self.is_disconnect_mode: # YENİ EKLENEN KISIM
            self.handle_disconnect_click(item_id)
            return
        # 2. Sürükleme ve Seçim Başlatma
        self.drag_item_tag = char_id    # Sürüklemek için ID'yi kaydet
        self.selected_char_id = char_id # İşlemler için (Sağ tık/Sil) ID'yi güncelle
        self.last_x, self.last_y = event.x, event.y
        
        # Seçilen portreyi görsel olarak en öne çıkar
        self.canvas.tag_raise(char_id)
    def drag_portre(self, event):
        if self.drag_item_tag:
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            
            self.canvas.move(self.drag_item_tag, dx, dy)
            self.update_relationship_lines(self.drag_item_tag)
            
            self.last_x, self.last_y = event.x, event.y
            
    def stop_drag(self, event):
        """Sürükleme bittiğinde seçili nesne hafızasını temizler."""
        self.drag_item_tag = None
        # Odaklanmayı serbest bırak ki diğer nesneler algılanabilsin
        self.canvas.focus_set() 
        print("SİSTEM: Nesne bırakıldı, hafıza temizlendi.")

    def show_context_menu(self, event):
        """Sağ tıklandığında imlecin altındaki nesneyi anlık olarak seçer."""
        item_id = self.canvas.find_withtag("current")
        if item_id:
            tags = self.canvas.gettags(item_id[0])
            if "portre" in tags or "portre_isim" in tags:
                # KRİTİK: Seçili ID'yi o an imlecin altındaki nesneye zorla
                self.selected_char_id = tags[0] 
                
                self.context_menu = tk.Menu(self, tearoff=0)
                self.context_menu.add_command(label="Düzenle/Gör", command=self.open_edit_form)
                self.context_menu.add_command(label="Depoya Taşı (Sil)", command=self.move_to_depo)
                
                self.context_menu.tk_popup(event.x_root, event.y_root)

    def open_edit_form(self):
        """Sağ tıklanan karakterin düzenleme formunu açar."""
        if self.selected_char_id:
            # Buraya düzenleme formunu açma mantığı gelecek.
            print(f"BİLGİ: {self.manager.characters[self.selected_char_id].name} düzenleme formu açılıyor...")
            # İleride: NewCharacterForm'a benzer bir düzenleme penceresi açacağız.
            pass
    
    # FamilyTreeApp sınıfı içine yeni metot:

    def handle_disconnect_click(self, item_id):
        char_id = self.canvas.gettags(item_id)[0]
        
        if self.first_clicked_char_id is None:
            self.first_clicked_char_id = char_id
            self.canvas.itemconfig(item_id, outline="orange", width=3) # Farklı renk olsun
            print(f"SİLME: İlk karakter seçildi: {self.manager.characters[char_id].name}")
        
        elif self.first_clicked_char_id == char_id:
            # Aynıya tıkladıysa iptal et
            rect_id = self.drawn_characters[char_id]['rect']
            self.canvas.itemconfig(rect_id, outline="black", width=1)
            self.first_clicked_char_id = None
        
        else:
            parent_id = self.first_clicked_char_id
            child_id = char_id
            
            # 1. Manager'dan ilişkileri sil
            if child_id in self.manager.characters[parent_id].children:
                self.manager.characters[parent_id].children.remove(child_id)
            if parent_id in self.manager.characters[child_id].parents:
                self.manager.characters[child_id].parents.remove(parent_id)
            
            # 2. Canvas'tan çizgiyi sil
            line_tag = f"rel_{parent_id}_{child_id}"
            if line_tag in self.relationship_lines:
                self.canvas.delete(self.relationship_lines[line_tag])
                del self.relationship_lines[line_tag]
            
            # Görseli düzelt ve sıfırla
            first_rect = self.drawn_characters[parent_id]['rect']
            self.canvas.itemconfig(first_rect, outline="black", width=1)
            self.first_clicked_char_id = None
            print(f"BİLGİ: {parent_id} ve {child_id} arasındaki ilişki silindi.")

    def move_to_depo(self):
        """Seçilen portreyi Canvas'tan kaldırır ve Manager'da depoya taşır (Silme)."""
        if not self.selected_char_id:
            return

        char_id = self.selected_char_id
        char = self.manager.characters.get(char_id)
        
        if not char:
            return

        # 1. İlişki Çizgilerini Kaldır
        # Hem ebeveyn hem çocuk ilişkisi olan çizgileri bulup kaldırıyoruz.
        
        lines_to_delete = []
        
        # Çocuk ilişkilerini bul
        for child_id in char.children:
            lines_to_delete.append(f"rel_{char_id}_{child_id}")
            
        # Ebeveyn ilişkilerini bul
        for parent_id in char.parents:
            lines_to_delete.append(f"rel_{parent_id}_{char_id}")
            
        for line_tag in lines_to_delete:
            if line_tag in self.relationship_lines:
                self.canvas.delete(self.relationship_lines[line_tag])
                del self.relationship_lines[line_tag]

        # 2. Portreyi Canvas'tan Kaldır
        self.canvas.delete(char_id) # char_id etiketi olan tüm Canvas öğeleri (dikdörtgen/isim) silinir.
        
        # 3. Manager'da Depoya Taşı (Bu metodu manager.py'ye ekleyeceğiz!)
        self.manager.move_to_depo(char_id) 
        
        # 4. Yerel Takip Listelerinden Kaldır
        if char_id in self.drawn_characters:
            del self.drawn_characters[char_id]
        
        print(f"DEPO: Karakter {char.name} başarıyla depoya taşındı ve Canvas'tan kaldırıldı.")
        
        # İşlem bitti
        self.selected_char_id = None
    # --- İLİŞKİ KURMA MANTIKLARI ---
    
    def toggle_connect_mode(self):
        self.is_connect_mode = not self.is_connect_mode
        self.first_clicked_char_id = None 

        if self.is_connect_mode:
            self.connect_button.config(text="İlişki Kur (AÇIK)", style='Connect.TButton')
            print("MODE: İlişki Kurma modu açıldı. Ebeveyn ve ardından Çocuk portresine tıklayın.")
        else:
            self.connect_button.config(text="İlişki Kur (Kapalı)", style='TButton')
            print("MODE: İlişki Kurma modu kapatıldı. Sürükleme aktif.")

    def handle_connect_click(self, item_id):
        char_id = self.canvas.gettags(item_id)[0] 
        char_name = self.manager.characters[char_id].name
        
        if self.first_clicked_char_id is None:
            self.first_clicked_char_id = char_id
            self.canvas.itemconfig(item_id, outline="blue", width=3) 
            print(f"BAĞLANTI: Ebeveyn seçildi: {char_name}. Şimdi çocuğu seçin.")
            
        elif self.first_clicked_char_id == char_id:
            first_char_rect_id = self.drawn_characters[char_id]['rect']
            self.canvas.itemconfig(first_char_rect_id, outline="black", width=1)
            self.first_clicked_char_id = None
            print(f"BAĞLANTI: Seçim iptal edildi.")
            
        else:
            parent_id = self.first_clicked_char_id
            child_id = char_id
            
            first_char_rect_id = self.drawn_characters[parent_id]['rect']
            self.canvas.itemconfig(first_char_rect_id, outline="black", width=1)
            
            self.draw_relationship_line(parent_id, child_id)
            
            print(f"BAĞLANTI: {self.manager.characters[parent_id].name} -> {char_name} (Ebeveyn/Çocuk) olarak bağlandı.")
            
            self.first_clicked_char_id = None
            
    # --- ÇİZGİLERİ GÜNCELLEME MANTIKLARI ---
    
    def get_portrait_center(self, char_id):
        """Karakter portresinin merkez koordinatlarını döndürür."""
        rect_id = self.drawn_characters[char_id]['rect']
        coords = self.canvas.coords(rect_id) 
        center_x = (coords[0] + coords[2]) / 2
        center_y = (coords[1] + coords[3]) / 2
        return center_x, center_y

    def draw_relationship_line(self, parent_id, child_id, is_loading=False):
        """İki karakter portresi arasına çizgi çizer. Yalnızca yeni etkileşimde manager'da kaydeder."""
        
        is_already_connected = child_id in self.manager.characters[parent_id].children

        # EĞER YENİ BİR İLİŞKİ KURULUYORSA (is_loading=False)
        if not is_loading:
            if is_already_connected:
                 print("BAĞLANTI: Bu ilişki zaten mevcut.")
                 return
                 
            # İlişkiyi Manager'da kaydet (Bu kısım YÜKLEME SIRASINDA atlanmalıdır)
            self.manager.characters[parent_id].children.append(child_id)
            self.manager.characters[child_id].parents.append(parent_id)
        
        # EĞER BURAYA GELDİYSEK: ÇİZİM YAPILMALIDIR (Ya yeni kurulmuştur ya da yükleniyordur)
        
        # Koordinatları al
        x1, y1 = self.get_portrait_center(parent_id)
        x2, y2 = self.get_portrait_center(child_id)
        
        # İlişkiyi Canvas'a çiz
        line_tag = f"rel_{parent_id}_{child_id}"
        line_id = self.canvas.create_line(
            x1, y1, x2, y2, 
            fill="red", width=2, arrow=tk.LAST,
            tags=(line_tag, "relationship", parent_id, child_id) 
        )

        # Çizgiyi kaydet
        self.relationship_lines[line_tag] = line_id
        
        # Çizgilerin portrelerin arkasında kalmasını sağla
        self.canvas.tag_lower("relationship")
    def update_relationship_lines(self, char_id):
        """Belirtilen karakter ID'si hareket ettiğinde ilgili tüm çizgileri günceller."""
        char = self.manager.characters.get(char_id)
        if not char:
            return

        new_center_x, new_center_y = self.get_portrait_center(char_id)

        # Ebeveyn Bağlantılarını Güncelle (char_id, çocuğun ID'si)
        for parent_id in char.parents:
            line_tag = f"rel_{parent_id}_{char_id}"
            if line_tag in self.relationship_lines:
                parent_center_x, parent_center_y = self.get_portrait_center(parent_id)
                line_id = self.relationship_lines[line_tag]
                self.canvas.coords(line_id, parent_center_x, parent_center_y, new_center_x, new_center_y)

        # Çocuk Bağlantılarını Güncelle (char_id, ebeveynin ID'si)
        for child_id in char.children:
            line_tag = f"rel_{char_id}_{child_id}"
            if line_tag in self.relationship_lines:
                child_center_x, child_center_y = self.get_portrait_center(child_id)
                line_id = self.relationship_lines[line_tag]
                self.canvas.coords(line_id, new_center_x, new_center_y, child_center_x, child_center_y)

class DepoWindow(tk.Toplevel):
    """Silinmiş karakterleri listeleyen ve geri alma imkanı sunan pencere."""
    def __init__(self, master, manager):
        super().__init__(master)
        self.title("Silinmiş Karakter Deposu")
        self.geometry("400x450")
        self.manager = manager
        self.master = master # Ana uygulamaya erişim için
        
        self.transient(master)
        self.grab_set()
        
        self.create_widgets()
        self.load_depo_list()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Depodaki Karakterler:").pack(pady=5)
        
        # Karakter Listesi (Listbox ve Scrollbar)
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.depo_listbox = tk.Listbox(list_frame, height=15, width=50, yscrollcommand=scrollbar.set)
        self.depo_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.depo_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # --- BUTON PANELİ ---
        # Burada üstteki tekli butonu sildik, sadece aşağıdaki çerçeveyi bıraktık.
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)

        # Karakteri Geri Al Butonu
        ttk.Button(btn_frame, text="Karakteri Geri Al", command=self.restore_character).pack(side=tk.LEFT, padx=5)
        
        # Kalıcı Olarak Sil Butonu
        ttk.Button(btn_frame, text="Kalıcı Olarak Sil", command=self.delete_permanently).pack(side=tk.LEFT, padx=5)




    def load_depo_list(self):
        """Manager'dan silinmiş karakterleri Listbox'a yükler."""
        self.depo_listbox.delete(0, tk.END) # Mevcut listeyi temizle
        
        self.depo_items = {} # (index: char_id) eşleştirmesi için
        
        if not self.manager.deleted_characters:
            self.depo_listbox.insert(tk.END, "Depoda silinmiş karakter bulunmuyor.")
            return

        for index, char in enumerate(self.manager.deleted_characters.values()):
            # İsim ve tür bilgisi ile gösterim
            display_text = f"[{char.species if char.species else 'Bilinmiyor'}] {char.name}"
            self.depo_listbox.insert(tk.END, display_text)
            self.depo_items[index] = char.id # ID'yi index'e bağla
    

    # main_app.py -> DepoWindow sınıfı içine yeni metot:

    def delete_permanently(self):
        """Seçilen karakteri depodan tamamen siler (Geri dönüşü yoktur)."""
        selected_indices = self.depo_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Uyarı", "Lütfen silmek istediğiniz bir karakter seçin.")
            return

        selected_index = selected_indices[0]
        char_id = self.depo_items.get(selected_index)
        char_name = self.manager.deleted_characters[char_id].name

        # Kullanıcıya son bir kez soralım (Kritik işlem!)
        onay = messagebox.askyesno("Kalıcı Sil", f"'{char_name}' karakterini sistemden tamamen silmek istediğinize emin misiniz?\nBu işlem geri alınamaz!")
        
        if onay:
            if self.manager.permanently_delete(char_id):
                self.load_depo_list() # Listeyi tazele
                messagebox.showinfo("Başarılı", f"{char_name} başarıyla silindi.")





    def restore_character(self):
        selected_indices = self.depo_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Hata", "Lütfen bir karakter seçin.")
            return

        selected_index = selected_indices[0]
        char_id_to_restore = self.depo_items.get(selected_index)

        if char_id_to_restore:
            restored_char = self.manager.restore_from_depo(char_id_to_restore)
            if restored_char:
                # Sadece karakteri çiziyoruz, redraw_all_relationships 
                # artık bu karakter için çizgi bulamayacak (çünkü listeleri boş)
                self.master.draw_character_on_canvas(restored_char, is_loading=True)
                
                # Canvas'ı temiz tutmak için yine de bir kez tetiklemek iyidir
                self.master.redraw_all_relationships() 
                
                self.load_depo_list()
                print(f"DEPO: {restored_char.name} tertemiz bir şekilde geri alındı.")



if __name__ == "__main__":
    app = FamilyTreeApp()
    app.mainloop()