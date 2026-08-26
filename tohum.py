"""
tohum — 3.6a: C genelleme testi.

Egitim: 1500 adim A/B (C yok)
Test:   A, B, C icin ayri kopya aglar
        Ogrenme=OFF, esik=0.5 sabit, enerji=MAX

C daha once hic gormedigi bir girdi.
Mevcut yapiyla nasil tepki veriyor?
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


def egit(adim=1500):
    # 5 noron: N0(init), N1(A), N2(B), N3(cikis), N4(geri besleme)
    noronlar = [Noron(i) for i in range(5)]
    bag = [
        {"k": 0, "h": 1, "g": 1.0},
        {"k": 0, "h": 2, "g": 1.0},
        {"k": 1, "h": 3, "g": 1.0},
        {"k": 2, "h": 3, "g": 1.0},
        {"k": 3, "h": 4, "g": 1.0},
        {"k": 4, "h": 0, "g": 1.0},
    ]
    noronlar[0].deger = 1.5
    son_ates = {}

    for adim in range(adim):
        girdi = "A" if random.random() < 0.5 else "B"
        noronlar[1 if girdi == "A" else 2].deger += 2.0

        ates = []
        for n in noronlar:
            if n.aktif_mi():
                ates.append(n.idx)
                son_ates[n.idx] = adim

        for b in bag:
            if b["k"] in ates:
                noronlar[b["h"]].deger += noronlar[b["k"]].deger * b["g"]

        for n in noronlar:
            if n.idx in ates: n.atesle()
            else: n.toparla()

        for b in bag:
            k, h = b["k"], b["h"]
            if k in son_ates and h in son_ates:
                f = son_ates[h] - son_ates[k]
                if 0 < f <= 3: b["g"] += 0.03
                elif f > 5: b["g"] -= 0.01
            elif k in son_ates and adim - son_ates[k] > 3:
                b["g"] -= 0.01
            b["g"] = max(0.05, min(2.5, b["g"]))

        for n in noronlar:
            n.deger *= 0.95

        if adim % 300 == 0:
            print(f"  {adim:4d} | 0->1:{bag[0]['g']:.2f} 0->2:{bag[1]['g']:.2f} "
                  f"1->3:{bag[2]['g']:.2f} 2->3:{bag[3]['g']:.2f} "
                  f"3->4:{bag[4]['g']:.2f} 4->0:{bag[5]['g']:.2f}")

    return bag


def test(bag, girdi, girdi_noron, tekrar=20):
    n = [Noron(i) for i in range(5)]
    akt = [0, 0, 0, 0, 0]

    for _ in range(tekrar):
        for x in n:
            x.enerji = 5.0
            x.deger = 0.0

        n[girdi_noron].deger += 2.0

        for _ in range(5):
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
    print("deney 3.6a: C genelleme testi")
    print("  egitim: A/B (C yok)")
    print("  test: A, B, C (ayri kopya aglar)")
    print()

    bag = egit(adim=1500)

    print()
    print("BAGLANTILAR:")
    for b in bag:
        print(f"  {b['k']}->{b['h']}: {b['g']:.2f}")

    print()
    print("TEST (ogrenme=OFF, esik=0.5, enerji=MAX):")
    a = test(bag, "A", 1, 20)
    b = test(bag, "B", 2, 20)
    c = test(bag, "C", 3, 20)

    for isim, veri in [("A", a), ("B", b), ("C", c)]:
        t = max(sum(veri), 1)
        pct = [f"N{i}={veri[i]/t*100:.0f}%" for i in range(5)]
        print(f"  {isim}: {' '.join(pct)}")

    print()
    print("  AYRIM (3'luluk):")
    for i in range(5):
        af = a[i]/max(sum(a),1)*100
        bf = b[i]/max(sum(b),1)*100
        cf = c[i]/max(sum(c),1)*100
        fark_ab = af - bf
        fark_ac = af - cf
        fark_bc = bf - cf

        if abs(fark_ab) > 10:
            sab = "A>B" if fark_ab > 0 else "B>A"
        else:
            sab = "~"
        if abs(fark_ac) > 10:
            sac = "A>C" if fark_ac > 0 else "C>A"
        else:
            sac = "~"
        if abs(fark_bc) > 10:
            sbc = "B>C" if fark_bc > 0 else "C>B"
        else:
            sbc = "~"

        print(f"    N{i}: A={af:.0f}% B={bf:.0f}% C={cf:.0f}% [{sab} {sac} {sbc}]")

    print()
    # C farkli mi?
    a_patern = tuple(round(a[i]/max(sum(a),1)*100) for i in range(5))
    b_patern = tuple(round(b[i]/max(sum(b),1)*100) for i in range(5))
    c_patern = tuple(round(c[i]/max(sum(c),1)*100) for i in range(5))

    if c_patern == a_patern:
        print("  [!] C ayni A gibi davraniyor")
    elif c_patern == b_patern:
        print("  [!] C ayni B gibi davraniyor")
    else:
        print("  [OK] C farkli bir patern gosteriyor!")
