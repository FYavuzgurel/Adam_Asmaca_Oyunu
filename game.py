import random


class Game:
    HUMAN_GUESSER = 1
    MACHINE_GUESSER = 2
    tried = 0
    allowed_mods = [HUMAN_GUESSER, MACHINE_GUESSER]
    alphabet = "abcçdefgğhıijklmnoöprsştuüvyz"

    def choose_length(self):    # Kullanıcı türüne göre kelime uzunluklarını belirleyen fonksiyon
        if self.mod == self.HUMAN_GUESSER:
            self.length = int(input("Harf sayisini girin: "))
        if self.mod == self.MACHINE_GUESSER:
            self.length = random.randint(4, 12) # 4 karakter ile 12 karakter arasında bir kelime tahmin eder

    def select_mode(self): # Kullanıcı türünü belirleyen fonksiyon
        mod = int(input("Mod seçiminizi yapın:\n1: Bilgisayar kelimeyi belirliyor\n2: Kullanici kelimeyi belirliyor:\n"))
        if mod not in self.allowed_mods:
            print("Doğru bir mod seçiniz.")
            self.select_mode()
        else:
            self.mod = mod

    def init_word(self):
        if self.mod == self.HUMAN_GUESSER: # kullanıcı insan ise text dosyasındaki kelimeleri listeye aktarır
            lines = open("turkish_dictionary.txt", encoding="utf-8").readlines() # Türkçe karakter desteği sağlaması için utf-8 kullanıldı
            word_list = []
            for line in lines:
                word = line.split(" ")[0] # text dosyasında birinci kelimeler ayrıştırıldı
                if len(word) == self.length: # istenilen karakter sayısında olan kelimeler içeri aktarıldı
                    word_list.append(word)
            self.chosen_word = random.choice(word_list) # rastgele bir kelime seçildi
        self.word = "_" * self.length # kelime gizlendi

    def guess_letter(self): # Kelime tahmin eden fonksiyon
        if self.mod == self.HUMAN_GUESSER:
            return input("Harf tahmin edin: ")
        if self.mod == self.MACHINE_GUESSER:
            letter = random.choice(self.alphabet) # Alfabeden rastgele harf seçimi yapılıyor
            self.alphabet = self.alphabet.replace(letter, "") # Bir kez tahmin edilen kelime tekrar edilmemesi için alfabe listesinden çıkartılıyor
            return letter

    def check_letter(self, letter): # girilen kelimenin kontrolünün sağlandığı fonksiyon
        if self.mod == self.HUMAN_GUESSER: #tahmin eden insan ise 
            if letter in self.chosen_word: 
                print("Bildiniz!")
                for i, character in enumerate(self.chosen_word):
                    if character == letter:
                        self.word = self.word[:i] + character + self.word[i + 1:]
                return True
            else:
                return False
        if self.mod == self.MACHINE_GUESSER: #tahmin eden bilgisayar ise 
            print("Harf tahmin ediyorum:", letter)
            correct = input("Bildim mi? (e/h): ")
            if correct == "e":
                amount = int(input("Kac harf bildim: "))
                for i in range(amount):
                    index = int(input(str(i + 1) + ". harfin sırası: ")) - 1
                    self.word = self.word[:index] + letter + self.word[index + 1:]
                return True
            else:
                return False

    def win(self): # Kazandı çıktısı veren fonksiyonn
        if self.mod == self.HUMAN_GUESSER:
            print("Kazandiniz! Kelime:", self.word)
        if self.mod == self.MACHINE_GUESSER:
            print("Kazandim! Kelime:", self.word)

    def lose(self): # Kaybetti çıktısı veren fonksiyonn
        if self.mod == self.HUMAN_GUESSER:
            print("Kaybettiniz! Kelime:", self.chosen_word)
        if self.mod == self.MACHINE_GUESSER:
            print("Kaybettim!")

    def start(self): # Fonksiyonlara Start verilen fonksiyon
        self.select_mode()
        self.choose_length()
        self.init_word()
        while self.tried < self.MAX_TRY: # Maksimum deneme hakkı aşılmadı ise döngü devam eder
            print(self.word)
            letter = self.guess_letter()
            found = self.check_letter(letter)
            if found:   # tahmin edilen kelimenin içerisinde '_' karakteri yoksa oyun kazanılır
                if "_" not in self.word:
                    self.win()
                    break
            else:
                self.tried += 1 # eğer yanlış tahmin edilirse hata sayısı +1 artar
        if self.tried == self.MAX_TRY:
            self.lose()

    def __init__(self, max_try=10): # initialize fonksiyonu max değeri girilir 
        self.MAX_TRY = max_try