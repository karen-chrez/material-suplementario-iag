"""
verificacion.py -- Verificación independiente de los cinco problemas.
Material suplementario S4 del artículo
"The use of Generative Artificial Intelligence in advanced mathematics courses".

Reproduce todos los valores de referencia de las Tablas 2-5 y genera las figuras 1-3.
Requiere: Python >= 3.10, sympy, numpy, scipy, control (python-control), matplotlib.
Uso:  python verificacion.py   (escribe salida_verificacion.txt y figuras en ./figuras)
"""
import os, sys
import numpy as np
import sympy as sp
import scipy, scipy.signal as sg
from scipy.linalg import expm
import control as ct
import matplotlib
matplotlib.rcParams.update({"font.family":"serif","font.serif":["Liberation Serif","TeX Gyre Termes"],"mathtext.fontset":"stix","pdf.fonttype":42,"ps.fonttype":42})  # tipografía tipo Times
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = []
def p(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)

os.makedirs("figuras", exist_ok=True)
p(f"Python {sys.version.split()[0]} | sympy {sp.__version__} | numpy {np.__version__} | "
  f"scipy {scipy.__version__} | control {ct.__version__}")
TOL_SIM = 1e-8

# --------------------------------------------------------------------------- a)
p("\n=== a) EDO: (D^2-2D-3)y = x sin2x + x^3 e^{3x}")
x = sp.symbols("x")
A, B, C, D, E, F, G, H = sp.symbols("A B C D E F G H")
yp = (A*x+B)*sp.cos(2*x) + (C*x+D)*sp.sin(2*x) + x*sp.exp(3*x)*(E*x**3+F*x**2+G*x+H)
res = sp.expand(sp.diff(yp, x, 2) - 2*sp.diff(yp, x) - 3*yp - (x*sp.sin(2*x) + x**3*sp.exp(3*x)))
eqs = []
for v in sp.collect(res, [sp.cos(2*x), sp.sin(2*x), sp.exp(3*x)], evaluate=False).values():
    eqs += sp.Poly(v, x).coeffs()
sol = sp.solve(eqs, [A, B, C, D, E, F, G, H])
p("coeficientes:", sol)
p("residuo simbólico:", sp.simplify(res.subs(sol)))

# --------------------------------------------------------------------------- b)
p("\n=== b) Laplace: y''+2y'+10y = u'-u, y(0-)=1, y'(0-)=3, u escalón")
t = np.arange(0, 6 + 1e-12, 1e-3); u = np.ones_like(t)
yzi = np.exp(-t)*(np.cos(3*t) + 4/3*np.sin(3*t))
yzs = -0.1 + np.exp(-t)*(0.1*np.cos(3*t) + 11/30*np.sin(3*t))
yT = -0.1 + np.exp(-t)*(1.1*np.cos(3*t) + 1.7*np.sin(3*t))
ts_ = sp.symbols("t", positive=True)
yTs = -sp.Rational(1, 10) + sp.exp(-ts_)*(sp.Rational(11, 10)*sp.cos(3*ts_) + sp.Rational(17, 10)*sp.sin(3*ts_))
p("y(0+) =", yTs.subs(ts_, 0), " y'(0+) =", sp.diff(yTs, ts_).subs(ts_, 0))
p("residuo EDO para t>0:", sp.simplify(sp.diff(yTs, ts_, 2) + 2*sp.diff(yTs, ts_) + 10*yTs + 1))

def sim(Am, Bm, Cm, x0, uu=u, tt=t):
    _, y, _ = sg.lsim((np.array(Am, float), np.array(Bm, float), np.array(Cm, float), 0), uu, tt, X0=x0)
    return y
eA = np.abs(sim([[0, 1], [-10, -2]], [[1], [-3]], [[1, 0]], [1, 3]) - yT).max()
eO = np.abs(sim([[-2, 1], [-10, 0]], [[1], [-1]], [[1, 0]], [1, 5]) - yT).max()
p(f"realización x1=y, x2=y'-u, x0=[1;3]:            max|err| = {eA:.1e}  {'OK' if eA < TOL_SIM else 'FALLA'}")
p(f"canónica observable (Gemini IDEAR), x0=[1;5]:   max|err| = {eO:.1e}  {'OK' if eO < TOL_SIM else 'FALLA'}")
# Código original de Gemini 3.6: sys_ss = ss(tf(...)), x0 = [-6/13; 7/13]
A0 = np.array([[-2., -10.], [1., 0.]]); B0 = np.array([[1.], [0.]]); C0 = np.array([[1., -1.]])
realiz = {"tf2ss (canónica controlable)": np.eye(2), "escalada diag(1,4)": np.diag([1., 4.])}
fig_data = None
for nombre, S in realiz.items():
    Ar, Br, Cr = S @ A0 @ np.linalg.inv(S), S @ B0, C0 @ np.linalg.inv(S)
    xB = [-6/13, 7/13]
    y_zi = sim(Ar, Br, Cr, xB, 0*u); y_zs = sim(Ar, Br, Cr, [0, 0]); y_to = sim(Ar, Br, Cr, xB)
    x_ok = np.linalg.solve(np.vstack([Cr, Cr @ Ar]), [1, 3]); y_ok = sim(Ar, Br, Cr, x_ok)
    p(f"Gemini 3.6, realización {nombre}: ANTES y(0)={y_to[0]:.4f}, err entrada cero={np.abs(y_zi-yzi).max():.3f}, "
      f"estado cero={np.abs(y_zs-yzs).max():.1e}, total={np.abs(y_to-yT).max():.3f} | DESPUÉS x0={np.round(x_ok,4)}, "
      f"err total={np.abs(y_ok-yT).max():.1e}")
    if fig_data is None: fig_data = (y_to, y_ok)
plt.figure(figsize=(3.3, 2.2))
plt.plot(t, yT, "k", lw=1.6, label="Analítica, Ec. (4)")
plt.plot(t, fig_data[0], "r--", lw=1.2, label="Código original")
plt.plot(t, fig_data[1], "b:", lw=1.6, label="Código corregido")
plt.xlabel("t [s]", fontsize=8); plt.ylabel("y(t)", fontsize=8); plt.grid(alpha=.3)
plt.legend(fontsize=7, frameon=False); plt.tick_params(labelsize=7); plt.tight_layout()
plt.savefig("figuras/fig_laplace.pdf"); plt.savefig("figuras/fig_laplace.png", dpi=200); plt.close()

# --------------------------------------------------------------------------- c)
p("\n=== c) Transformada Z: Gp(s)=1125/[s(s+5)], ZOH, T=1 s")
Gp = ct.tf([1125], [1, 5, 0]); Gz = ct.c2d(Gp, 1.0, "zoh")
p("G(z) =", Gz)
p("polos LC sin controlador:", np.round(ct.poles(ct.feedback(Gz, 1)), 4))
def Cd(nm, dn): return ct.tf(nm, dn, 1.0)
def eval_disc(nombre, Cz):
    T = ct.feedback(Cz*Gz, 1); k = np.arange(0, 40.)
    _, y = ct.step_response(T, T=k); y = np.squeeze(y); yss = float(np.real(ct.dcgain(T)))
    idx = np.where(np.abs(y-yss) > 0.02*abs(yss))[0]; tsd = k[idx[-1]+1] if len(idx) else 0
    _, uk = ct.step_response(ct.feedback(Cz, Gz), T=k); uk = np.squeeze(uk)
    tc = np.arange(0, 30, 1e-3); uc = uk[np.minimum((tc//1).astype(int), len(uk)-1)]
    _, yc = ct.forced_response(Gp, T=tc, U=uc); idc = np.where(np.abs(yc-1) > 0.02)[0]
    pol = ct.poles(T)
    p(f"{nombre:34s} polos={np.round(pol,4)} |z|max={max(abs(pol)):.4f} Mp(muestras)={(y.max()-yss)*100:.2f}% "
      f"ts(muestras)={tsd:.0f} s | Mp(continua)={(yc.max()-1)*100:.2f}% ts(continua)={tc[idc[-1]+1]:.2f} s")
    return k, y, tc, yc
disenos = {"GPT ZS  C(z)=0.0038751": Cd([0.0038751], [1]),
           "GPT IDEAR C(z)=0.004": Cd([0.004], [1]),
           "Gem. H IDEAR C(z)=0.0038": Cd([0.0038], [1]),
           "Gem. 3.6 C(z)=0.0035": Cd([0.0035], [1]),
           "Gem. H ZS adelanto": Cd([0.0045, -0.0045*0.006738], [1, 0.20])}
curvas = {k_: eval_disc(k_, v) for k_, v in disenos.items()}
s = ct.tf("s")
for nombre, Cs in {"GPT ZS  Ka=0.0158974": 0.0158974, "GPT IDEAR Ka=0.0155": 0.0155,
                   "Gem. H IDEAR Ka=0.015432": 0.015432, "Gem. 3.6 Ka=0.0154": 0.0154,
                   "Gem. H ZS adelanto": 0.2104*(s+5)/(s+20)}.items():
    T = ct.feedback(Cs*Gp, 1); tt = np.linspace(0, 8, 800001); _, y = ct.step_response(T, T=tt); y = np.squeeze(y)
    idx = np.where(np.abs(y-1) > 0.02)[0]
    p(f"{nombre:34s} Mp={(y.max()-1)*100:.2f}% ts={tt[idx[-1]+1]:.3f} s "
      f"tr(10-90)={tt[np.argmax(y>=0.9)]-tt[np.argmax(y>=0.1)]:.3f} s")
plt.figure(figsize=(3.3, 2.2))
k, y, tc, yc = curvas["GPT ZS  C(z)=0.0038751"]
plt.plot(tc, yc, "r", lw=1.1, label="Salida continua, K=0.0038751")
plt.plot(k, y, "ro", ms=3.5, label="Muestras")
k2, y2, tc2, yc2 = curvas["Gem. H ZS adelanto"]
plt.plot(tc2, yc2, "b--", lw=1.1, label="Salida continua, adelanto")
plt.axhline(1.10, color="gray", ls=":", lw=1); plt.text(5.5, 1.125, "límite $M_p$ = 10 %", fontsize=7, color="gray"); plt.ylim(0, 1.25)
plt.xlim(0, 10); plt.xlabel("t [s]", fontsize=8); plt.ylabel("y(t)", fontsize=8); plt.grid(alpha=.3)
plt.legend(fontsize=6.5, frameon=False, loc="lower right"); plt.tick_params(labelsize=7); plt.tight_layout()
plt.savefig("figuras/fig_z.pdf"); plt.savefig("figuras/fig_z.png", dpi=200); plt.close()

# --------------------------------------------------------------------------- d)
p("\n=== d) Espacio de estado")
A = np.array([[-3., 1.], [-2., 0.]]); B = np.array([[1.], [-2.]]); C = np.array([[1., 0.]])
p("det[B AB] =", round(np.linalg.det(ct.ctrb(A, B)), 6), " det[C;CA] =", round(np.linalg.det(ct.obsv(A, C)), 6))
K = ct.place(A, B, [-2+2j, -2-2j]); L = ct.place(A.T, C.T, [-3, -4]).T
p("K =", np.round(K, 6), " L =", np.round(L.T, 6))
Ab = np.block([[A, -B@K], [L@C, A-B@K-L@C]]); Bb = np.vstack([B, B])
p("eigenvalores del sistema aumentado:", np.round(np.linalg.eigvals(Ab), 6))
Tcl = ct.ss(Ab, Bb, np.hstack([C, np.zeros((1, 2))]), 0)
p("Y(s)/R(s) =", ct.minreal(ct.ss2tf(Tcl), verbose=False), " y(inf) =", round(float(np.real(ct.dcgain(Tcl))), 6))
M = np.zeros((5, 5)); M[:4, :4] = Ab; M[:4, 4] = Bb[:, 0]
plt.figure(figsize=(3.3, 2.2))
for z0, etiqueta in [(np.array([1, -1, 0, 1.]), "x̂(0)=[0;1] (GPT ZS)"), (np.array([1, -1, 0, 0.]), "x̂(0)=[0;0] (GPT IDEAR)")]:
    tc_ex = None; tt = np.arange(0, 12, 1e-3)
    for ti in tt:
        zz = expm(M*ti) @ np.append(z0, 1.)
        if np.linalg.norm(zz[:2]-zz[2:4]) < 1e-10: tc_ex = ti; break
    p(f"Euler, x(0)=[1;-1], {etiqueta}: exacta ||e||<1e-10 desde t={tc_ex:.2f} s")
    hs, errs = [], []
    for h in [0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001]:
        n = int(round(10/h)); z = z0.copy(); ze = np.append(z0, 1.); P = expm(M*h); err = 0; tcr = None
        for kk in range(n):
            z = z + h*(Ab@z + Bb[:, 0]); ze = P@ze; err = max(err, np.abs(z[:2]-ze[:2]).max())
            if tcr is None and np.linalg.norm(z[:2]-z[2:]) < 1e-10: tcr = (kk+1)*h
        hs.append(h); errs.append(err)
        if h in (0.1, 0.01, 0.001):
            p(f"   h={h:<6} max|x_Euler - x_exacta| en [0,10] s = {err:.2e}   ||e||<1e-10 desde t={tcr}")
    plt.loglog(hs, errs, "o-", ms=3, lw=1, label=etiqueta)
plt.xlabel("h [s]", fontsize=8); plt.ylabel("máx. error de trayectoria", fontsize=8); plt.grid(alpha=.3, which="both")
plt.legend(fontsize=6.5, frameon=False); plt.tick_params(labelsize=7); plt.tight_layout()
plt.savefig("figuras/fig_euler.pdf"); plt.savefig("figuras/fig_euler.png", dpi=200); plt.close()

# --------------------------------------------------------------------------- e)
p("\n=== e) Respuesta en frecuencia: L(s)=K/[s(s+2)(s+3)]")
L1 = ct.tf([1], [1, 5, 6, 0])
wc = (-5*np.sqrt(3) + np.sqrt(99))/2; Kc = 1/abs(ct.evalfr(L1, 1j*wc))
p(f"MF=60°: wc={wc:.5f} rad/s, Kc={Kc:.5f}, MF verificado={ct.margin(Kc*L1)[1]:.4f}°")
gm = ct.margin(15*L1)[0]; p(f"MG=2: K=15, MG verificado={gm:.5f} ({20*np.log10(gm):.3f} dB), w180=sqrt(6)={np.sqrt(6):.5f}")
from scipy.optimize import brentq
Mr = 10**(2/20); f = lambda q: ((36+26*q+3*q**2)/10)**2*(1-1/Mr**2) - q**2*(13+2*q)
q = brentq(f, 0.5, 2); Kr = (36+26*q+3*q**2)/10
w = np.logspace(-1, 1, 200001); Tm = np.abs(Kr*ct.evalfr(L1, 1j*w)/(1+Kr*ct.evalfr(L1, 1j*w)))
p(f"Mr=+2 dB: K={Kr:.5f}, wr={np.sqrt(q):.5f} rad/s, max|T| verificado={20*np.log10(Tm.max()):.4f} dB")
p(f"Ku={ct.margin(L1)[0]:.4f}, wu={np.sqrt(6):.5f} rad/s")

with open("salida_verificacion.txt", "w", encoding="utf-8") as fh:
    fh.write("\n".join(OUT) + "\n")
