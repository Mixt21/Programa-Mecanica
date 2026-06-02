import math
import matplotlib.pyplot as plt

K = 8.99e9  

cargas = []                
dimension = ""             
puntos_campo_guardados = [] 
fuerza_neta_guardada = None 

def configurar_sistema():
    global cargas, dimension, puntos_campo_guardados, fuerza_neta_guardada
    
    print("\n" + "="*50)
    print("         CONFIGURACIÓN DEL SISTEMA               ")
    print("="*50)
    
    dimension = input("¿Dimensión de simulación? (1D / 2D): ").strip().upper()
    while dimension not in ["1D", "2D"]:
        dimension = input("⚠️ Opción inválida. Elige 1D o 2D: ").strip().upper()

    try:
        num_cargas = int(input("¿Cuántas cargas vas a registrar en total?: "))
        if dimension == "1D" and num_cargas < 2:
            print("⚠️ [ERROR]: Para 1D necesitas mínimo 2 cargas.")
            return False
        if dimension == "2D" and num_cargas < 3:
            print("⚠️ [ERROR]: Para 2D necesitas mínimo 3 cargas.")
            return False
    except:
        print("⚠️ [ERROR]: Debes ingresar un número entero válido.")
        return False

    cargas = []
    puntos_campo_guardados = [] 
    fuerza_neta_guardada = None
    
    for i in range(num_cargas):
        while True:
            print(f"\n--- DATOS DE LA CARGA NUMERO {i+1} ---")
            try:
                valor_q = float(input(f"  -> Valor q{i+1} en Coulombs (ej. 1e-6): "))
                pos_x = float(input(f"  -> Posición X (metros): "))
                pos_y = float(input(f"  -> Posición Y (metros): ")) if dimension == "2D" else 0.0
                
                posicion_repetida = False
                for c in cargas:
                    if c['x'] == pos_x and c['y'] == pos_y:
                        print(f"⚠️ [ERROR]: Coordenada ({pos_x}, {pos_y}) ya ocupada por Carga {c['numero']}. Intenta otra.")
                        posicion_repetida = True
                        break
                
                if posicion_repetida:
                    continue 
                
                cargas.append({"numero": i+1, "q": valor_q, "x": pos_x, "y": pos_y})
                break 
                
            except:
                print("⚠️ [ERROR]: Entrada inválida. Usa números.")
                continue
            
    return True

def menu():
    global cargas, dimension, puntos_campo_guardados, fuerza_neta_guardada
    
    print("=================================================")
    print("       BIENVENIDO AL SIMULADOR ELECTROSTÁTICO    ")
    print("=================================================")
    
    while not configurar_sistema():
        print("Reiniciando el registro por datos incorrectos...")

    while True:
        print("\n" + "—"*50)
        print(f" MENU PRINCIPAL  |  Modo activo: {dimension}")
        print("—"*50)
        print("1. Ver datos de las cargas registradas")
        print("2. Calcular FUERZA NETA sobre una carga")
        print("3. Calcular CAMPO ELÉCTRICO en 3 puntos")
        print("4. Mostrar GRÁFICA / IMAGEN del sistema")
        print("5. REINICIAR (Cambiar de modo o registrar nuevas cargas)")
        print("6. Salir del programa")
        print("="*50)
        
        opcion = input("Selecciona una opción (1-6): ").strip()
        
        if opcion == "1":
            print("\n=== CARGAS EN EL SISTEMA ===")
            for c in cargas:
                print(f"• Carga {c['numero']}: q = {c['q']:.3e} C  |  Posición = ({c['x']}, {c['y']}) m")
                
        elif opcion == "2":
            ejecutar_calculo_fuerza()
            
        elif opcion == "3":
            ejecutar_calculo_campo()
            
        elif opcion == "4":
            print("\n[Abriendo visualización...] Cierra la ventana gráfica para regresar al menú.")
            generar_grafica_imagen()
            
        elif opcion == "5":
            while not configurar_sistema():
                pass
            
        elif opcion == "6":
            print("\n¡Simulación finalizada con éxito!")
            break
        else:
            print("⚠️ Opción no válida. Elige de el 1 al 6.")

def ejecutar_calculo_fuerza():
    global fuerza_neta_guardada
    print("\n=== CÁLCULO DE FUERZA ELÉCTRICA NETA ===")
    try:
        seleccion = int(input("¿Qué número de carga deseas analizar?: "))
        idx_sel = seleccion - 1
        if idx_sel < 0 or idx_sel >= len(cargas):
            print("⚠️ [ERROR]: Ese número de carga no existe.")
            return
    except:
        print("⚠️ [ERROR]: Entrada inválida.")
        return

    carga_analizada = cargas[idx_sel]
    fx_neta, fy_neta = 0.0, 0.0
    componentes_individuales = []
    
    print(f"\n>> Interacciones sobre la Carga {carga_analizada['numero']}:")
    
    for i in range(len(cargas)):
        if i == idx_sel:
            print(f"  -> Carga {cargas[i]['numero']}: Auto-fuerza excluida (0 N).")
            continue
            
        otra_carga = cargas[i]
        dx = carga_analizada['x'] - otra_carga['x']
        dy = carga_analizada['y'] - otra_carga['y']
        distancia = math.sqrt(dx**2 + dy**2)
        
        if distancia == 0:
            print(f"⚠️ [ERROR FÍSICO]: Distancia cero con Carga {otra_carga['numero']}.")
            return
            
        ux, uy = dx / distancia, dy / distancia
        magnitud_f = K * abs(carga_analizada['q'] * otra_carga['q']) / (distancia**2)
        
        if (carga_analizada['q'] > 0 and otra_carga['q'] > 0) or (carga_analizada['q'] < 0 and otra_carga['q'] < 0):
            fx_ind, fy_ind = magnitud_f * ux, magnitud_f * uy
        else:
            fx_ind, fy_ind = -magnitud_f * ux, -magnitud_f * uy
            
        fx_neta += fx_ind
        fy_neta += fy_ind
        
        componentes_individuales.append({
            "desde_x": otra_carga['x'], "desde_y": otra_carga['y'],
            "fx": fx_ind, "fy": fy_ind
        })
        
        print(f"  -> Desde Carga {otra_carga['numero']}: Distancia = {distancia:.2f} m | Fx = {fx_ind:.3e} N, Fy = {fy_ind:.3e} N")

    magnitud_neta = math.sqrt(fx_neta**2 + fy_neta**2)
    
    fuerza_neta_guardada = {
        "carga_num": carga_analizada['numero'],
        "x_origen": carga_analizada['x'], "y_origen": carga_analizada['y'],
        "fx": fx_neta, "fy": fy_neta, "magnitud": magnitud_neta,
        "individuales": componentes_individuales
    }
    
    print(f"\n>> RESULTADO FUERZA NETA:")
    print(f"   Fx = {fx_neta:.3e} N | Fy = {fy_neta:.3e} N")
    if dimension == "2D":
        print(f"   Dirección (Ángulo) = {math.degrees(math.atan2(fy_neta, fx_neta)):.2f}°")
    else:
        print(f"   Dirección = {'Derecha (+)' if fx_neta > 0 else 'Izquierda (-)' if fx_neta < 0 else 'Nula'}")
    print(f"   Magnitud Total = {magnitud_neta:.3e} N")

def ejecutar_calculo_campo():
    global puntos_campo_guardados
    print("\n=== CÁLCULO DE CAMPO ELÉCTRICO (3 PUNTOS) ===")
    
    puntos_campo_guardados = [] 
    
    for p in range(1, 4):
        while True: 
            print(f"\n--- COORDENADAS DEL PUNTO DE PRUEBA {p} ---")
            try:
                px = float(input(f"  Coordenada X para Punto {p}: "))
                py = float(input(f"  Coordenada Y para Punto {p}: ")) if dimension == "2D" else 0.0
                    
                ex_total, ey_total = 0.0, 0.0
                sobre_carga = False
                
                for c in cargas:
                    dx = px - c['x']
                    dy = py - c['y']
                    distancia = math.sqrt(dx**2 + dy**2)
                    
                    if distancia == 0:
                        print(f"⚠️ [ERROR]: El Punto {p} coincide con la posición de la Carga {c['numero']}. Elige otra coordenada.")
                        sobre_carga = True
                        break
                        
                    ux, uy = dx / distancia, dy / distancia
                    magnitud_e = K * c['q'] / (distancia**2)
                    
                    ex_total += magnitud_e * ux
                    ey_total += magnitud_e * uy
                    
                if sobre_carga:
                    continue 
                    
                magnitud_e_total = math.sqrt(ex_total**2 + ey_total**2)
                
                puntos_campo_guardados.append({
                    "numero": p, "x": px, "y": py, 
                    "ex": ex_total, "ey": ey_total, "magnitud": magnitud_e_total
                })
                
                print(f"  -> Resultados Punto {p} ({px}, {py}):")
                print(f"     Ex = {ex_total:.3e} N/C | Ey = {ey_total:.3e} N/C | Magnitud E = {magnitud_e_total:.3e} N/C")
                break 
            except:
                print("⚠️ [ERROR]: Entrada numérica no válida.")
                continue

def generar_grafica_imagen():
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    plt.figure(figsize=(10, 8))
    
    plt.axhline(0, color='#7f8c8d', linestyle='-', linewidth=0.8)
    if dimension == "2D":
        plt.axvline(0, color='#7f8c8d', linestyle='-', linewidth=0.8)

    texto_datos = "📊 RESUMEN DEL SISTEMA\n" + "—"*25 + "\n"
    for c in cargas:
        texto_datos += f"q{c['numero']}: {c['q']:.1e} C en ({c['x']:.1f}, {c['y']:.1f})m\n"
    
    texto_datos += "\n📝 CÁLCULOS ACTIVOS:\n"
    
    for c in cargas:
        color_c = '#e74c3c' if c['q'] > 0 else '#2980b9'
        signo = "+" if c['q'] > 0 else "-"
        plt.scatter(c['x'], c['y'], color=color_c, s=400, edgecolors='#2c3e50', linewidths=2, zorder=5)
        plt.text(c['x'], c['y'] + 0.15, f"q{c['numero']} ({signo})", ha='center', weight='bold', color='#2c3e50')

    if fuerza_neta_guardada is not None:
        fn = fuerza_neta_guardada
        

        for ind in fn['individuales']:
            plt.quiver(ind['desde_x'], ind['desde_y'], ind['fx'], ind['fy'], color='#95a5a6',
                       angles='xy', scale_units='xy', scale=None, width=0.003, linestyle='--', alpha=0.7, zorder=4)
        
        plt.quiver(fn['x_origen'], fn['y_origen'], fn['fx'], fn['fy'], color='#27ae60',
                   angles='xy', scale_units='xy', scale=None, width=0.007, zorder=6)
        texto_datos += f"• F. Neta en q{fn['carga_num']}: {fn['magnitud']:.2e} N\n"

    if len(puntos_campo_guardados) > 0:
        for p in puntos_campo_guardados:
            plt.scatter(p['x'], p['y'], color='#8e44ad', marker='x', s=120, linewidths=2.5, zorder=6)
            plt.quiver(p['x'], p['y'], p['ex'], p['ey'], color='#8e44ad',
                       angles='xy', scale_units='xy', scale=None, width=0.005, zorder=6)
            plt.text(p['x'], p['y'] - 0.25, f"P{p['numero']}", color='#8e44ad', ha='center', fontsize=9, weight='bold')
            texto_datos += f"• Campo en P{p['numero']}: {p['magnitud']:.2e} N/C\n"

    if "•" not in texto_datos:
        texto_datos += "(Ningún cálculo ejecutado)"

    props_caja = dict(boxstyle='round,pad=0.6', facecolor='#ffffff', edgecolor='#bdc3c7', alpha=0.9)
    plt.gca().text(0.02, 0.98, texto_datos, transform=plt.gca().transAxes, fontsize=9,
                   verticalalignment='top', bbox=props_caja, fontfamily='monospace')

    plt.title(f"Plano Vectorial Electrostático — Modo {dimension}", fontsize=13, weight='bold', color='#2c3e50', pad=15)
    plt.xlabel("Eje Horizontal X (Metros)", fontsize=10, color='#34495e')
    plt.ylabel("Eje Vertical Y (Metros)", fontsize=10, color='#34495e')
    plt.grid(True, linestyle=':', alpha=0.5, color='#bdc3c7')
    plt.axis('equal')
    
    from matplotlib.lines import Line2D
    leyendas_elementos = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#e74c3c', markersize=11, label='Carga Positiva (+)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#2980b9', markersize=11, label='Carga Negativa (-)'),
        Line2D([0], [0], color='#27ae60', lw=3, label='Vector Fuerza Neta ──►'),
        Line2D([0], [0], color='#95a5a6', lw=1.5, linestyle='--', label='Fuerzas Individuales ╌►'),
        Line2D([0], [0], marker='x', color='#8e44ad', linestyle='None', markersize=9, markeredgewidth=2, label='Punto de Campo (P)')
    ]
    plt.legend(handles=leyendas_elementos, loc='lower right', frameon=True, facecolor='#ffffff', edgecolor='#bdc3c7')
    
    plt.show()

if __name__ == "__main__":
    menu()
