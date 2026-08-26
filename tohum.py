"""
tohum — 3.6b: Egitimde sessiz kalan 3. sensor.

5 giris sensoru + 3 ic noron = 8 noron
Egitim: YALNIZCA sens0(A) ve sens1(B) aktif
        sens2(C) hic kullanilmiyor
Test:   A, B, C icin ayri kopya aglar
        C = daha once hic aktif olmamis sens2
"""


import random


class Noron:
    def __init__(self, idx, esik=0.5):
        self.idx = idx
        self.deger = 0.0
        self.esik = esik
        self.enerji = 5.0
        self.max_enerji = 5.0

    def atesle(self):
        self.enerji -= 0.5
        self.enerji = max(0, self.enerji)
        self.deger = 0.0

    def toparla(self):
        if self.deger < self.esik:
            self.enerji += 0.05
            self.enerji = min(self.max_enerji, self.enerji)

    def aktif_mi(self):
        return self.deger > self.esik and self.enerji > 0.1


def egit(adim=2000):
    # 8 noron:
    # 0-4: sens0(A), sens1(B), sens2(C-sessiz), sens3(bos), sens4(bos)
    # 5: ic noron alpha
    # 6: ic noron beta
    # 7: cikis noron
    n = [Noron(i) for i in range(8)]
    bag = [
        {"k": 0, "h": 5, "g": 1.0},   # A -> alpha
        {"k": 1, "h": 6, "g": 1.0},   # B -> beta
        {"k": 5, "h": 7, "g": 1.0},   # alpha -> cikis
        {"k": 6, "h": 7, "g": 1.0},   # beta -> cikis
        {"k": 7, "h": 5, "g": 0.5},   # cikis -> alpha (geri besleme)
        {"k": 7, "h": 6, "g": 0.5},   # cikis -> beta (geri besleme)
    ]
    n[0].deger = 1.5
    son_ates = {}

    for adim in range(adim):
        girdi = "A" if random.random() < 0.5 else "B"
        n[0 if girdi == "A" else 1].deger += 2.0

        ates = []
        for x in n:
            if x.aktif_mi():
                ates.append(x.idx)
                son_ates[x.idx] = adim

        for b in bag:
            if b["k"] in ates:
                n[b["h"]].deger += n[b["k"]].deger * b["g"]

        for x in n:
            if x.idx in ates: x.atesle()
            else: x.toparla()

        for b in bag:
            k, h = b["k"], b["h"]
            if k in son_ates and h in son_ates:
                f = son_ates[h] - son_ates[k]
                if 0 < f <= 3: b["g"] += 0.03
                elif f > 5: b["g"] -= 0.01
            elif k in son_ates and adim - son_ates[k] > 3:
                b["g"] -= 0.01
            b["g"] = max(0.05, min(2.5, b["g"]))

        for x in n:
            x.deger *= 0.95

        if adim % 400 == 0:
            g_str = " ".join(f"{b['k']}->{b['h']}:{b['g']:.2f}" for b in bag)
            print(f"  {adim:4d} | {g_str}")

    return bag


def test(bag, sens_noron, tekrar=20):
    n = [Noron(i) for i in range(8)]
    akt = [0] * 8

    for _ in range(tekrar):
        for x in n:
            x.enerji = 5.0
            x.deger = 0.0

        n[sens_noron].deger += 2.0

        for _ in range(8):
            ates = [x.idx for x in n if x.aktif_mi()]
            for b in bag:
                if b["k"] in ates:
                    n[b["h"]].deger += n[b["k"]].deger * b["g"]
            for x in n:
                if x.idx in ates: x.atesle()
                else: x.toparla()
                x.deger *= 0.95
            for i in ates:
                akt[i] += 1

    return akt


if __name__ == "__main__":
    print("deney 3.6b: egitimde sessiz 3. sensor")
    print("  5 sensor(0-4) + 2 ic(5,6) + 1 cikis(7) = 8 noron")
    print("  egitim: sens0(A) + sens1(B) aktif, sens2(C) SESSiZ")
    print("  test: A(sens0), B(sens1), C(sens2)")
    print()

    bag = egit(adim=2000)

    print()
    print("BAGLANTILAR:")
    for b in bag:
        print(f"  {b['k']}->{b['h']}: {b['g']:.2f}")

    print()
    print("TEST:")
    a = test(bag, 0, 20)
    b = test(bag, 1, 20)
    c = test(bag, 2, 20)

    isimler = ["sens0", "sens1", "sens2", "sens3", "sens4", "alpha", "beta", "cikis"]
    for isim, veri in [("A(sens0)", a), ("B(sens1)", b), ("C(sens2)", c)]:
        t = max(sum(veri), 1)
        pct = " ".join(f"{isimler[i]}={veri[i]/t*100:.0f}%" for i in range(8))
        print(f"  {isim}: {pct}")

    print()
    print("AYRIM (A/B icin onemli noronlar: alpha=5, beta=6, cikis=7):")
    for i in [5, 6, 7]:
        af = a[i]/max(sum(a),1)*100
        bf = b[i]/max(sum(b),1)*100
        cf = c[i]/max(sum(c),1)*100
        print(f"  {isimler[i]:5s}: A={af:.0f}% B={bf:.0f}% C={cf:.0f}%")

    print()
    # C farkli mi A/B'den?
    ic_a = tuple(round(a[i]/max(sum(a),1)*100) for i in [5,6,7])
    ic_b = tuple(round(b[i]/max(sum(b),1)*100) for i in [5,6,7])
    ic_c = tuple(round(c[i]/max(sum(c),1)*100) for i in [5,6,7])

    print(f"  A ic patern: {ic_a}")
    print(f"  B ic patern: {ic_b}")
    print(f"  C ic patern: {ic_c}")

    if ic_c == ic_a or ic_c == ic_b:
        print("  [!] C mevcut bir paterni kopyaliyor")
    else:
        print("  [OK] C kendine ait farkli bir patern olusturdu")
