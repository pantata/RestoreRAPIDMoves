#!/usr/bin/env python3
import sys
import re
import os
import glob

def uprav_soubor(vstup, vystup, retract):
    with open(vstup, "r") as f:
        radky = f.readlines()

    nove_radky = []
    i = 0
    while i < len(radky):
        r = radky[i].rstrip("\n")

        if r.startswith('('):
            nove_radky.append(r)
            i += 1
            continue

        if retract in r:
            cislo = r.split()[0]
            z_hodnota = re.search(r"Z([-+]?[0-9]*\.?[0-9]+)", retract)
            if z_hodnota:
                nove_radky.append(f"{cislo} G0 Z{z_hodnota.group(1)}")
            else:
                nove_radky.append(f"{cislo} G0 Z15")

            if i + 1 < len(radky):
                r2 = radky[i + 1].rstrip("\n")
                if not r2.startswith('(') and not re.search(r"\bG[0-9]+\b", r2):
                    cislo2, *zbytek2 = r2.split()
                    nove_radky.append(f"{cislo2} G0 {' '.join(zbytek2)}")
                else:
                    nove_radky.append(r2)
                i += 1

            if i + 1 < len(radky):
                r3 = radky[i + 1].rstrip("\n")
                if not r3.startswith('('):
                    cislo3, *zbytek3 = r3.split()
                    obsah = " ".join(zbytek3)
                    m = re.search(r"Z([-+]?[0-9]*\.?[0-9]+)", obsah)
                    if m and float(m.group(1)) > 0:
                        nove_radky.append(f"{cislo3} G0 Z{m.group(1)}")
                    elif ((re.search(r"[XYZ]", obsah) and re.search(r"F", obsah))
                    and not re.search(r"\bG[0-3]\b", obsah)):
                        nove_radky.append(f"{cislo3} G1 {obsah}")
                    else:
                        nove_radky.append(r3)
                else:
                    nove_radky.append(r3)
                i += 1

            if i + 1 < len(radky):
                r4 = radky[i + 1].rstrip("\n")
                if not r4.startswith('('):
                    cislo4, *zbytek4 = r4.split()
                    obsah = " ".join(zbytek4)
                    if (re.search(r"[Z]", obsah)
                        and not re.search(r"\bG[0-3]\b", obsah)):
                        nove_radky.append(f"{cislo4} G1 {obsah}")
                    else:
                        nove_radky.append(r4)
                else:
                    nove_radky.append(r4)
                i += 1
        else:
            nove_radky.append(r)

        i += 1

    with open(vystup, "w") as f:
        for nr in nove_radky:
            f.write(nr + "\n")


if __name__ == "__main__":
    default_retract = "Z24. F#100"

    if len(sys.argv) == 1:
        soubory = glob.glob("*.ngc")
        for s in soubory:
            vystup = os.path.splitext(s)[0] + "-R.ngc"
            uprav_soubor(s, vystup, default_retract)
            print(f"Upraven: {s} -> {vystup}")
    elif len(sys.argv) == 4:
        vstup = sys.argv[1]
        vystup = sys.argv[2]
        retract = sys.argv[3]
        uprav_soubor(vstup, vystup, retract)
    elif len(sys.argv) == 3:
        vstup = sys.argv[1]
        vystup = sys.argv[2]
        uprav_soubor(vstup, vystup, default_retract)
    else:
        print("Použití:")
        print(f"  Bez parametrů: upraví všechny *.ngc v adresáři (retract = {default_retract})")
        print(f"  script.py vstup.nc vystup.nc          (retract = {default_retract})")
        print("  script.py vstup.nc vystup.nc 'Zxx. F#yy'  (vlastní retract)")
        sys.exit(1)
