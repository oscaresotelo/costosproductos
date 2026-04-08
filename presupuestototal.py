import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Minerva · Costos",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');
:root {
    --bg:#0d0f14; --surface:#151820; --surface2:#1c2030; --border:#252a3a;
    --accent:#c8ff4e; --accent2:#4ef0ff; --danger:#ff5a5a;
    --text:#f0f2fa; --muted:#a0a8bc; --green:#4ade80; --yellow:#fbbf24;
}
html,body,[data-testid="stAppViewContainer"]{background-color:var(--bg)!important;color:var(--text)!important;font-family:'DM Mono',monospace!important;font-size:16px!important;}
[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] *{color:var(--text)!important;}
h1,h2,h3{font-family:'Syne',sans-serif!important;color:var(--text)!important;}
.titulo-principal{font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;letter-spacing:-1px;line-height:1.1;color:var(--text);margin-bottom:0.2rem;}
.titulo-principal span{color:var(--accent);}
.subtitulo{font-family:'DM Mono',monospace;font-size:1rem;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-bottom:2rem;}
.metric-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:1.2rem 1.4rem;margin-bottom:0.6rem;}
.metric-label{font-size:0.88rem;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:0.3rem;font-family:'DM Mono',monospace;}
.metric-value{font-family:'Syne',sans-serif;font-size:2rem;font-weight:700;color:var(--text);}
.metric-value.accent{color:var(--accent);} .metric-value.green{color:var(--green);} .metric-value.danger{color:var(--danger);} .metric-value.yellow{color:var(--yellow);} .metric-value.blue{color:var(--accent2);}
.section-header{font-family:'Syne',sans-serif;font-size:0.9rem;letter-spacing:3px;text-transform:uppercase;color:var(--muted);padding:0.5rem 0;border-bottom:1px solid var(--border);margin:1.2rem 0 0.8rem 0;}
.costo-row{display:flex;justify-content:space-between;align-items:center;padding:0.5rem 0;border-bottom:1px solid var(--border);font-size:1rem;}
.costo-row:last-child{border-bottom:none;}
.costo-nombre{color:var(--text);} .costo-monto{font-family:'DM Mono',monospace;color:var(--accent);font-weight:500;} .costo-porce{font-size:0.88rem;color:var(--muted);margin-left:0.6rem;}
.pill{display:inline-block;padding:0.2rem 0.7rem;border-radius:20px;font-size:0.82rem;font-family:'DM Mono',monospace;letter-spacing:1px;text-transform:uppercase;}
.pill-green{background:rgba(74,222,128,0.15);color:var(--green);border:1px solid rgba(74,222,128,0.3);}
.pill-red{background:rgba(255,90,90,0.15);color:var(--danger);border:1px solid rgba(255,90,90,0.3);}
.pill-yellow{background:rgba(251,191,36,0.15);color:var(--yellow);border:1px solid rgba(251,191,36,0.3);}
.ganancia-bar-container{height:8px;background:var(--border);border-radius:4px;overflow:hidden;margin-top:0.4rem;}
.ganancia-bar{height:100%;border-radius:4px;transition:width 0.5s ease;}
.block-box{background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:1rem 1.2rem;margin-bottom:0.5rem;}
.tag-sin-precio{font-size:0.78rem;color:var(--danger);background:rgba(255,90,90,0.1);padding:0.1rem 0.5rem;border-radius:4px;border:1px solid rgba(255,90,90,0.2);}
.stNumberInput input{background:#ffffff!important;color:#111111!important;border:1px solid #cccccc!important;border-radius:8px!important;font-family:'DM Mono',monospace!important;font-size:1rem!important;font-weight:600!important;}
.stNumberInput input:focus{border-color:var(--accent)!important;box-shadow:0 0 0 2px rgba(200,255,78,0.25)!important;}
.stTextInput input{background:#ffffff!important;color:#111111!important;border:1px solid #cccccc!important;border-radius:8px!important;font-family:'DM Mono',monospace!important;font-size:1rem!important;}
.stSelectbox>div>div,.stSelectbox [data-baseweb="select"],.stSelectbox [data-baseweb="select"]>div,.stSelectbox [data-baseweb="select"]>div>div{background:#ffffff!important;background-color:#ffffff!important;color:#111111!important;border-color:#cccccc!important;border-radius:8px!important;font-family:'DM Mono',monospace!important;}
.stSelectbox [data-baseweb="select"] span,.stSelectbox [data-baseweb="select"] div[class*="ValueContainer"] *,.stSelectbox [data-baseweb="select"] div[class*="singleValue"],.stSelectbox [data-baseweb="select"] input{color:#111111!important;font-weight:600!important;font-family:'DM Mono',monospace!important;}
.stSelectbox [data-baseweb="select"] svg{fill:#111111!important;}
[data-baseweb="popover"],[data-baseweb="popover"] ul,[data-baseweb="menu"]{background:#ffffff!important;background-color:#ffffff!important;}
[data-baseweb="popover"] [role="option"],[data-baseweb="menu"] [role="option"]{background:#ffffff!important;color:#111111!important;font-family:'DM Mono',monospace!important;font-size:0.95rem!important;}
[data-baseweb="popover"] [role="option"]:hover,[data-baseweb="menu"] [role="option"]:hover,[data-baseweb="popover"] [aria-selected="true"],[data-baseweb="menu"] [aria-selected="true"]{background:#e8f5e9!important;color:#111111!important;}
.stNumberInput label,.stTextInput label,.stSelectbox label,.stSlider label,.stCheckbox label{color:var(--text)!important;font-size:0.92rem!important;font-family:'DM Mono',monospace!important;}
.stSlider>div{color:var(--text)!important;}
[data-testid="stMetric"]{display:none;}
div[data-testid="column"]{gap:0!important;}
.stButton>button{background:var(--accent)!important;color:#0d0f14!important;font-family:'Syne',sans-serif!important;font-weight:700!important;border:none!important;border-radius:8px!important;letter-spacing:1px!important;}
.stButton>button:hover{background:#d4ff66!important;}
.aviso{background:rgba(255,90,90,0.08);border:1px solid rgba(255,90,90,0.25);border-radius:8px;padding:0.8rem 1.1rem;font-size:0.96rem;color:var(--danger);margin-bottom:0.8rem;}
.info-box{background:rgba(78,240,255,0.05);border:1px solid rgba(78,240,255,0.2);border-radius:8px;padding:0.8rem 1.1rem;font-size:0.96rem;color:var(--accent2);margin-bottom:0.8rem;}
.success-box{background:rgba(74,222,128,0.05);border:1px solid rgba(74,222,128,0.25);border-radius:8px;padding:0.8rem 1.1rem;font-size:0.96rem;color:var(--green);margin-bottom:0.8rem;}
button[data-baseweb="tab"]{font-family:'DM Mono',monospace!important;font-size:0.75rem!important;letter-spacing:1px!important;color:var(--muted)!important;}
button[data-baseweb="tab"][aria-selected="true"]{color:var(--accent)!important;border-bottom:2px solid var(--accent)!important;}
[data-testid="stDataFrameResizable"]{background:var(--surface)!important;}
</style>
""", unsafe_allow_html=True)


# ── DB ─────────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_conn():
    db_path = Path("minerva.db")
    if not db_path.exists():
        db_path = Path(__file__).parent / "minerva.db"
    return sqlite3.connect(str(db_path), check_same_thread=False)

def query(sql, params=()):
    return pd.read_sql_query(sql, get_conn(), params=params)


# ── FUNCIONES DE DATOS (caché solo para datos que no dependen de cotización) ───

@st.cache_data(ttl=60)
def get_clientes():
    return query("SELECT id, nombre FROM clientes ORDER BY nombre")

@st.cache_data(ttl=60)
def get_productos_por_cliente(cliente_id):
    return query("""
        SELECT p.id, p.nombre, p.id_receta, p.envase_id, p.tipo_caja_id,
               e.descripcion as envase_desc, e.capacidad_litros
        FROM productos p
        LEFT JOIN envases e ON p.envase_id = e.id
        WHERE p.cliente_id = ?
        ORDER BY p.nombre
    """, (cliente_id,))

@st.cache_data(ttl=60)
def get_ultimo_precio_venta(cliente_id, producto_id, envase_id):
    df = query("""
        SELECT precio_unitario, fecha_desde
        FROM precios_productos_envasados
        WHERE cliente_id=? AND producto_id=? AND envase_id=? AND fecha_hasta IS NULL
        ORDER BY fecha_desde DESC LIMIT 1
    """, (cliente_id, producto_id, envase_id))
    if df.empty:
        df = query("""
            SELECT precio_unitario, fecha_desde
            FROM precios_productos_envasados
            WHERE cliente_id=? AND producto_id=? AND fecha_hasta IS NULL
            ORDER BY fecha_desde DESC LIMIT 1
        """, (cliente_id, producto_id))
    return (df.iloc[0]["precio_unitario"], df.iloc[0]["fecha_desde"]) if not df.empty else (None, None)

@st.cache_data(ttl=60)
def get_compra_cruda_mp(materia_prima_id):
    """
    Devuelve datos CRUDOS de la última compra de una MP.
    precio_unitario y costo_flete pueden estar en USD o ARS según campo 'moneda'.
    La conversión a ARS se hace FUERA con la cotización del usuario.
    """
    df_c = query("""
        SELECT numero_comprobante, cantidad, precio_unitario,
               costo_total, costo_flete, moneda, cotizacion_usd, fecha
        FROM compras_materia_prima
        WHERE materia_prima_id=? AND cantidad>0 AND precio_unitario>0
        ORDER BY fecha DESC LIMIT 1
    """, (materia_prima_id,))

    if df_c.empty:
        df_p = query("""
            SELECT precio_unitario, fecha, costo_flete
            FROM precios_materias_primas
            WHERE materia_prima_id=?
            ORDER BY fecha DESC LIMIT 1
        """, (materia_prima_id,))
        if df_p.empty:
            return None
        r = df_p.iloc[0]
        # precios_materias_primas ya están en ARS
        return {
            "precio_usd": None,
            "precio_ars_directo": float(r["precio_unitario"]),
            "flete_raw": float(r["costo_flete"] or 0),
            "flete_moneda": "ARS",
            "costo_total_ars": float(r["precio_unitario"]),
            "cantidad": 1.0,
            "moneda": "ARS",
            "fecha": str(r["fecha"]),
            "fuente": "tabla precios",
            "nro_comprobante": "",
        }

    r        = df_c.iloc[0]
    moneda   = str(r["moneda"] or "ARS").strip().upper()
    cantidad = float(r["cantidad"])
    p_raw    = float(r["precio_unitario"])
    c_total  = float(r["costo_total"] or 0)
    nro      = str(r["numero_comprobante"] or "").strip()

    return {
        "precio_usd":        p_raw if moneda == "USD" else None,
        "precio_ars_directo": p_raw if moneda == "ARS" else None,
        "flete_raw":         float(r["costo_flete"] or 0),
        "flete_moneda":      moneda,
        "costo_total_bd":    c_total,   # en ARS según lo que guardó la app
        "cantidad":          cantidad,
        "moneda":            moneda,
        "cotizacion_bd":     float(r["cotizacion_usd"] or 1.0),
        "fecha":             str(r["fecha"]),
        "fuente":            "compra directa" if not nro else f"comprobante {nro}",
        "nro_comprobante":   nro,
    }

@st.cache_data(ttl=60)
def get_comprobante_crudo(nro_comprobante):
    """Devuelve todas las filas de un comprobante con datos crudos."""
    return query("""
        SELECT costo_flete, moneda, cotizacion_usd, costo_total,
               precio_unitario, cantidad
        FROM compras_materia_prima
        WHERE numero_comprobante=? AND cantidad>0
    """, (nro_comprobante,))

@st.cache_data(ttl=60)
def get_ultimo_precio_envase(envase_id):
    df = query("""
        SELECT precio_unitario, fecha_ingreso FROM entradas_envases
        WHERE envase_id=? ORDER BY fecha_ingreso DESC LIMIT 1
    """, (envase_id,))
    return (df.iloc[0]["precio_unitario"], df.iloc[0]["fecha_ingreso"]) if not df.empty else (None, None)

@st.cache_data(ttl=60)
def get_info_caja(tipo_caja_id):
    df = query("SELECT descripcion, unidades_por_caja FROM tipo_cajas WHERE id=?", (tipo_caja_id,))
    return df.iloc[0] if not df.empty else None

@st.cache_data(ttl=60)
def get_overhead():
    df_g = query("SELECT importe_total FROM gastos")
    df_e = query("SELECT sueldo_base FROM empleados")
    tot_g = float(df_g["importe_total"].sum()) if not df_g.empty else 0
    tot_s = float(df_e["sueldo_base"].sum()) if not df_e.empty else 0
    return tot_g, tot_s, tot_g + tot_s

@st.cache_data(ttl=60)
def get_flete_receta(receta_id):
    df = query("""
        SELECT monto FROM costos_flete_recetas
        WHERE receta_id=? ORDER BY fecha_desde DESC LIMIT 1
    """, (receta_id,))
    return float(df.iloc[0]["monto"]) if not df.empty else 0.0

@st.cache_data(ttl=60)
def get_all_gastos():
    return query("""
        SELECT g.fecha_factura, g.beneficiario_nombre, ci.nombre as categoria,
               g.importe_total, g.moneda, g.observaciones
        FROM gastos g
        LEFT JOIN categorias_imputacion ci ON g.categoria_id=ci.id
        ORDER BY g.fecha_factura DESC
    """)

@st.cache_data(ttl=60)
def get_all_empleados():
    return query("SELECT nombre, sueldo_base FROM empleados ORDER BY nombre")

@st.cache_data(ttl=60)
def get_cotizacion_dolar():
    df = query("SELECT compra, venta, fecha_hora FROM cotizacion_dolar ORDER BY fecha_hora DESC LIMIT 1")
    if df.empty:
        return None, None, None
    return float(df.iloc[0]["compra"]), float(df.iloc[0]["venta"]), str(df.iloc[0]["fecha_hora"])

@st.cache_data(ttl=60)
def get_ingredientes_raw(receta_id):
    """Solo trae la lista de ingredientes sin precios (cacheable)."""
    return query("""
        SELECT ri.materia_prima_id, mp.nombre, ri.cantidad, ri.unidad
        FROM receta_ingredientes ri
        JOIN materias_primas mp ON ri.materia_prima_id = mp.id
        WHERE ri.receta_id=?
        ORDER BY ri.cantidad DESC
    """, (receta_id,))


# ── FUNCIONES QUE DEPENDEN DE LA COTIZACIÓN (sin caché) ───────────────────────

def convertir_a_ars(valor, moneda, cotizacion_usuario):
    """Convierte un valor a ARS usando la cotización actual del usuario."""
    if moneda == "USD":
        return valor * cotizacion_usuario
    return valor  # ya está en ARS

def calcular_precio_mp_ars(materia_prima_id, cotizacion_usuario):

    flete_unit_ars = 0.0  # ✅ SOLUCIÓN CLAVE

    datos = get_compra_cruda_mp(materia_prima_id)
    if datos is None:
        return None, None, 0.0, None, "sin precio"

    moneda  = datos["moneda"]
    fecha   = datos["fecha"]
    fuente  = datos["fuente"]
    nro     = datos["nro_comprobante"]
    cantidad = datos.get("cantidad", 1.0)

    # Precio base
    if datos["precio_usd"] is not None:
        precio_base_ars = datos["precio_usd"] * cotizacion_usuario
    else:
        precio_base_ars = datos["precio_ars_directo"] or 0.0

    costo_total_esta_compra_ars = precio_base_ars * cantidad

    if nro:
        df_comp = get_comprobante_crudo(nro)

        if not df_comp.empty:
            idx_max   = df_comp["costo_flete"].idxmax()
            row_flete = df_comp.loc[idx_max]

            # ✅ flete SIEMPRE en ARS
            flete_total_ars = float(row_flete["costo_flete"])

            suma_ars = 0.0
            for _, r in df_comp.iterrows():
                mon_r = str(r["moneda"] or "ARS").strip().upper()
                pu_r  = float(r["precio_unitario"])
                qty_r = float(r["cantidad"])
                suma_ars += convertir_a_ars(pu_r, mon_r, cotizacion_usuario) * qty_r

            suma_ars   = suma_ars or 1.0
            proporcion = costo_total_esta_compra_ars / suma_ars

            if cantidad > 0:
                flete_unit_ars = (flete_total_ars * proporcion) / cantidad

    else:
        flete_raw = datos.get("flete_raw", 0.0)
        if cantidad > 0:
            flete_unit_ars = flete_raw / cantidad  # ✅ ARS directo

    return precio_base_ars + flete_unit_ars, precio_base_ars, flete_unit_ars, fecha, fuente

def get_ingredientes_con_precio(receta_id, cotizacion_usuario):
    """Ingredientes con precio en ARS usando la cotización actual del usuario."""
    df = get_ingredientes_raw(receta_id).copy()
    precios, bases, fechas, fletes, fuentes = [], [], [], [], []
    for mp_id in df["materia_prima_id"]:
        p, pb, fl, f, src = calcular_precio_mp_ars(int(mp_id), cotizacion_usuario)
        precios.append(p); bases.append(pb); fletes.append(fl)
        fechas.append(f); fuentes.append(src)
    df["precio_unitario"] = precios
    df["precio_base"]     = bases
    df["precio_fecha"]    = fechas
    df["flete_unitario"]  = fletes
    df["fuente_precio"]   = fuentes
    df["costo_linea"]     = df["cantidad"] * df["precio_unitario"].fillna(0)
    return df


# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="titulo-principal">⚗️ Minerva · <span>Costos</span></div>
<div class="subtitulo">análisis de rentabilidad por producto</div>
""", unsafe_allow_html=True)


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-header">Filtros</div>', unsafe_allow_html=True)
    clientes_df  = get_clientes()
    cli_opciones = {row["nombre"]: row["id"] for _, row in clientes_df.iterrows()}
    cliente_sel  = st.selectbox("Cliente", list(cli_opciones.keys()))
    cliente_id   = cli_opciones[cliente_sel]

    productos_df = get_productos_por_cliente(cliente_id)
    if productos_df.empty:
        st.warning("Sin productos para este cliente.")
        st.stop()

    prod_opciones = {row["nombre"]: row for _, row in productos_df.iterrows()}
    prod_sel      = st.selectbox("Producto", list(prod_opciones.keys()))
    prod_row      = prod_opciones[prod_sel]

    st.markdown('<div class="section-header">Cotización Dólar</div>', unsafe_allow_html=True)
    dolar_compra_bd, dolar_venta_bd, dolar_fecha_bd = get_cotizacion_dolar()
    dolar_default = float(dolar_venta_bd or 1400.0)
    cotizacion_dolar = st.number_input(
        "Cotización USD → ARS",
        min_value=1.0, value=dolar_default, step=10.0,
        help="Se aplica a insumos y envases en USD. Se precarga desde la BD."
    )
    if dolar_fecha_bd:
        st.markdown(
            f'<div style="font-size:0.82rem;color:var(--muted);margin-top:-0.3rem;margin-bottom:0.5rem;">'
            f'BD: compra ${dolar_compra_bd:,.0f} / venta ${dolar_venta_bd:,.0f}<br>'
            f'Actualizado: {dolar_fecha_bd[:10]}</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-header">Parámetros</div>', unsafe_allow_html=True)
    capacidad_planta = st.number_input(
        "Capacidad planta (litros/mes)", min_value=1000, max_value=200000,
        value=32000, step=1000,
    )
    margen_objetivo = st.slider("Margen deseado (%)", min_value=0, max_value=200, value=30)
    precio_venta_manual = st.number_input(
        "Precio venta manual (ARS, 0 = BD)",
        min_value=0.0, value=0.0, step=100.0,
    )

    st.markdown('<div class="section-header">Opciones</div>', unsafe_allow_html=True)
    mostrar_grafico_ing      = st.checkbox("Gráfico ingredientes", value=True)
    mostrar_overhead_detalle = st.checkbox("Detalle overhead", value=False)


# ── CÁLCULOS ──────────────────────────────────────────────────────────────────
receta_id    = prod_row.get("id_receta")
envase_id    = prod_row.get("envase_id")
tipo_caja_id = prod_row.get("tipo_caja_id")
prod_id      = int(prod_row["id"])
cap_litros   = float(prod_row.get("capacidad_litros") or 1.0)
envase_desc  = prod_row.get("envase_desc") or "—"

# Insumos — recalcula con cotización actual del usuario
costo_insumos     = 0.0
ingred_df         = pd.DataFrame()
avisos_sin_precio = []
if receta_id and str(receta_id).strip() not in ("", "None"):
    ingred_df = get_ingredientes_con_precio(int(receta_id), cotizacion_dolar)
    sin_p_df  = ingred_df[ingred_df["precio_unitario"].isna() | (ingred_df["precio_unitario"] == 0)]
    avisos_sin_precio = sin_p_df["nombre"].tolist()
    costo_insumos = ingred_df["costo_linea"].sum() * cap_litros / 200.0
else:
    avisos_sin_precio = ["Producto sin receta asignada"]

# Envase (USD → ARS con cotización usuario)
precio_envase_usd = 0.0
fecha_envase      = None
if envase_id:
    _pe, fecha_envase = get_ultimo_precio_envase(int(envase_id))
    precio_envase_usd = float(_pe or 0)
costo_envase = precio_envase_usd * cotizacion_dolar

# Caja
costo_caja_por_unidad = 0.0
caja_info = None
if tipo_caja_id:
    caja_info = get_info_caja(int(tipo_caja_id))

# Overhead (1 litro fijo)
total_gastos, total_sueldos, total_overhead = get_overhead()
overhead_por_litro  = total_overhead / capacidad_planta if capacidad_planta > 0 else 0
overhead_por_unidad = overhead_por_litro * 1.0

# Flete de receta
flete_receta_por_unidad = 0.0
if receta_id and str(receta_id).strip() not in ("", "None"):
    flete_receta_por_unidad = get_flete_receta(int(receta_id)) * cap_litros / 200.0

# Totales
costo_total     = costo_insumos + costo_envase + costo_caja_por_unidad + overhead_por_unidad + flete_receta_por_unidad
precio_bd, fecha_precio_bd = get_ultimo_precio_venta(cliente_id, prod_id, int(envase_id) if envase_id else 0)
precio_venta    = precio_venta_manual if precio_venta_manual > 0 else float(precio_bd or 0)
precio_sugerido = costo_total * (1 + margen_objetivo / 100) if costo_total > 0 else 0
ganancia_abs    = precio_venta - costo_total if precio_venta > 0 else 0
ganancia_pct    = (ganancia_abs / precio_venta * 100) if precio_venta > 0 else 0
markup_pct      = (ganancia_abs / costo_total * 100) if costo_total > 0 else 0


# ── AVISOS ────────────────────────────────────────────────────────────────────
for av in avisos_sin_precio[:3]:
    st.markdown(f'<div class="aviso">⚠ Sin precio: <b>{av}</b></div>', unsafe_allow_html=True)
if precio_venta == 0:
    st.markdown('<div class="info-box">ℹ Sin precio de venta registrado. Ingresá uno en el panel lateral.</div>', unsafe_allow_html=True)


# ── TABS ──────────────────────────────────────────────────────────────────────
tabs = st.tabs(["📊 Resumen", "🧪 Ingredientes", "🏭 Overhead", "📋 Comparativa", "🧮 Simulador"])


# ══ TAB 1 — RESUMEN ══════════════════════════════════════════════════════════
with tabs[0]:
    col1, col2 = st.columns([1.1, 0.9], gap="medium")

    with col1:
        st.markdown('<div class="section-header">Desglose de costo por unidad</div>', unsafe_allow_html=True)

        def fila_costo(nombre, valor, total, icono=""):
            pct = (valor / total * 100) if total > 0 else 0
            st.markdown(f"""
            <div class="costo-row">
                <span class="costo-nombre">{icono} {nombre}</span>
                <span>
                    <span class="costo-monto">$ {valor:,.2f}</span>
                    <span class="costo-porce">{pct:.1f}%</span>
                </span>
            </div>""", unsafe_allow_html=True)

        fila_costo("Insumos (receta)", costo_insumos, costo_total, "🧬")
        fila_costo("Envase", costo_envase, costo_total, "🫙")
        fila_costo("Caja / Embalaje", costo_caja_por_unidad, costo_total, "📦")
        fila_costo("Overhead (indirectos)", overhead_por_unidad, costo_total, "🏭")
        fila_costo("Flete receta", flete_receta_por_unidad, costo_total, "🚛")

        st.markdown(f"""
        <div style="margin-top:0.8rem;padding:0.8rem 0;border-top:2px solid var(--accent);">
            <div class="costo-row" style="border:none;padding:0;">
                <span style="font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;">COSTO TOTAL UNITARIO</span>
                <span style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.2rem;color:var(--accent);">$ {costo_total:,.2f}</span>
            </div>
        </div>""", unsafe_allow_html=True)

        fecha_envase_html = (
            f"<div style='font-size:0.88rem;color:var(--muted);margin-top:0.4rem;'>"
            f"Último precio: <b>USD {precio_envase_usd:,.3f}</b> = <b>ARS $ {costo_envase:,.2f}</b> ({fecha_envase})</div>"
            if fecha_envase else ""
        )
        st.markdown(f"""
        <div class="block-box" style="margin-top:1rem;">
            <div style="font-size:0.85rem;letter-spacing:2px;color:var(--muted);text-transform:uppercase;margin-bottom:0.5rem;">Envase / Presentación</div>
            <div style="font-size:1.05rem;">{envase_desc} &nbsp;·&nbsp; <span style="color:var(--muted);">{cap_litros} L/unidad</span></div>
            {fecha_envase_html}
        </div>""", unsafe_allow_html=True)

        if caja_info is not None:
            st.markdown(f"""
            <div class="block-box">
                <div style="font-size:0.85rem;letter-spacing:2px;color:var(--muted);text-transform:uppercase;margin-bottom:0.5rem;">Caja</div>
                <div style="font-size:1.05rem;">{caja_info['descripcion']}</div>
                <div style="font-size:0.88rem;color:var(--muted);margin-top:0.3rem;">{caja_info['unidades_por_caja']} unidades por caja</div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">Precio de venta y ganancia</div>', unsafe_allow_html=True)

        fuente_precio = "manual" if precio_venta_manual > 0 else ("base de datos" if precio_bd else "—")
        fecha_venta_html = (
            f"<div style='font-size:0.82rem;color:var(--muted);margin-top:0.2rem;'>vigente desde {fecha_precio_bd}</div>"
            if fecha_precio_bd and precio_venta_manual == 0 else ""
        )
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Precio de venta ({fuente_precio})</div>
            <div class="metric-value blue">$ {precio_venta:,.2f}</div>
            {fecha_venta_html}
        </div>""", unsafe_allow_html=True)

        color_gan = "green" if ganancia_abs > 0 else "danger"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Ganancia por unidad</div>
            <div class="metric-value {color_gan}">$ {ganancia_abs:,.2f}</div>
        </div>""", unsafe_allow_html=True)

        pill_class = "pill-green" if ganancia_pct >= 20 else ("pill-yellow" if ganancia_pct >= 10 else "pill-red")
        bar_color  = "var(--green)" if ganancia_pct >= 20 else ("var(--yellow)" if ganancia_pct >= 10 else "var(--danger)")
        bar_width  = min(abs(ganancia_pct), 100)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Margen neto &nbsp;<span class="pill {pill_class}">{ganancia_pct:.1f}%</span></div>
            <div class="metric-value {color_gan}">{ganancia_pct:.1f}%</div>
            <div class="ganancia-bar-container">
                <div class="ganancia-bar" style="width:{bar_width}%;background:{bar_color};"></div>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Markup sobre costo</div>
            <div class="metric-value yellow">{markup_pct:.1f}%</div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:1.4rem;">Precio sugerido</div>', unsafe_allow_html=True)
        diferencia = precio_sugerido - precio_venta
        dif_pct    = (diferencia / precio_venta * 100) if precio_venta > 0 else 0
        dif_color  = "var(--green)" if diferencia <= 0 else "var(--danger)"
        dif_signo  = "+" if diferencia > 0 else ""
        st.markdown(f"""
        <div class="block-box">
            <div style="font-size:0.85rem;letter-spacing:2px;color:var(--muted);text-transform:uppercase;margin-bottom:0.6rem;">
                Con {margen_objetivo}% de margen objetivo
            </div>
            <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:var(--accent2);">
                $ {precio_sugerido:,.2f}
            </div>
            <div style="font-size:0.9rem;margin-top:0.5rem;color:{dif_color};">
                {dif_signo}$ {diferencia:,.2f} &nbsp;({dif_signo}{dif_pct:.1f}%) vs. precio actual
            </div>
        </div>""", unsafe_allow_html=True)


# ══ TAB 2 — INGREDIENTES ═════════════════════════════════════════════════════
with tabs[1]:
    if ingred_df.empty:
        st.markdown('<div class="aviso">Sin receta asignada a este producto.</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="info-box">Receta ID: <b>{receta_id}</b> · '
            f'Escala: 200 L base → {cap_litros} L/unidad ({cap_litros/200*100:.1f}%) · '
            f'Precios en ARS al dólar $ {cotizacion_dolar:,.0f} · '
            f'<b>Flete prorrateado por comprobante</b></div>',
            unsafe_allow_html=True
        )

        c1, c2, c3, c4, c5, c6 = st.columns([2.5, 0.9, 1.1, 1, 1, 1.3])
        for col, h in zip([c1,c2,c3,c4,c5,c6], ["Ingrediente","Cantidad","$ base/u","Flete/u","Costo línea","Fuente"]):
            with col:
                st.markdown(f'<div style="font-size:0.82rem;letter-spacing:2px;color:var(--muted);text-transform:uppercase;">{h}</div>', unsafe_allow_html=True)

        st.markdown('<hr style="border-color:var(--border);margin:0.4rem 0;">', unsafe_allow_html=True)

        for _, row in ingred_df.iterrows():
            sin_p          = pd.isna(row["precio_unitario"]) or row["precio_unitario"] == 0
            costo_escalado = row["costo_linea"] * cap_litros / 200.0
            flete_u        = float(row.get("flete_unitario", 0) or 0)
            fuente         = str(row.get("fuente_precio", "") or "")
            p_base_solo    = float(row.get("precio_base") or 0) if not sin_p else 0

            c1, c2, c3, c4, c5, c6 = st.columns([2.5, 0.9, 1.1, 1, 1, 1.3])
            with c1:
                tag = '<span class="tag-sin-precio">sin precio</span>' if sin_p else ""
                st.markdown(f'<div style="font-size:0.92rem;padding:0.3rem 0;">{row["nombre"]} {tag}</div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div style="font-size:0.92rem;padding:0.3rem 0;color:var(--muted);">{row["cantidad"]} {row["unidad"]}</div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div style="font-size:0.92rem;padding:0.3rem 0;color:var(--accent2);">$ {p_base_solo:,.2f}</div>', unsafe_allow_html=True)
            with c4:
                fc = "var(--yellow)" if flete_u > 0 else "var(--muted)"
                st.markdown(f'<div style="font-size:0.92rem;padding:0.3rem 0;color:{fc};">$ {flete_u:,.2f}</div>', unsafe_allow_html=True)
            with c5:
                cc = "var(--muted)" if sin_p else "var(--accent)"
                st.markdown(f'<div style="font-size:0.92rem;padding:0.3rem 0;color:{cc};">$ {costo_escalado:,.2f}</div>', unsafe_allow_html=True)
            with c6:
                st.markdown(f'<div style="font-size:0.75rem;padding:0.3rem 0;color:var(--muted);">{fuente}</div>', unsafe_allow_html=True)

        st.markdown('<hr style="border-color:var(--border);margin:0.6rem 0;">', unsafe_allow_html=True)
        ct1, _, _, _, ct5, _ = st.columns([2.5, 0.9, 1.1, 1, 1, 1.3])
        with ct1:
            st.markdown('<div style="font-family:Syne,sans-serif;font-weight:700;font-size:1.05rem;">TOTAL INSUMOS</div>', unsafe_allow_html=True)
        with ct5:
            st.markdown(f'<div style="font-family:Syne,sans-serif;font-weight:800;font-size:1.05rem;color:var(--accent);">$ {costo_insumos:,.2f}</div>', unsafe_allow_html=True)

        if mostrar_grafico_ing:
            st.markdown('<div class="section-header" style="margin-top:1.5rem;">Participación por ingrediente</div>', unsafe_allow_html=True)
            df_chart = ingred_df.copy()
            df_chart["costo_escalado"] = df_chart["costo_linea"] * cap_litros / 200.0
            df_chart = df_chart[df_chart["costo_escalado"] > 0].sort_values("costo_escalado", ascending=False)
            if not df_chart.empty:
                st.bar_chart(df_chart.set_index("nombre")["costo_escalado"], color="#c8ff4e")


# ══ TAB 3 — OVERHEAD ═════════════════════════════════════════════════════════
with tabs[2]:
    col_ov1, col_ov2 = st.columns(2, gap="medium")

    with col_ov1:
        st.markdown('<div class="section-header">Estructura de overhead</div>', unsafe_allow_html=True)

        def mini_card(label, valor, color="var(--text)"):
            st.markdown(f"""
            <div class="metric-card" style="padding:0.9rem 1.1rem;">
                <div class="metric-label">{label}</div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.3rem;color:{color};">$ {valor:,.0f}</div>
            </div>""", unsafe_allow_html=True)

        mini_card("Total gastos operativos", total_gastos, "var(--accent2)")
        mini_card("Total sueldos empleados", total_sueldos, "var(--yellow)")
        mini_card("OVERHEAD TOTAL", total_overhead, "var(--accent)")

        st.markdown(f"""
        <div class="block-box" style="margin-top:1rem;">
            <div class="metric-label">Capacidad de planta</div>
            <div style="font-size:1.2rem;font-weight:700;">{capacidad_planta:,.0f} L / mes</div>
            <div style="font-size:0.92rem;color:var(--muted);margin-top:0.5rem;">
                Overhead por litro: <b style="color:var(--accent);">$ {overhead_por_litro:,.2f}</b>
            </div>
            <div style="font-size:0.92rem;color:var(--muted);">
                Overhead por unidad (1L fijo): <b style="color:var(--accent);">$ {overhead_por_unidad:,.2f}</b>
            </div>
        </div>""", unsafe_allow_html=True)

    with col_ov2:
        st.markdown('<div class="section-header">Empleados</div>', unsafe_allow_html=True)
        for _, e in get_all_empleados().iterrows():
            st.markdown(f"""
            <div class="costo-row">
                <span class="costo-nombre">{e['nombre']}</span>
                <span class="costo-monto">$ {e['sueldo_base']:,.0f}</span>
            </div>""", unsafe_allow_html=True)

    if mostrar_overhead_detalle:
        st.markdown('<div class="section-header" style="margin-top:1.5rem;">Detalle de gastos</div>', unsafe_allow_html=True)
        gastos_df = get_all_gastos()
        if not gastos_df.empty:
            st.dataframe(
                gastos_df, use_container_width=True, hide_index=True,
                column_config={
                    "importe_total": st.column_config.NumberColumn("Importe", format="$ %.0f"),
                    "fecha_factura": "Fecha", "beneficiario_nombre": "Beneficiario",
                    "categoria": "Categoría", "moneda": "Moneda", "observaciones": "Obs.",
                }
            )


# ══ TAB 4 — COMPARATIVA ══════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header">Todos los productos del cliente</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="info-box">Precios calculados al dólar $ {cotizacion_dolar:,.0f} · '
        'Flete prorrateado por comprobante · Solo productos con precio de venta.</div>',
        unsafe_allow_html=True
    )

    rows_comp = []
    for _, prod in productos_df.iterrows():
        p_id  = int(prod["id"])
        p_rec = prod.get("id_receta")
        p_env = prod.get("envase_id")
        p_cap = float(prod.get("capacidad_litros") or 1.0)

        ci = 0.0
        if p_rec and str(p_rec).strip() not in ("", "None"):
            try:
                idf = get_ingredientes_con_precio(int(p_rec), cotizacion_dolar)
                ci  = idf["costo_linea"].sum() * p_cap / 200.0
            except Exception:
                ci = 0.0

        ce = 0.0
        if p_env:
            try:
                pe, _ = get_ultimo_precio_envase(int(p_env))
                ce    = float(pe or 0) * cotizacion_dolar
            except Exception:
                ce = 0.0

        oh = overhead_por_litro * 1.0

        fl = 0.0
        if p_rec and str(p_rec).strip() not in ("", "None"):
            try:
                fl = get_flete_receta(int(p_rec)) * p_cap / 200.0
            except Exception:
                fl = 0.0

        costo_u = ci + ce + oh + fl
        pv, _   = get_ultimo_precio_venta(cliente_id, p_id, int(p_env) if p_env else 0)
        pv      = float(pv or 0)
        if pv == 0:
            continue

        gan    = pv - costo_u
        margen = (gan / pv * 100) if pv > 0 else 0
        rows_comp.append({
            "Producto":      prod["nombre"],
            "Envase":        prod.get("envase_desc") or "—",
            "Cap (L)":       p_cap,
            "Costo insumos": round(ci, 2),
            "Costo envase":  round(ce, 2),
            "Overhead":      round(oh, 2),
            "Flete":         round(fl, 2),
            "COSTO TOTAL":   round(costo_u, 2),
            "Precio venta":  round(pv, 2),
            "Ganancia":      round(gan, 2),
            "Margen %":      round(margen, 1),
        })

    if rows_comp:
        df_comp = pd.DataFrame(rows_comp).sort_values("Margen %", ascending=False)
        st.dataframe(
            df_comp, use_container_width=True, hide_index=True,
            column_config={
                "Costo insumos": st.column_config.NumberColumn(format="$ %.2f"),
                "Costo envase":  st.column_config.NumberColumn(format="$ %.2f"),
                "Overhead":      st.column_config.NumberColumn(format="$ %.2f"),
                "Flete":         st.column_config.NumberColumn(format="$ %.2f"),
                "COSTO TOTAL":   st.column_config.NumberColumn(format="$ %.2f"),
                "Precio venta":  st.column_config.NumberColumn(format="$ %.2f"),
                "Ganancia":      st.column_config.NumberColumn(format="$ %.2f"),
                "Margen %":      st.column_config.ProgressColumn("Margen %", min_value=0, max_value=100, format="%.1f%%"),
            }
        )
        st.markdown('<div class="section-header" style="margin-top:1.5rem;">Margen por producto</div>', unsafe_allow_html=True)
        st.bar_chart(df_comp.set_index("Producto")["Margen %"], color="#4ef0ff")
    else:
        st.markdown('<div class="aviso">No hay productos con precio de venta registrado para este cliente.</div>', unsafe_allow_html=True)


# ══ TAB 5 — SIMULADOR DE PRESUPUESTO ════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header">Simulador de presupuesto</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="info-box">Armá un presupuesto combinando varios productos y cantidades. '
        'Los costos se calculan con la cotización del dólar del panel lateral.</div>',
        unsafe_allow_html=True
    )

    # Inicializar lista de items en session_state
    if "presupuesto_items" not in st.session_state:
        st.session_state.presupuesto_items = []

    # ── Agregar producto ──
    col_ag1, col_ag2, col_ag3 = st.columns([3, 1, 1])
    with col_ag1:
        prod_sim = st.selectbox("Producto a agregar", list(prod_opciones.keys()), key="sim_prod")
    with col_ag2:
        cant_sim = st.number_input("Unidades", min_value=1, value=100, step=10, key="sim_cant")
    with col_ag3:
        st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)
        if st.button("➕ Agregar"):
            row_s      = prod_opciones[prod_sim]
            p_id_s     = int(row_s["id"])
            p_rec_s    = row_s.get("id_receta")
            p_env_s    = row_s.get("envase_id")
            p_cap_s    = float(row_s.get("capacidad_litros") or 1.0)
            p_env_desc = row_s.get("envase_desc") or "—"

            ci_s = 0.0
            if p_rec_s and str(p_rec_s).strip() not in ("", "None"):
                try:
                    idf_s = get_ingredientes_con_precio(int(p_rec_s), cotizacion_dolar)
                    ci_s  = idf_s["costo_linea"].sum() * p_cap_s / 200.0
                except Exception:
                    ci_s = 0.0

            ce_s = 0.0
            if p_env_s:
                try:
                    pe_s, _ = get_ultimo_precio_envase(int(p_env_s))
                    ce_s    = float(pe_s or 0) * cotizacion_dolar
                except Exception:
                    ce_s = 0.0

            fl_s = 0.0
            if p_rec_s and str(p_rec_s).strip() not in ("", "None"):
                try:
                    fl_s = get_flete_receta(int(p_rec_s)) * p_cap_s / 200.0
                except Exception:
                    fl_s = 0.0

            costo_u_s = ci_s + ce_s + overhead_por_unidad + fl_s
            pv_s, _   = get_ultimo_precio_venta(cliente_id, p_id_s, int(p_env_s) if p_env_s else 0)
            pv_s      = float(pv_s or 0)

            st.session_state.presupuesto_items.append({
                "producto":    prod_sim,
                "envase":      p_env_desc,
                "unidades":    cant_sim,
                "costo_unit":  round(costo_u_s, 2),
                "precio_venta": round(pv_s, 2),
                "costo_total": round(costo_u_s * cant_sim, 2),
                "venta_total": round(pv_s * cant_sim, 2),
            })
            st.rerun()

    # ── Tabla del presupuesto ──
    if st.session_state.presupuesto_items:
        st.markdown('<div class="section-header">Items del presupuesto</div>', unsafe_allow_html=True)

        items = st.session_state.presupuesto_items
        df_pres = pd.DataFrame(items)

        # Edición de unidades y eliminación
        indices_a_borrar = []
        for i, item in enumerate(items):
            c1, c2, c3, c4, c5, c6 = st.columns([2.5, 0.8, 1.1, 1.1, 1.1, 0.5])
            with c1:
                st.markdown(f'<div style="font-size:0.92rem;padding:0.5rem 0;">{item["producto"]}<br><span style="font-size:0.75rem;color:var(--muted);">{item["envase"]}</span></div>', unsafe_allow_html=True)
            with c2:
                nueva_cant = st.number_input("u", min_value=1, value=item["unidades"], step=10, key=f"cant_{i}", label_visibility="collapsed")
                if nueva_cant != item["unidades"]:
                    st.session_state.presupuesto_items[i]["unidades"]    = nueva_cant
                    st.session_state.presupuesto_items[i]["costo_total"] = round(item["costo_unit"] * nueva_cant, 2)
                    st.session_state.presupuesto_items[i]["venta_total"] = round(item["precio_venta"] * nueva_cant, 2)
                    st.rerun()
            with c3:
                st.markdown(f'<div style="font-size:0.88rem;padding:0.5rem 0;color:var(--muted);">Costo: <b style="color:var(--text);">$ {item["costo_unit"]:,.0f}</b></div>', unsafe_allow_html=True)
            with c4:
                gan_item = item["precio_venta"] - item["costo_unit"]
                color_gi = "var(--green)" if gan_item > 0 else "var(--danger)"
                st.markdown(f'<div style="font-size:0.88rem;padding:0.5rem 0;">Gan: <b style="color:{color_gi};">$ {gan_item:,.0f}</b></div>', unsafe_allow_html=True)
            with c5:
                st.markdown(f'<div style="font-size:0.88rem;padding:0.5rem 0;color:var(--accent);">Total: <b>$ {item["costo_total"]:,.0f}</b></div>', unsafe_allow_html=True)
            with c6:
                if st.button("🗑", key=f"del_{i}"):
                    indices_a_borrar.append(i)

        if indices_a_borrar:
            st.session_state.presupuesto_items = [
                x for j, x in enumerate(st.session_state.presupuesto_items) if j not in indices_a_borrar
            ]
            st.rerun()

        # ── Totales del presupuesto ──
        st.markdown('<hr style="border-color:var(--border);margin:0.8rem 0;">', unsafe_allow_html=True)

        total_costo_pres  = sum(i["costo_total"] for i in items)
        total_venta_pres  = sum(i["venta_total"] for i in items)
        total_gan_pres    = total_venta_pres - total_costo_pres
        margen_pres       = (total_gan_pres / total_venta_pres * 100) if total_venta_pres > 0 else 0
        total_unidades    = sum(i["unidades"] for i in items)

        mc1, mc2, mc3, mc4 = st.columns(4)
        def metric_sim(col, label, valor, color="var(--accent)"):
            with col:
                st.markdown(f"""
                <div class="metric-card" style="padding:0.9rem 1rem;">
                    <div class="metric-label">{label}</div>
                    <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.4rem;color:{color};">$ {valor:,.0f}</div>
                </div>""", unsafe_allow_html=True)

        metric_sim(mc1, f"Costo total ({total_unidades} u)", total_costo_pres, "var(--accent2)")
        metric_sim(mc2, "Venta total (precio BD)", total_venta_pres, "var(--text)")
        metric_sim(mc3, "Ganancia estimada", total_gan_pres, "var(--green)" if total_gan_pres > 0 else "var(--danger)")

        with mc4:
            pill_p = "pill-green" if margen_pres >= 20 else ("pill-yellow" if margen_pres >= 10 else "pill-red")
            st.markdown(f"""
            <div class="metric-card" style="padding:0.9rem 1rem;">
                <div class="metric-label">Margen promedio</div>
                <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.4rem;color:var(--yellow);">{margen_pres:.1f}%</div>
            </div>""", unsafe_allow_html=True)

        # ── Ajuste de precio de venta del presupuesto ──
        st.markdown('<div class="section-header" style="margin-top:1rem;">Ajustar precio de venta del presupuesto</div>', unsafe_allow_html=True)

        col_adj1, col_adj2 = st.columns(2)
        with col_adj1:
            margen_pres_obj = st.slider(
                "Margen objetivo del presupuesto (%)",
                min_value=0, max_value=150, value=30, key="margen_presupuesto"
            )
            precio_presup_sugerido = total_costo_pres * (1 + margen_pres_obj / 100)
            diferencia_presup = precio_presup_sugerido - total_venta_pres
            dif_signo_p = "+" if diferencia_presup > 0 else ""
            dif_color_p = "var(--danger)" if diferencia_presup > 0 else "var(--green)"
            st.markdown(f"""
            <div class="block-box">
                <div style="font-size:0.85rem;color:var(--muted);margin-bottom:0.4rem;">Precio total sugerido con {margen_pres_obj}% margen</div>
                <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:var(--accent2);">$ {precio_presup_sugerido:,.0f}</div>
                <div style="font-size:0.88rem;margin-top:0.3rem;color:{dif_color_p};">{dif_signo_p}$ {diferencia_presup:,.0f} vs. precios actuales de BD</div>
            </div>""", unsafe_allow_html=True)

        with col_adj2:
            st.markdown('<div style="font-size:0.85rem;color:var(--muted);margin-bottom:0.6rem;">Desglose del presupuesto</div>', unsafe_allow_html=True)
            for item in items:
                pct_item = (item["costo_total"] / total_costo_pres * 100) if total_costo_pres > 0 else 0
                st.markdown(f"""
                <div class="costo-row" style="font-size:0.88rem;">
                    <span style="color:var(--text);">{item['producto'][:30]} x{item['unidades']}</span>
                    <span><span style="color:var(--accent);">$ {item['costo_total']:,.0f}</span>
                    <span style="color:var(--muted);margin-left:0.4rem;">{pct_item:.0f}%</span></span>
                </div>""", unsafe_allow_html=True)

        # ── Botón limpiar ──
        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
        if st.button("🗑 Limpiar presupuesto"):
            st.session_state.presupuesto_items = []
            st.rerun()

    else:
        st.markdown("""
        <div class="block-box" style="text-align:center;padding:2rem;">
            <div style="font-size:2rem;margin-bottom:0.5rem;">📋</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.1rem;color:var(--muted);">
                Seleccioná productos y cantidad para armar el presupuesto
            </div>
        </div>""", unsafe_allow_html=True)