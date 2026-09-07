#!/usr/bin/env python3
"""Generate all 6 figures for the ENIP paper."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR.mkdir(exist_ok=True)

# Color palette
COLORS = {
    'primary': '#2563eb',    # Blue
    'secondary': '#7c3aed',  # Purple
    'accent': '#059669',     # Green
    'warning': '#d97706',    # Amber
    'gray': '#6b7280',       # Gray
    'light': '#f3f4f6',      # Light gray
    'white': '#ffffff',
    'bg': '#fafafa',
}

LAYER_COLORS = ['#3b82f6', '#8b5cf6', '#10b981']  # Blue, Purple, Green


def fig1_three_layer_framework():
    """Figure 1: Three-Layer Editorial Competence Framework (Block Diagram)"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_facecolor(COLORS['bg'])
    fig.patch.set_facecolor(COLORS['white'])

    # Title
    ax.text(6, 9.5, 'Three-Layer Editorial Competence Framework',
            fontsize=16, fontweight='bold', ha='center', va='center')

    # Three layers (stacked boxes)
    layers = [
        ('Layer 3: Substantive', 'Fact verification, style adaptation\nDevelopmental editing', 'Kurator', COLORS['accent'], 1),
        ('Layer 2: Structural', 'TEEL+ structure, transitions\nDepth model, coherence', 'Arsitek', COLORS['secondary'], 2),
        ('Layer 1: Mechanical', 'PUEBI/KBBI proofreading\nSpelling, punctuation, typography', 'Tukang Bangunan', COLORS['primary'], 3),
    ]

    for i, (title, desc, analogy, color, y) in enumerate(layers):
        # Main box
        rect = FancyBboxPatch((1, y * 2.5 - 0.8), 7, 2.2,
                              boxstyle="round,pad=0.1",
                              facecolor=color, alpha=0.15,
                              edgecolor=color, linewidth=2)
        ax.add_patch(rect)

        # Layer title
        ax.text(4.5, y * 2.5 + 0.7, title,
                fontsize=13, fontweight='bold', ha='center', va='center',
                color=color)

        # Description
        ax.text(4.5, y * 2.5 - 0.1, desc,
                fontsize=10, ha='center', va='center',
                color='#374151', linespacing=1.4)

        # Analogy box (right side)
        analogy_box = FancyBboxPatch((8.5, y * 2.5 - 0.5), 3, 1.6,
                                     boxstyle="round,pad=0.1",
                                     facecolor=color, alpha=0.08,
                                     edgecolor=color, linewidth=1.5,
                                     linestyle='--')
        ax.add_patch(analogy_box)
        ax.text(10, y * 2.5 + 0.3, analogy,
                fontsize=11, fontweight='bold', ha='center', va='center',
                color=color)
        ax.text(10, y * 2.5 - 0.2, 'Analogi',
                fontsize=9, ha='center', va='center', color=COLORS['gray'])

        # Arrow from layer to analogy
        ax.annotate('', xy=(8.3, y * 2.5), xytext=(7.2, y * 2.5),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

    # Legend
    ax.text(6, 0.8, 'Hierarki: Makna > Kejelasan > Gaya > Estetika > Konvensi',
            fontsize=10, ha='center', va='center', style='italic',
            color=COLORS['gray'])

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig1_three_layer_framework.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'fig1_three_layer_framework.pdf', bbox_inches='tight')
    plt.close()
    print('Created fig1_three_layer_framework.png/pdf')


def fig2_style_engine():
    """Figure 2: Style Engine with Hybrid Weighting (Flowchart)"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_facecolor(COLORS['bg'])
    fig.patch.set_facecolor(COLORS['white'])

    # Title
    ax.text(7, 9.5, 'Style Engine with Hybrid Weighting',
            fontsize=16, fontweight='bold', ha='center', va='center')

    # 5 base styles (top row)
    styles = ['Akademis\nFormal', 'Jurnalistik\nInformatif', 'Naratif\nSastrawi',
              'Populer-\nEdukatif', 'Persuasif-\nArgumentatif']
    style_colors = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981']

    for i, (style, color) in enumerate(zip(styles, style_colors)):
        x = 1.5 + i * 2.5
        rect = FancyBboxPatch((x - 0.9, 7.2), 1.8, 1.6,
                              boxstyle="round,pad=0.1",
                              facecolor=color, alpha=0.15,
                              edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x, 8, style, fontsize=9, fontweight='bold',
                ha='center', va='center', color=color)

    # Hybrid mode box (center)
    hybrid_box = FancyBboxPatch((3, 4.5), 8, 2,
                                boxstyle="round,pad=0.2",
                                facecolor=COLORS['primary'], alpha=0.1,
                                edgecolor=COLORS['primary'], linewidth=2)
    ax.add_patch(hybrid_box)
    ax.text(7, 6, 'Mode Hybrid', fontsize=14, fontweight='bold',
            ha='center', va='center', color=COLORS['primary'])
    ax.text(7, 5.2, 'Primary 60%  |  Secondary 30%  |  Tertiary 10%',
            fontsize=11, ha='center', va='center', color='#374151')

    # Arrows from styles to hybrid
    for i in range(5):
        x = 1.5 + i * 2.5
        ax.annotate('', xy=(7, 6.8), xytext=(x, 7.2),
                    arrowprops=dict(arrowstyle='->', color='#9ca3af', lw=1.2))

    # 7 micro parameters (bottom row)
    params = ['Formalitas\n1-10', 'Panjang\nKalimat', 'Densitas\nIstilah',
              'Frekuensi\nAnalogi', 'Pertanyaan\nRetoris', 'Toleransi\nPoetika',
              'Perspektif\nNaratif']

    for i, param in enumerate(params):
        x = 1 + i * 1.8
        rect = FancyBboxPatch((x - 0.7, 1.8), 1.4, 1.4,
                              boxstyle="round,pad=0.1",
                              facecolor=COLORS['accent'], alpha=0.1,
                              edgecolor=COLORS['accent'], linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, 2.5, param, fontsize=8, ha='center', va='center',
                color=COLORS['accent'])

    # Label
    ax.text(7, 3.8, '7 Parameter Mikro', fontsize=11, fontweight='bold',
            ha='center', va='center', color=COLORS['accent'])

    # Arrows from hybrid to params
    for i in range(7):
        x = 1 + i * 1.8
        ax.annotate('', xy=(x, 3.2), xytext=(7, 4.3),
                    arrowprops=dict(arrowstyle='->', color='#9ca3af', lw=1,
                                    connectionstyle='arc3,rad=0.1'))

    # Output
    out_box = FancyBboxPatch((4, 0.2), 6, 1.2,
                             boxstyle="round,pad=0.1",
                             facecolor=COLORS['warning'], alpha=0.15,
                             edgecolor=COLORS['warning'], linewidth=2)
    ax.add_patch(out_box)
    ax.text(7, 0.8, 'Output: Clean | Edit+Catatan | Track Changes | Konsultasi',
            fontsize=10, ha='center', va='center', color=COLORS['warning'])

    ax.annotate('', xy=(7, 1.4), xytext=(7, 1.8),
                arrowprops=dict(arrowstyle='->', color=COLORS['warning'], lw=1.5))

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig2_style_engine.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'fig2_style_engine.pdf', bbox_inches='tight')
    plt.close()
    print('Created fig2_style_engine.png/pdf')


def fig3_workflow():
    """Figure 3: Seven-Stage Editing Workflow (Flow Diagram)"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 6))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_facecolor(COLORS['bg'])
    fig.patch.set_facecolor(COLORS['white'])

    # Title
    ax.text(8, 5.5, 'Seven-Stage Editing Workflow',
            fontsize=16, fontweight='bold', ha='center', va='center')

    stages = [
        ('1. Intake &\nDiagnosis', '#3b82f6'),
        ('2. Substantive\nEditing', '#8b5cf6'),
        ('3. Structural\nEditing', '#ec4899'),
        ('4. Sentence\nEditing', '#f59e0b'),
        ('5. Proofreading', '#10b981'),
        ('6. Enhancement', '#06b6d4'),
        ('7. Output &\nEditor Notes', '#6366f1'),
    ]

    box_width = 1.8
    gap = 0.35
    start_x = 0.5

    for i, (stage, color) in enumerate(stages):
        x = start_x + i * (box_width + gap)
        rect = FancyBboxPatch((x, 2.5), box_width, 2.2,
                              boxstyle="round,pad=0.15",
                              facecolor=color, alpha=0.15,
                              edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + box_width / 2, 3.6, stage,
                fontsize=9, fontweight='bold', ha='center', va='center',
                color=color)

        # Arrow to next stage
        if i < len(stages) - 1:
            ax.annotate('', xy=(x + box_width + gap - 0.05, 3.6),
                        xytext=(x + box_width + 0.05, 3.6),
                        arrowprops=dict(arrowstyle='->', color='#9ca3af', lw=2))

    # Output modes (bottom)
    modes = ['Clean Edit', 'Edit + Catatan', 'Track Changes', 'Konsultasi']
    mode_colors = ['#3b82f6', '#8b5cf6', '#ec4899', '#10b981']

    for i, (mode, color) in enumerate(zip(modes, mode_colors)):
        x = 2 + i * 3.5
        rect = FancyBboxPatch((x - 0.9, 0.5), 1.8, 1.2,
                              boxstyle="round,pad=0.1",
                              facecolor=color, alpha=0.08,
                              edgecolor=color, linewidth=1.5,
                              linestyle='--')
        ax.add_patch(rect)
        ax.text(x, 1.1, mode, fontsize=9, ha='center', va='center',
                color=color)

    ax.text(8, 2, '4 Mode Output', fontsize=11, fontweight='bold',
            ha='center', va='center', color=COLORS['gray'])

    # Arrow from workflow to output modes
    ax.annotate('', xy=(8, 1.7), xytext=(8, 2.5),
                arrowprops=dict(arrowstyle='->', color='#9ca3af', lw=1.5))

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig3_workflow.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'fig3_workflow.pdf', bbox_inches='tight')
    plt.close()
    print('Created fig3_workflow.png/pdf')


def fig4_progressive_disclosure():
    """Figure 4: Progressive Disclosure Context Cost (Bar Chart)"""
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))

    levels = ['Discovery\n(Frontmatter)', 'Activation\n(SKILL.md Body)', 'Execution\n(All References + Assets)']
    tokens = [382, 2266, 7941]
    colors = ['#3b82f6', '#8b5cf6', '#10b981']

    bars = ax.barh(levels, tokens, color=colors, alpha=0.7, height=0.5, edgecolor=colors, linewidth=1.5)

    # Add value labels
    for bar, token in zip(bars, tokens):
        ax.text(bar.get_width() + 100, bar.get_y() + bar.get_height()/2,
                f'{token:,} tokens', va='center', fontsize=11, fontweight='bold')

    ax.set_xlabel('Token Count', fontsize=12, fontweight='bold')
    ax.set_title('Progressive Disclosure Context Cost', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlim(0, 10000)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3)

    # Add vertical line for full bundle
    ax.axvline(x=10589, color=COLORS['warning'], linestyle='--', linewidth=1.5, alpha=0.7)
    ax.text(10589 + 100, 2.3, 'Full Bundle\n10,589 tokens', fontsize=9,
            color=COLORS['warning'], fontweight='bold', va='center')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig4_progressive_disclosure.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'fig4_progressive_disclosure.pdf', bbox_inches='tight')
    plt.close()
    print('Created fig4_progressive_disclosure.png/pdf')


def fig5_radar_chart():
    """Figure 5: Self-Reported Quality Scores (Radar Chart)"""
    categories = ['Kejelasan', 'Koherensi', 'Kedalaman', 'Akurasi', 'Gaya', 'Mekanik', 'Engagement']
    N = len(categories)

    # Scores from experimental_log.md
    scores_1 = [8, 8, 7, 8, 8, 9, 7]  # Academic-Popular
    scores_3 = [8, 9, 8, 8, 9, 9, 7]  # Literary

    # Complete the loop
    scores_1 += scores_1[:1]
    scores_3 += scores_3[:1]

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(1, 1, figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_facecolor(COLORS['white'])
    fig.patch.set_facecolor(COLORS['white'])

    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], categories, fontsize=10)

    # Draw ylabels
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=8, color='gray')

    # Plot data
    ax.plot(angles, scores_1, 'o-', linewidth=2, label='Academic-Popular', color='#3b82f6')
    ax.fill(angles, scores_1, alpha=0.15, color='#3b82f6')

    ax.plot(angles, scores_3, 's-', linewidth=2, label='Literary', color='#ec4899')
    ax.fill(angles, scores_3, alpha=0.15, color='#ec4899')

    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)

    # Title
    plt.title('Self-Reported Quality Scores on Worked Examples', fontsize=13,
              fontweight='bold', pad=20)

    # Caveat
    fig.text(0.5, 0.02, '* Caveat: Self-assessment bias — scores reported by the model itself',
             ha='center', fontsize=9, style='italic', color='gray')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig5_quality_scores_radar.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'fig5_quality_scores_radar.pdf', bbox_inches='tight')
    plt.close()
    print('Created fig5_quality_scores_radar.png/pdf')


def fig6_artifact_characteristics():
    """Figure 6: Verified Skill Artifact Characteristics (Bar Chart)"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    metrics = [
        'Core Lines\n(SKILL.md)',
        'Description\nLength (chars)',
        'Reference\nFiles',
        'Asset\nFiles',
        'Project Install\nPaths',
        'Global Install\nPaths',
        'Validator\nWarnings',
    ]
    values = [173, 1014, 6, 3, 9, 8, 0]
    max_vals = [500, 1024, 10, 5, 15, 15, 1]
    colors = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#06b6d4', '#6366f1']

    # Normalize values for display
    display_vals = [v for v in values]

    bars = ax.bar(metrics, display_vals, color=colors, alpha=0.7, edgecolor=colors, linewidth=1.5)

    # Add value labels on bars
    for bar, val, max_val in zip(bars, values, max_vals):
        height = bar.get_height()
        if val == 1014:
            label = f'{val}/{max_val}'
        elif val == 0:
            label = '0 ✓'
        else:
            label = str(val)
        ax.text(bar.get_x() + bar.get_width()/2., height + 10,
                label, ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax.set_title('Verified Skill Artifact Characteristics', fontsize=14, fontweight='bold', pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(0, 1200)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig6_artifact_characteristics.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'fig6_artifact_characteristics.pdf', bbox_inches='tight')
    plt.close()
    print('Created fig6_artifact_characteristics.png/pdf')


if __name__ == '__main__':
    print('Generating figures for ENIP paper...')
    fig1_three_layer_framework()
    fig2_style_engine()
    fig3_workflow()
    fig4_progressive_disclosure()
    fig5_radar_chart()
    fig6_artifact_characteristics()
    print(f'\nAll figures saved to {OUTPUT_DIR}')
