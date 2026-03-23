# character.py

class Character:
    """Kurgusal evrendeki bir karakteri temsil eden sınıf."""
    
    def __init__(self, id, name, species=None, birth_year=None, description=""):
        # Temel Bilgiler
        self.id = id              # Benzersiz Kimlik (Arka planda kullanılacak, görünmez)
        self.name = name          # Karakterin Adı (Görselde görünecek)
        self.species = species    # Irk/Türü (Örn: "Elf", "İnsan")
        self.birth_year = birth_year # Doğum Yılı
        
        # İlişki Listeleri (İlişkileri kurmak için ID'leri tutar)
        self.spouse_ids = []      # Eş/Partner ID'lerinin listesi
        self.parent_ids = []      # Ebeveyn ID'lerinin listesi (Anne ve Baba)
        self.children_ids = []    # Çocuk ID'lerinin listesi

        # Ek Bilgiler
        self.description = description
        
    def __str__(self):
        """Karakter objesi yazdırıldığında okunur bir çıktı verir."""
        return f"ID: {self.id}, Ad: {self.name}, Irk: {self.species}, Çocuk Sayısı: {len(self.children_ids)}"

    def add_child(self, child_id):
        """Karaktere çocuk ID'si ekler."""
        if child_id not in self.children_ids:
            self.children_ids.append(child_id)
            
    def add_parent(self, parent_id):
        """Karaktere ebeveyn ID'si ekler."""
        if parent_id not in self.parent_ids:
            self.parent_ids.append(parent_id)

    def add_spouse(self, spouse_id):
        """Karaktere eş ID'si ekler."""
        if spouse_id not in self.spouse_ids:
            self.spouse_ids.append(spouse_id)

# Not: Bu dosyayı kaydettikten sonra, FamilyTreeManager dosyanızdaki import hatası çözülecektir.