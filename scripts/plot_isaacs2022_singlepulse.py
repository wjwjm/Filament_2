from __future__ import annotations
import argparse
import numpy as np
import matplotlib.pyplot as plt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("npz40")
    ap.add_argument("npz120")
    ap.add_argument("--out", default="ne_peak_vs_z.png")
    args = ap.parse_args()

    d40 = np.load(args.npz40)
    d120 = np.load(args.npz120)
    plt.plot(d40["z_from_focus_cm"], d40["ne_peak_m3"], label="40 fs")
    plt.plot(d120["z_from_focus_cm"], d120["ne_peak_m3"], label="120 fs")
    plt.xlabel("distance from vacuum focus [cm]")
    plt.ylabel("peak electron density [m^-3]")
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.out, dpi=160)
    print(f"saved {args.out}")

if __name__ == "__main__":
    main()
