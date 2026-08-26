# tohum

Bos bir beyin. Hedef yok, amaç yok. Sadece var.

Deneyimle kendi baglantilarini olusturur.

---

## Son deney: 3.5 — Esik homeostazi kapali, sadece plastisite

### Egitim
- 1500 adim rastgele A/B girdisi
- Esik homeostazi: KAPALI (esik sabit 0.5)
- Plastisite: sadece baglantilar degisir
- Enerji rezervi: her noronun kendi enerjisi var

### python tohum.py ciktisi:
```
deney 3.5: esik homeostazi kapali

     0 | 0->1:1.00 0->2:1.00 1->3:1.00 2->3:1.00
   300 | 0->1:1.24 0->2:1.18 1->3:2.50 2->3:2.50
   600 | 0->1:1.24 0->2:1.18 1->3:2.50 2->3:2.50
   900 | 0->1:1.24 0->2:1.18 1->3:2.50 2->3:2.50
  1200 | 0->1:1.24 0->2:1.18 1->3:2.50 2->3:2.50

BAGLANTILAR:
  0->1: 1.24
  0->2: 1.18
  1->3: 2.50
  2->3: 2.50
  3->0: 2.50

TEST (ogrenme=OFF, esik=0.5 sabit, enerji=MAX):
  A: N0= 20(17%) N1= 40(33%) N2= 20(17%) N3= 40(33%)
  B: N0= 20(17%) N1= 20(17%) N2= 40(33%) N3= 40(33%)

  AYRIM:
    N0: A=17% B=17% [~esit]
    N1: A=33% B=17% [A>B]
    N2: A=17% B=33% [B>A]
    N3: A=33% B=33% [~esit]

  [OK] Net A/B ayrimi!
```

### Sonuc
Sistem A ve B icin farkli ic aktivasyon paternleri olusturmus.
Ogrenme kapali, enerji sabit, esik sabit olmasina ragmen fark var.
Bu, deneyim sonucu olusan baglanti yapisinin girdi-spesifik davransi urettigini gosteriyor.

---

## Deney gecmisi

| Deney | Aciklama | Sonuc |
|-------|----------|-------|
| 1.0 | 3 noron halka | Sistem oldu |
| 2.0 | Dengeli döngü | Enerji sabit |
| 2.1 | Plastisite | Enerji patladi |
| 2.3 | Rekabet + geri besleme | Kalici tercih olustu |
| 2.8 | Esik homeostazi | 600 adim canli ama enerji patladi |
| 3.0 | Noron-basina enerji rezervi | 593/600 canli, dengeye geldi |
| 3.1 | Disaridan A/B girdisi | Sistem canli kaldi |
| 3.2 | Girdiye bagli plastisite | Baglantilar farklasti |
| 3.3 | A/B testi | Net fark olustu |
| 3.4 | Ogrenme kapali (esikli) | Ayrim gorunmedi |
| **3.5** | **Ogrenme kapali (esiksiz)** | **NET A/B AYRIMI** |

---

## Calistir

```
python tohum.py
```
