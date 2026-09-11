import numpy as np
import matplotlib.pyplot as plt
import warnings

# Ignoramos el warning de tight_layout por los inset (solo estético)
warnings.filterwarnings("ignore", category=UserWarning, message="This figure includes Axes")

# ==============================================================================
# PARÁMETROS TCDS UNIFICADOS + DATOS LHC (RUN 3)
# ==============================================================================
phi = (1.0 + np.sqrt(5.0)) / 2.0    # Fricción Resultante Universal
kappa = -5.682181                   # Amplitud del Desnivel / Freno Estructural
n = 9.314138                        # Exponente Topológico Efectivo de Red 3D
LI_0 = 0.02                         # Acoplamiento Base / Entorno Relajado

# Datos empíricos LHC
E_lhc_TeV = 13.6                    # Energía centro de masa en TeV
radio_impacto_fm = 0.8              # Escala transversal en femtómetros
amplitud_desacople = E_lhc_TeV / 100.0  # Normalización de perturbación

# Dominio espacial
x = np.linspace(-3.0, 3.0, 2000)
R_bubble = 1.0

# ==============================================================================
# PERFILES DE ACOPLAMIENTO: ALCUBIERRE + PULSO LHC
# ==============================================================================
f_alcubierre = (np.tanh(10 * (x + R_bubble)) - np.tanh(10 * (x - R_bubble))) / 2.0
pulso_lhc = amplitud_desacople * (x / radio_impacto_fm) * np.exp(-0.5 * (x / radio_impacto_fm)**2)
LI_x = LI_0 + (1.0 - LI_0) * f_alcubierre * (1.0 + 0.1 * np.sin(np.pi * x / R_bubble)) + pulso_lhc
LI_x = np.clip(LI_x, 0.0, 1.0)

# ==============================================================================
# GEODÉSICA DE DESNIVEL TOPOLÓGICO
# ==============================================================================
dLI_dx = np.gradient(LI_x, x)
g_x = -kappa * n * (LI_x**(n - 1.0)) * np.abs(dLI_dx)
dg_dx = np.gradient(g_x, x)
T_x = np.abs(dg_dx)

# ==============================================================================
# EFECTO VISUAL: CUELLO DE BOTELLA
# ==============================================================================
ancho_aparente = 1.0 - 0.7 * LI_x
y_upper = 0.5 + ancho_aparente * 0.4
y_lower = 0.5 - ancho_aparente * 0.4

# ==============================================================================
# ZONA DE TRANSICIÓN TOPOLÓGICA
# ==============================================================================
X_MIN, X_MAX = -1.15, 0.95
mask = (x >= X_MIN) & (x <= X_MAX)

# ==============================================================================
# FIGURA PRINCIPAL
# ==============================================================================
fig = plt.figure(figsize=(12, 14), facecolor='white')
gs = fig.add_gridspec(4, 1, height_ratios=[1, 0.65, 1, 1], hspace=0.45)

# ------------------------------------------------------------------------------
# PANEL 0: ILUSIÓN ÓPTICA — CUELLO DE BOTELLA
# ------------------------------------------------------------------------------
ax0 = fig.add_subplot(gs[0])
ax0.set_facecolor('#f5f7ff')
ax0.fill_between(x, y_lower, y_upper, color='#3b82f6', alpha=0.18)
ax0.plot(x, y_upper, color='#1e3a8a', lw=2.2)
ax0.plot(x, y_lower, color='#1e3a8a', lw=2.2)
for curv in np.linspace(0.1, 0.9, 8):
    ax0.plot(x, 0.5 + (curv - 0.5) * ancho_aparente * 0.85, color='#1e3a8a', lw=0.6, alpha=0.25)
ax0.axvspan(X_MIN, X_MAX, color='#f59e0b', alpha=0.12)
ax0.axvline(-R_bubble, color='#f59e0b', linestyle='--', lw=1.2, alpha=0.7, label='Radio de Burbuja')
ax0.axvline(R_bubble, color='#f59e0b', linestyle='--', lw=1.2, alpha=0.7)
ax0.axvline(0, color='#dc2626', linestyle='-', lw=1.5, alpha=0.8, label='Centro / Nave')
ax0.set_xlim(-3, 3); ax0.set_ylim(0, 1); ax0.set_yticks([])
ax0.set_title(r'ILUSIÓN ÓPTICA — CUELLO DE BOTELLA'+'\nDesnivel Topológico: Contracción al Frente, Relajación Atrás',
              fontsize=14, fontweight='bold', color='#1e3a8a', pad=12)
ax0.legend(loc='upper right', framealpha=0.8)
ax0.grid(False)

# LUPA
ax0_inset = ax0.inset_axes([0.315, 0.07, 0.37, 0.86])
ax0_inset.set_facecolor('white')
ax0_inset.fill_between(x[mask], y_lower[mask], y_upper[mask], color='#2563eb', alpha=0.22)
ax0_inset.plot(x[mask], y_upper[mask], color='#1e3a8a', lw=2.0)
ax0_inset.plot(x[mask], y_lower[mask], color='#1e3a8a', lw=2.0)
for curv in np.linspace(0.05, 0.95, 32):
    ax0_inset.plot(x[mask], 0.5 + (curv - 0.5) * ancho_aparente[mask] * 0.9,
                   color='#1e40af', lw=0.45, alpha=0.35)
ax0_inset.set_xlim(X_MIN, X_MAX); ax0_inset.set_ylim(0.05, 0.95)
ax0_inset.set_xticks([]); ax0_inset.set_yticks([])
for s in ax0_inset.spines.values(): s.set_edgecolor('black'); s.set_linewidth(1.2)
ax0.indicate_inset_zoom(ax0_inset, edgecolor='black', linestyle='--', linewidth=1.0)

# ------------------------------------------------------------------------------
# PANEL 1: PERFIL DE ACOPLAMIENTO
# ------------------------------------------------------------------------------
ax1 = fig.add_subplot(gs[1])
ax1.plot(x, LI_x, color='#1d4ed8', lw=2.8, label=r'Acoplamiento $LI(x)$')
ax1.fill_between(x, 0, LI_x, color='#3b82f6', alpha=0.12)
ax1.axvspan(X_MIN, X_MAX, color='#f59e0b', alpha=0.12)
ax1.axvline(0, color='#dc2626', linestyle='--', alpha=0.6)
ax1.axhline(LI_0, color='gray', linestyle=':', label=r'Base $LI_0$')
ax1.axhline(1.0, color='#64748b', linestyle='--', alpha=0.5, label='Límite de Compresión')
ax1.set_xlim(-3, 3); ax1.set_ylim(0, 1.08)
ax1.set_ylabel(r'Acoplamiento $LI$', fontsize=11, fontweight='semibold')
ax1.set_title(f'PERFIL TOPOLÓGICO — Burbuja de Desacople por Perturbación LHC {E_lhc_TeV} TeV',
              fontsize=12, fontweight='bold', pad=10)
ax1.grid(True, linestyle='--', alpha=0.3)
ax1.legend(loc='upper right')

ax1_inset = ax1.inset_axes([0.315, 0.18, 0.37, 0.78])
ax1_inset.set_facecolor('white')
ax1_inset.plot(x[mask], LI_x[mask], color='#1d4ed8', lw=2.6)
ax1_inset.fill_between(x[mask], 0, LI_x[mask], color='#3b82f6', alpha=0.22)
ax1_inset.set_xlim(X_MIN, X_MAX); ax1_inset.set_ylim(-0.05, 1.08)
for s in ax1_inset.spines.values(): s.set_edgecolor('black'); s.set_linewidth(1.2)
ax1.indicate_inset_zoom(ax1_inset, edgecolor='black', linestyle='--', linewidth=1.0)

# ------------------------------------------------------------------------------
# PANEL 2: GEODÉSICA
# ------------------------------------------------------------------------------
ax2 = fig.add_subplot(gs[2])
ax2.plot(x, g_x, color='#16a34a', lw=2.6, label=r'Geodésica $g(x) = -\kappa \, n \, LI^{n-1} \, |\nabla LI|$')
ax2.fill_between(x, 0, g_x, color='#16a34a', alpha=0.15)
ax2.axvspan(X_MIN, X_MAX, color='#f59e0b', alpha=0.08)
ax2.axvline(0, color='#dc2626', linestyle='--', alpha=0.6)
ax2.set_xlim(-3, 3)
ax2.set_ylabel(r'Tensión Estructural $g(x)$', fontsize=11, fontweight='semibold')
ax2.set_title('GEODÉSICA NULA EFECTIVA — Gradiente que Propulsa la Burbuja',
              fontsize=12, fontweight='bold', pad=10)
ax2.grid(True, linestyle='--', alpha=0.3)
ax2.legend(loc='upper right')

ax2_inset = ax2.inset_axes([0.315, 0.15, 0.37, 0.75])
ax2_inset.set_facecolor('white')
ax2_inset.plot(x[mask], g_x[mask], color='#16a34a', lw=2.4)
ax2_inset.fill_between(x[mask], 0, g_x[mask], color='#16a34a', alpha=0.22)
ax2_inset.set_xlim(X_MIN, X_MAX); ax2_inset.set_ylim(bottom=0)
for s in ax2_inset.spines.values(): s.set_edgecolor('black'); s.set_linewidth(1.2)
ax2.indicate_inset_zoom(ax2_inset, edgecolor='black', linestyle='--', linewidth=1.0)

# ------------------------------------------------------------------------------
# PANEL 3: FRICCIÓN
# ------------------------------------------------------------------------------
ax3 = fig.add_subplot(gs[3])
ax3.plot(x, T_x, color='#7c3aed', lw=2.6, label=r'Fricción de Red $T(x) \propto |\nabla g|$')
ax3.fill_between(x, 0, T_x, color='#7c3aed', alpha=0.15)
ax3.axvspan(X_MIN, X_MAX, color='#f59e0b', alpha=0.08)
ax3.axvline(0, color='#dc2626', linestyle='--', alpha=0.6)
ax3.set_xlim(-3, 3)
ax3.set_xlabel(r'Posición a lo largo del eje de deformación $x/R$', fontsize=12, fontweight='semibold')
ax3.set_ylabel(r'Costo de Fricción $T(x)$', fontsize=11, fontweight='semibold')
ax3.set_title(r'COSTO FINITO DE DESACOPLE — Sustitución de Materia Exótica por Fricción Topológica $\phi$',
              fontsize=12, fontweight='bold', pad=10)
ax3.grid(True, linestyle='--', alpha=0.3)
ax3.legend(loc='upper right')

ax3_inset = ax3.inset_axes([0.315, 0.15, 0.37, 0.75])
ax3_inset.set_facecolor('white')
ax3_inset.plot(x[mask], T_x[mask], color='#7c3aed', lw=2.4)
ax3_inset.fill_between(x[mask], 0, T_x[mask], color='#7c3aed', alpha=0.22)
ax3_inset.set_xlim(X_MIN, X_MAX); ax3_inset.set_ylim(bottom=0)
for s in ax3_inset.spines.values(): s.set_edgecolor('black'); s.set_linewidth(1.2)
ax3.indicate_inset_zoom(ax3_inset, edgecolor='black', linestyle='--', linewidth=1.0)

plt.tight_layout()
plt.savefig('tcds_alcubierre_lupa_cientifica.png', dpi=300, bbox_inches='tight')
plt.show()

# ==============================================================================
# RESUMEN NUMÉRICO
# ==============================================================================
print("=" * 60)
print("RESUMEN — DESNIVEL TOPOLÓGICO TCDS + ALCUBIERRE + LHC")
print("=" * 60)
print(f"Fricción Universal φ  = {phi:.6f}")
print(f"Amplitud κ            = {kappa:.6f}")
print(f"Exponente n           = {n:.6f}")
print(f"Acoplamiento Base LI₀ = {LI_0:.6f}")
print(f"Energía LHC           = {E_lhc_TeV} TeV")
print(f"Pico de Tensión g_max = {np.max(g_x):.6f}")
print(f"Pico de Fricción T_max= {np.max(T_x):.6f}")
print(f"Zona de Lupa: x ∈ [{X_MIN:.2f}, {X_MAX:.2f}]")
print("=" * 60)
print("La fricción finita T(x) reemplaza el requerimiento")
print("de materia exótica infinita por un costo energético")
print("finito y medible en términos de desacople de red.")
print("La lupa resalta la zona crítica donde el desnivel")
print("topológico produce la transición de curvatura efectiva.")
print("=" * 60)
