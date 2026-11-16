%% verificacion_independiente.m
% Material suplementario S3 - Verificacion independiente de los cinco problemas.
% Imprime version de MATLAB/toolboxes, resultados y errores numericos.
% Requiere: Control System Toolbox; Symbolic Math Toolbox (solo problema a).
clear; clc; format long g
fprintf('%s\n', version); ver('control'); ver('symbolic');
tol_num = 1e-8;      % tolerancia aceptada para comparar analitico vs. numerico

%% a) EDO: (D^2-2D-3)y = x sin2x + x^3 e^{3x}
syms x A B C D E F G H
yp = (A*x+B)*cos(2*x) + (C*x+D)*sin(2*x) + x*exp(3*x)*(E*x^3+F*x^2+G*x+H);
res = simplify(diff(yp,2) - 2*diff(yp) - 3*yp - (x*sin(2*x) + x^3*exp(3*x)));
eqs = [coeffs(simplify(subs(res,{sin(2*x),exp(3*x)},{0,0})/cos(2*x)),x), ...
       coeffs(simplify(subs(res,{cos(2*x),exp(3*x)},{0,0})/sin(2*x)),x), ...
       coeffs(simplify(subs(res,{cos(2*x),sin(2*x)},{0,0})/exp(3*x)),x)];
S = solve(eqs,[A B C D E F G H]);
disp('a) Coeficientes:'); disp(struct2array(S))
fprintf('   residuo simbolico = %s\n', char(simplify(subs(res,S))));   % debe ser 0

%% b) Laplace: y''+2y'+10y = u'-u, y(0-)=1, y'(0-)=3, u escalon
t  = (0:1e-3:6)'; u = ones(size(t));
yT = -1/10 + exp(-t).*(11/10*cos(3*t) + 17/10*sin(3*t));      % ec. (7)
% Realizacion del sistema A: x1 = y, x2 = y' - u  -> x(0-) = x(0+) = [1; 3]
sysA = ss([0 1; -10 -2], [1; -3], [1 0], 0);
eA   = max(abs(lsim(sysA,u,t,[1;3]) - yT));
% Codigo ORIGINAL del sistema B: usa la realizacion que construye MATLAB y
% un x0 calculado para otra realizacion supuesta (comentario "C = [-1 1]")
tB   = (0:0.01:6)'; uB = ones(size(tB));
yTB  = -1/10 + exp(-tB).*(11/10*cos(3*tB) + 17/10*sin(3*tB));
yziB = exp(-tB).*(cos(3*tB) + 4/3*sin(3*tB));
sysB = ss(tf([1 -1],[1 2 10]));
disp('   Matrices reales de ss(tf(...)) en esta version:'); disp(sysB.A), disp(sysB.C)
x0_B = [-6/13; 7/13];                                   % valor declarado por B
y_zi = lsim(sysB, zeros(size(tB)), tB, x0_B);
y_zs = lsim(sysB, uB, tB, [0;0]);
y_to = lsim(sysB, uB, tB, x0_B);
fprintf('b) ANTES (codigo B): y(0)=%.4f | err max entrada cero=%.3f, estado cero=%.1e, total=%.3f\n', ...
        y_to(1), max(abs(y_zi-yziB)), max(abs(y_zs-(yTB-yziB))), max(abs(y_to-yTB)));
x0_ok = obsv(sysB) \ [1; 3];        % correccion: valido porque D = 0 y u(0-) = 0
y_ok  = lsim(sysB, uB, tB, x0_ok);
fprintf('   DESPUES (x0 = obsv\\[1;3] = [%.4f %.4f]): err max total = %.1e\n', x0_ok, max(abs(y_ok-yTB)));
fprintf('   Sistema A (x0 = [1;3]): err max total = %.1e\n', eA);
figure; plot(tB,yTB,'k',tB,y_to,'r--',tB,y_ok,'b:','LineWidth',1.5); grid on
legend('Analitica (7)','Codigo B original','Codigo B corregido'); xlabel('t [s]'); ylabel('y(t)')

%% c) Transformada Z
Gp = tf(1125,[1 5 0]); Gz = c2d(Gp,1,'zoh'); disp('c) G(z) ='); Gz
disp(pole(feedback(Gz,1)).')
for K = [0.0035 0.0038751 0.004]          % 0.0035 = Gemini; 0.0038751 = ChatGPT
    Td = feedback(K*Gz,1); s = stepinfo(Td,'SettlingTimeThreshold',0.02);
    fprintf('   K=%.7f |p|=%.4f Mp=%.2f%% Ts=%g s ess=%.1e\n', K, abs(pole(Td(1))), ...
            s.Overshoot, s.SettlingTime, 1-dcgain(Td));
end
for Ka = [0.0154 0.0158974]                % 0.0154 = Gemini; 0.0158974 = ChatGPT
Ta = feedback(Ka*Gp,1); s = stepinfo(Ta,'SettlingTimeThreshold',0.02,'RiseTimeLimits',[0.1 0.9]);
fprintf('   Analogico Ka=%.7f: Mp=%.2f%% Ts=%.3f s Tr(10-90)=%.3f s\n', Ka, s.Overshoot, s.SettlingTime, s.RiseTime);
end

%% d) Espacio de estado + Euler
A = [-3 1; -2 0]; B = [1; -2]; C = [1 0];
fprintf('d) det(ctrb)=%g det(obsv)=%g\n', det(ctrb(A,B)), det(obsv(A,C)));
K = place(A,B,[-2+2j -2-2j]); L = place(A',C',[-3 -4])'; disp(K), disp(L.')
Ab = [A -B*K; L*C A-B*K-L*C]; disp(eig(Ab).')
% Condiciones de las respuestas: A -> xhat(0)=[0;1]; B -> xhat(0)=[0;0], dt=0.001
% Ambas usan u = r - K*xhat (N = 1). Cambie z0 para cada caso.
N = 1; Bb = [B; B]*N;
for z0 = [[1;-1;0;1], [1;-1;0;0]]
exacta = @(tt) expm([Ab Bb; zeros(1,5)]*tt) * [z0; 1];
fprintf('   Estudio de paso, z0 = [%g %g %g %g] (Euler explicito, r = 1, t en [0,10] s):\n', z0);
for h = [0.1 0.05 0.01 0.001]
    n = round(10/h); z = z0; err = 0; tcruce = NaN;
    for k = 1:n
        z = z + h*(Ab*z + Bb); ze = exacta(k*h);
        err = max(err, max(abs(z(1:2)-ze(1:2))));
        if isnan(tcruce) && norm(z(1:2)-z(3:4)) < 1e-10, tcruce = k*h; end
    end
    fprintf('   h=%-6g max|x_Euler - x_exacta| = %.2e   |e|<1e-10 desde t = %g s\n', h, err, tcruce);
end
end
fprintf('   y(inf) con u = r - K*xhat: %.4f (sin precompensacion)\n', dcgain(ss(Ab,[B;B],[C 0 0],0)));

%% e) Respuesta en frecuencia
L1 = tf(1,[1 5 6 0]);
wc = (-5*sqrt(3)+sqrt(99))/2; Kc = 1/abs(freqresp(L1,wc));
[gm,pm] = margin(Kc*L1); fprintf('e) MF=60: Kc=%.4f wc=%.5f (MF=%.2f)\n', Kc, wc, pm);
[gm,pm] = margin(15*L1); fprintf('   K=15: MG=%.4f (%.2f dB)\n', gm, 20*log10(gm));
M = 10^(2/20); f = @(q) ((36+26*q+3*q^2)/10)^2*(1-1/M^2) - q^2*(13+2*q);
q = fzero(f,[0.5 2]); Kr = (36+26*q+3*q^2)/10;
[mag,~,w] = bode(feedback(Kr*L1,1), logspace(-1,1,20001));
fprintf('   Mr=+2dB: K=%.5f wr=%.5f max|T|=%.4f dB\n', Kr, sqrt(q), 20*log10(max(squeeze(mag))));
fprintf('   Ku=30, wu=sqrt(6)=%.5f; comprobacion margin: %.4f\n', sqrt(6), margin(L1));
