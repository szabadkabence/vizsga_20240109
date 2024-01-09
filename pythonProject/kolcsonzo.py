from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta

class Bicikli(ABC):
    def __init__(self, tipus, ar, allapot):
        self.tipus = tipus
        self.ar = ar
        self.allapot = allapot
        self.elerheto = True

    @abstractmethod
    def display_info(self):
        pass

class OrszagutiBicikli(Bicikli):
    def __init__(self, ar, allapot):
        super().__init__("Országúti", ar, allapot)

    def display_info(self):
        print(f"Országúti bicikli - Ár: {self.ar}, Állapot: {self.allapot}")

class HegyiBicikli(Bicikli):
    def __init__(self, ar, allapot):
        super().__init__("Hegyi", ar, allapot)

    def display_info(self):
        print(f"Hegyi bicikli - Ár: {self.ar}, Állapot: {self.allapot}")


######datum ellenorzes######
from datetime import datetime

def ervenyes_datum(datum_str):
    try:
        datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
        return datum >= datetime.today().date()
    except ValueError:
        return False


class Kolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.biciklik = []
        self.kolcsonzesek = []

    def uj_kolcsonzes(self, bicikli_tipus, kezdes_datuma, idotartam_nap):
        if not ervenyes_datum(kezdes_datuma):
            print("A megadott dátum érvénytelen.")
            return

        elerheto_bicikli = next((b for b in self.biciklik if b.tipus == bicikli_tipus and b.elerheto), None)
        if elerheto_bicikli:
            uj_kolcsonzes = Kolcsonzes(elerheto_bicikli, datetime.strptime(kezdes_datuma, "%Y-%m-%d").date(),
                                       idotartam_nap)
            self.kolcsonzesek.append(uj_kolcsonzes)
            elerheto_bicikli.elerheto = False
            print("Kölcsönzés sikeresen létrehozva.")
        else:
            print("Nincs elérhető bicikli ebben a típusban.")
    def biciklit_hozzaad(self, bicikli):
        self.biciklik.append(bicikli)

    def kolcsonzes_hozzaad(self, kolcsonzes):
        self.kolcsonzesek.append(kolcsonzes)

    def kolcsonzes_lemondas(self, kolcsonzes):
        if kolcsonzes in self.kolcsonzesek and kolcsonzes.aktív:
            kolcsonzes.aktív = False
            print("A kölcsönzés lemondva.")
        else:
            print("Nem található aktív kölcsönzés ezzel az azonosítóval.")

    def kolcsonzesek_kilistazasa(self):
        if not self.kolcsonzesek:
            print("Nincsenek kölcsönzések.")
        else:
            print(f"{self.nev} kölcsönző kölcsönzései:")
            for kolcsonzes in self.kolcsonzesek:
                kolcsonzes.kolcsonzes_info()

    def biciklik_kilistazasa(self):
        if not self.biciklik:
            print("Nincsenek biciklik a kölcsönzőben.")
        else:
            print(f"{self.nev} kölcsönző biciklik:")
            for bicikli in self.biciklik:
                bicikli.display_info()



    def kolcsonzes_lemondas(self, kolcsonzes_id):

        kolcsonzes = next((k for k in self.kolcsonzesek if k.id == kolcsonzes_id and k.aktív), None)
        if kolcsonzes:
            kolcsonzes.aktív = False
            print("A kölcsönzés sikeresen lemondva.")
        else:
            print("Nem található aktív kölcsönzés ezzel az azonosítóval.")

    def tesztadatokkal_tolt(kolcsonzo):
        # Példa biciklik létrehozása
        orszaguti1 = OrszagutiBicikli(10000, "új")
        hegyi1 = HegyiBicikli(12000, "használt")
        orszaguti2 = OrszagutiBicikli(9500, "jó állapotban")

        # Biciklik hozzáadása a kölcsönzőhöz
        kolcsonzo.biciklit_hozzaad(orszaguti1)
        kolcsonzo.biciklit_hozzaad(hegyi1)
        kolcsonzo.biciklit_hozzaad(orszaguti2)

        # Példa kölcsönzések létrehozása
        kolcsonzes1 = Kolcsonzes(orszaguti1, datetime(2024, 1, 15).date(), 3)
        kolcsonzes2 = Kolcsonzes(hegyi1, datetime(2024, 1, 20).date(), 2)

        # Kölcsönzések hozzáadása a kölcsönzőhöz
        kolcsonzo.kolcsonzes_hozzaad(kolcsonzes1)
        kolcsonzo.kolcsonzes_hozzaad(kolcsonzes2)

        # A kölcsönzött biciklik elérhetőségének frissítése
        for kolcsonzes in kolcsonzo.kolcsonzesek:
            kolcsonzes.bicikli.elerheto = False









from datetime import date


class Kolcsonzes:
    def __init__(self, bicikli, kezdes_datuma, idotartam_nap):
        self.bicikli = bicikli
        self.kezdes_datuma = kezdes_datuma
        self.idotartam_nap = idotartam_nap
        self.aktív = True

    def kolcsonzes_info(self):
        print(f"Bicikli típusa: {self.bicikli.tipus}, "
              f"Kölcsönzés kezdete: {self.kezdes_datuma}, "
              f"Kölcsönzés időtartama: {self.idotartam_nap} nap, "
              f"Állapot: {'Aktív' if self.aktív else 'Lezárva'}")



def main_menu(kolcsonzo):
    while True:
        print("\n***** Biciklikölcsönző Menü *****")
        print("1. Biciklik listázása")
        print("2. Kölcsönzés")
        print("3. Kölcsönzés lemondása")
        print("4. Kölcsönzések listázása")
        print("5. Kilépés")
        valasztas = input("Válassz egy opciót (1-5): ")

        if valasztas == '1':
            kolcsonzo.biciklik_kilistazasa()
        elif valasztas == '2':
            bicikli_tipus = input("Add meg a bicikli típusát (pl. országúti, hegyi): ")
            kezdes_datuma = input("Add meg a kölcsönzés kezdő dátumát (YYYY-MM-DD formátumban): ")
            idotartam_nap = int(input("Add meg a kölcsönzés időtartamát napokban: "))
            kolcsonzo.uj_kolcsonzes(bicikli_tipus, kezdes_datuma, idotartam_nap)

        elif valasztas == '3':
            kolcsonzes_id = int(input("Add meg a lemondandó kölcsönzés azonosítóját: "))
            kolcsonzo.kolcsonzes_lemondas(kolcsonzes_id)
        elif valasztas == '4':
            kolcsonzo.kolcsonzesek_kilistazasa()
        elif valasztas == '5':
            print("Kilépés a programból.")
            break
        else:
            print("Érvénytelen választás. Próbáld újra!")

def tesztadatokkal_tolt(kolcsonzo):
    # Példa biciklik létrehozása
    orszaguti1 = OrszagutiBicikli(10000, "új")
    hegyi1 = HegyiBicikli(12000, "használt")
    orszaguti2 = OrszagutiBicikli(9500, "jó állapotban")

    # Biciklik hozzáadása a kölcsönzőhöz
    kolcsonzo.biciklit_hozzaad(orszaguti1)
    kolcsonzo.biciklit_hozzaad(hegyi1)
    kolcsonzo.biciklit_hozzaad(orszaguti2)

    # Példa kölcsönzések létrehozása
    kolcsonzes1 = Kolcsonzes(orszaguti1, datetime(2024, 1, 15).date(), 3)
    kolcsonzes2 = Kolcsonzes(hegyi1, datetime(2024, 1, 20).date(), 2)

    # Kölcsönzések hozzáadása a kölcsönzőhöz
    kolcsonzo.kolcsonzes_hozzaad(kolcsonzes1)
    kolcsonzo.kolcsonzes_hozzaad(kolcsonzes2)

    # A kölcsönzött biciklik elérhetőségének frissítése
    for kolcsonzes in kolcsonzo.kolcsonzesek:
        kolcsonzes.bicikli.elerheto = False




kolcsonzo = Kolcsonzo("CityBike Kölcsonző")

tesztadatokkal_tolt(kolcsonzo)
main_menu(kolcsonzo)



