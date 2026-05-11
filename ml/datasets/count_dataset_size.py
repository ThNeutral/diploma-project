import os
import matplotlib.pyplot as plt
import numpy as np
 
 
# ── Configuration ────────────────────────────────────────────────────────────
TRAIN_DIR = "../data/PlantVillage/train"   # path to your train split folder
# ─────────────────────────────────────────────────────────────────────────────
 
 
def count_samples(root_dir: str) -> dict[str, int]:
    """Return {class_name: sample_count} for an ImageFolder-style directory."""
    counts = {}
    if not os.path.isdir(root_dir):
        raise FileNotFoundError(f"Directory not found: {root_dir!r}")
    for class_name in sorted(os.listdir(root_dir)):
        class_path = os.path.join(root_dir, class_name)
        if not os.path.isdir(class_path):
            continue
        n = sum(
            1 for f in os.listdir(class_path)
            if os.path.isfile(os.path.join(class_path, f))
        )
        counts[class_name] = n
    return counts
 
 
def plot_distribution(train_counts: dict) -> None:
    classes    = list(train_counts.keys())
    train_vals = [train_counts.get(c, 0) for c in classes]
    n          = len(classes)
    x          = np.arange(n)
 
    # ── Style ─────────────────────────────────────────────────────────────────
    plt.rcParams.update({
        "font.family":       "DejaVu Sans",
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "axes.grid":         True,
        "grid.linestyle":    "--",
        "grid.alpha":        0.4,
    })
 
    fig, ax = plt.subplots(figsize=(max(18, n * 0.55), 8))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#0f1117")
    ax.tick_params(colors="#cccccc")
    ax.yaxis.label.set_color("#cccccc")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333333")
    ax.yaxis.grid(True, color="#333333", linestyle="--", linewidth=0.6)
    ax.xaxis.grid(False)
 
    TRAIN_COLOR = "#4fc3f7"
 
    # ── Bars ──────────────────────────────────────────────────────────────────
    ax.bar(x, train_vals, width=0.9, color=TRAIN_COLOR, alpha=0.85, zorder=3)
    ax.set_ylabel("Sample count", fontsize=11, color="#cccccc")
    ax.set_title(
        "PlantVillage — Samples per Class (Train)",
        fontsize=15, fontweight="bold", color="#ffffff", pad=14,
    )
 
    # ── Legend ────────────────────────────────────────────────────────────────
    from matplotlib.patches import Patch
    ax.legend(
        handles=[Patch(facecolor=TRAIN_COLOR, alpha=0.85, label="Train")],
        fontsize=10, framealpha=0.15,
        labelcolor="#cccccc", facecolor="#1a1a2e",
    )
 
    # ── Mean line ─────────────────────────────────────────────────────────────
    mean_val = np.mean(train_vals)
    ax.axhline(mean_val, color=TRAIN_COLOR, linewidth=1.2,
               linestyle=":", alpha=0.7, zorder=4)
    ax.text(
        n - 0.5, mean_val * 1.02,
        f"mean {mean_val:,.0f}",
        color=TRAIN_COLOR, fontsize=8.5, alpha=0.85, ha="right",
    )
 
    # ── X-axis labels ─────────────────────────────────────────────────────────
    ax.set_xticks(x)
    ax.set_xticklabels(classes, rotation=55, ha="right",
                       fontsize=7.5, color="#cccccc")
 
    # ── Save ──────────────────────────────────────────────────────────────────
    plt.tight_layout()
    out_path = "dataset_distribution.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    print(f"Saved → {out_path}")
    plt.show()
 
 
if __name__ == "__main__":
    print(f"Scanning train → {TRAIN_DIR!r}")
    train_counts = count_samples(TRAIN_DIR)
    print(f"Found {len(train_counts)} classes in train split.")
    plot_distribution(train_counts)