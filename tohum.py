"""
tohum — 3.5: Esik homeostazi kapali. Sadece plastisite.

Egitim: esik sabit 0.5, sadece baglantilar degisir
Test:   A ve B icin ayri kopya ag, ayni baslangic
"""


import random
import json
from collections import defaultdict


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
    noronlar = [Noron(i, 0.5) for i in range(4)]
    bag = [
        {"k": 0, "h": 1, "g": 1.0},
        {"k": 0, "h": 2, "g": 1.0},
        {"k": 1, "h": 3, "g": 1.0},
        {"k": 2, "h": 3, "g": 1.0},
        {"k": 3, "h": 0, "g": 1.0},
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

        # Esik homeostazi YOK — esikler sabit 0.5

        for n in noronlar:
            n.deger *= 0.95

        if adim % 300 == 0:
            print(f"  {adim:4d} | 0->1:{bag[0]['g']:.2f} 0->2:{bag[1]['g']:.2f} "
                  f"1->3:{bag[2]['g']:.2f} 2->3:{bag[3]['g']:.2f}")

    return bag


def test(bag, girdi, tekrar=20):
    n = [Noron(i, 0.5) for i in range(4)]
    akt = [0, 0, 0, 0]

    for _ in range(tekrar):
        for x in n:
            x.enerji = 5.0
            x.deger = 0.0

        n[1 if girdi == "A" else 2].deger += 2.0

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
    print("deney 3.5: esik homeostazi kapali")
    print()

    bag = egit(adim=1500)

    print()
    print("BAGLANTILAR:")
    for b in bag:
        print(f"  {b['k']}->{b['h']}: {b['g']:.2f}")

    print()
    print("TEST (ogrenme=OFF, esik=0.5 sabit, enerji=MAX):")
    a = test(bag, "A", 20)
    b = test(bag, "B", 20)

    ta = max(sum(a), 1)
    tb = max(sum(b), 1)

    print(f"  A: N0={a[0]:3d}({a[0]/ta*100:.0f}%) N1={a[1]:3d}({a[1]/ta*100:.0f}%) "
          f"N2={a[2]:3d}({a[2]/ta*100:.0f}%) N3={a[3]:3d}({a[3]/ta*100:.0f}%)")
    print(f"  B: N0={b[0]:3d}({b[0]/tb*100:.0f}%) N1={b[1]:3d}({b[1]/tb*100:.0f}%) "
          f"N2={b[2]:3d}({b[2]/tb*100:.0f}%) N3={b[3]:3d}({b[3]/tb*100:.0f}%)")

    print()
    print("  AYRIM:")
    for i in range(4):
        af, bf = a[i]/ta*100, b[i]/tb*100
        d = af - bf
        s = "A>B" if d > 10 else ("B>A" if d < -10 else "~esit")
        print(f"    N{i}: A={af:.0f}% B={bf:.0f}% [{s}]")

    tf = sum(abs(a[i]/ta - b[i]/tb) for i in range(4))
    print()
    if tf > 0.3: print("  [OK] Net A/B ayrimi!")
    elif tf > 0.15: print("  [~] Hafif ayrim")
    else: print("  [!] Net ayrim yok")
