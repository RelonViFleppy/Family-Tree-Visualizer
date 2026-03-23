import networkx as nx
import json
from character import Character# Varsayalım ki Character sınıfı ayrı bir dosyada (character.py)

class FamilyTreeManager:
    def __init__(self):
        # Tüm aktif karakterler (ID -> Character objesi)
        self.active_characters = {}
        # Depo/Yedek: Silinen karakterler buraya taşınır
        self.deleted_characters = {} 
        # NetworkX Grafik objesi
        self.graph = nx.DiGraph() 

    # --- Karakter Ekleme / Oluşturma (Hedef 3) ---
    def add_character(self, name, species=None, birth_year=None, description=""):
        # Basit bir ID üretme mantığı (Gerçek uygulamada daha sağlam olmalı)
        new_id = f"C{len(self.active_characters) + len(self.deleted_characters) + 1:04d}"
        
        new_char = Character(new_id, name, species, birth_year, description)
        self.active_characters[new_id] = new_char
        self.graph.add_node(new_id, label=name) # Grafiğe düğüm ekleniyor (Hedef 1)
        return new_char

    # --- Karakter Silme / Depolama (Hedef 4) ---
    def delete_character(self, character_id):
        if character_id in self.active_characters:
            char_to_move = self.active_characters.pop(character_id)
            self.deleted_characters[character_id] = char_to_move
            
            # Grafikten düğümü kaldır
            if self.graph.has_node(character_id):
                self.graph.remove_node(character_id)
            
            # İlişkileri de temizle (Daha sonra detaylandırılacak)
            print(f"Karakter {char_to_move.name} depoya taşındı.")
            return True
        return False

    # --- Karakteri Depodan Geri Alma (Hedef 4) ---
    def restore_character(self, character_id):
        if character_id in self.deleted_characters:
            char_to_restore = self.deleted_characters.pop(character_id)
            self.active_characters[character_id] = char_to_restore
            self.graph.add_node(character_id, label=char_to_restore.name)
            
            # İlişkileri de geri yükle (Daha sonra detaylandırılacak)
            print(f"Karakter {char_to_restore.name} geri yüklendi.")
            return True
        return False


    # --- İlişki Kurma (Hedef 5) ---
    def create_relationship(self, parent_id, child_id, relation_type="parent_child"):
        # Temel kontrol
        if parent_id not in self.active_characters or child_id not in self.active_characters:
            return False # Karakterler aktif listede yoksa bağlanamaz

        # Karakter objelerini güncelle
        # ... (burada parent objesinin children listesine child_id eklenir)
        # ... (burada child objesinin parent listesine parent_id eklenir)
        
        # NetworkX'e kenar (ilişki) ekle
        self.graph.add_edge(parent_id, child_id, relation=relation_type)
        print(f"{self.active_characters[parent_id].name} -> {self.active_characters[child_id].name} ilişkisi kuruldu.")
        return True