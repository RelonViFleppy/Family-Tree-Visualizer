import json
import os
from uuid import uuid4

# Kayıt dosyasının adı
DATA_FILE = "family_tree_data.json"

class Character:
    """Tek bir kurgusal karakteri temsil eder."""
    def __init__(self, name, species=None, description=None, char_id=None, parents=None, children=None, spouses=None,image_path=None):
        self.id = char_id if char_id else str(uuid4())
        self.name = name
        self.species = species
        self.description = description
        self.image_path = image_path 
        # İlişkiler: Yükleme sırasında mevcut listeleri kullan
        self.parents = parents if parents is not None else []
        self.children = children if children is not None else []
        self.spouses = spouses if spouses is not None else []

    def to_dict(self):
        """Karakter objesini JSON'a kaydedilebilecek bir sözlüğe dönüştürür."""
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "description": self.description,
            "parents": self.parents,
            "children": self.children,
            "spouses": self.spouses
        }
        
    def __str__(self):
        """Karakter objesi yazdırıldığında okunur bir çıktı verir."""
        return f"ID: {self.id[:4]}... | Ad: {self.name} | Irk: {self.species}"


class FamilyTreeManager:
    """Tüm karakter verilerini ve ilişkilerini yönetir."""
    
    def __init__(self, data_file="family_tree_data.json"):
        # 1. Önce dosya yolunu ve gerekli sözlükleri tanımla
        self.data_file = data_file
        self.characters = {}
        self.deleted_characters = {}
        self.drawn_characters_coords = {} # Koordinatlar için sözlük
        
        # 2. ANCAK HER ŞEY TANIMLANDIKTAN SONRA veriyi yükle
        self.load_all_data() 

    # manager.py -> FamilyTreeManager sınıfı içinde
    def add_character(self, name, species, description, image_path=None):
        """Yeni bir karakter oluşturur ve listeye ekler."""
    # Karakter objesini oluştururken parametre isimlerine dikkat ederek gönderiyoruz
        new_char = Character(
        name=name, 
        species=species, 
        description=description, 
        image_path=image_path  # Formdan gelen yolu buraya aktarıyoruz
    )
    
        self.characters[new_char.id] = new_char
        return new_char

    # =========================================================================
    # SİLME / DEPOLAMA MANTIĞI
    # =========================================================================
    
    # manager.py içindeki FamilyTreeManager sınıfında:

    def move_to_depo(self, char_id):
        if char_id in self.characters:
            char = self.characters.pop(char_id)
            
            # KRİTİK DÜZELTME: İlişkileri sıfırla
            # Bu karakterin diğer karakterlerdeki izlerini silmeliyiz
            for p_id in char.parents:
                if p_id in self.characters:
                    if char_id in self.characters[p_id].children:
                        self.characters[p_id].children.remove(char_id)
            
            for c_id in char.children:
                if c_id in self.characters:
                    if char_id in self.characters[c_id].parents:
                        self.characters[c_id].parents.remove(char_id)
            
            # Karakterin kendi listelerini de temizle
            char.children = []
            char.parents = []
            
            self.deleted_characters[char_id] = char
            print(f"MANAGER: {char.name} bağları koparılarak depoya taşındı.")

    def restore_from_depo(self, char_id):
        """Karakteri depodan aktif listeye geri taşır."""
        if char_id not in self.deleted_characters:
            return None
            
        char_to_restore = self.deleted_characters.pop(char_id)
        self.characters[char_id] = char_to_restore # Aktif listeye geri ekle

        # NOT: İlişkilerin temizlenmesi/yeniden kurulması GUI katmanında halledilir,
        # burada sadece veri yapısını hareket ettiriyoruz.
        
        print(f"MANAGER: {char_to_restore.name} aktif listeye geri alındı.")
        return char_to_restore
    # =========================================================================
    # KALICI KAYIT VE YÜKLEME METOTLARI
    # =========================================================================
    
    def permanently_delete(self, char_id):
        """Karakteri depodan ve sistemden tamamen siler."""
        if char_id in self.deleted_characters:
            char_name = self.deleted_characters[char_id].name
            del self.deleted_characters[char_id]
            print(f"MANAGER: {char_name} sistemden kalıcı olarak silindi.")
            return True
        return False


    def save_all_data(self, current_coords=None): # current_coords parametresini ekledik
        """Tüm karakter verilerini ve güncel koordinatları JSON'a kaydeder."""
        # Eğer dışarıdan koordinat sözlüğü gelmişse onu kullan
        if current_coords:
            self.drawn_characters_coords = current_coords

        data = {
            "characters": {},
            "deleted_characters": {}
        }

        # 1. Aktif karakterleri kaydet
        for c_id, char in self.characters.items():
            # Koordinatları al, yoksa varsayılan 50,50 kullan
            coords = self.drawn_characters_coords.get(c_id, {'x': 50, 'y': 50})
            
            data["characters"][c_id] = {
                "name": char.name,
                "species": char.species,
                "description": char.description,
                "image_path": char.image_path,
                "parents": char.parents,
                "children": char.children,
                "x": coords.get('x', 50),
                "y": coords.get('y', 50)
            }

        # 2. Depodaki karakterleri kaydet (Koordinatlara gerek yok)
        for d_id, char in self.deleted_characters.items():
            data["deleted_characters"][d_id] = {
                "name": char.name,
                "species": char.species,
                "description": char.description,
                "image_path": char.image_path,
                "parents": char.parents,
                "children": char.children
            }

        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("MANAGER: Veriler ve pozisyonlar başarıyla kaydedildi.")
        except Exception as e:
            print(f"MANAGER: Kayıt sırasında hata: {e}")

    def load_all_data(self):
        """JSON dosyasından verileri ve resim yollarını yükler."""
        if not os.path.exists(self.data_file):
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 1. Aktif Karakterleri Yükle
            for c_id, c_data in data.get("characters", {}).items():
                char = Character(
                    name=c_data["name"],
                    species=c_data.get("species"),
                    description=c_data.get("description"),
                    char_id=c_id,
                    parents=c_data.get("parents", []),
                    children=c_data.get("children", []),
                    # KRİTİK: JSON'daki resim yolunu Character objesine veriyoruz!
                    image_path=c_data.get("image_path") 
                )
                self.characters[c_id] = char
                
                # Koordinatları hafızaya al ki uygulama çizerken bilsin
                self.drawn_characters_coords[c_id] = {
                    'x': c_data.get('x', 50),
                    'y': c_data.get('y', 50)
                }

            # 2. Depodaki Karakterleri Yükle
            for d_id, d_data in data.get("deleted_characters", {}).items():
                d_char = Character(
                    name=d_data["name"],
                    species=d_data.get("species"),
                    description=d_data.get("description"),
                    char_id=d_id,
                    parents=d_data.get("parents", []),
                    children=d_data.get("children", []),
                    # Buraya da eklemeyi unutma
                    image_path=d_data.get("image_path")
                )
                self.deleted_characters[d_id] = d_char
            
            print("MANAGER: Tüm resim yolları ve veriler başarıyla yüklendi.")
            
        except Exception as e:
            print(f"MANAGER: Veri yükleme hatası: {e}")