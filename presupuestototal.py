import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
import io
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

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
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    
    # Asegurar que existan las tablas de persistencia para el Overhead personalizado
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ajustes_overhead (
            tipo TEXT,              -- 'gasto' o 'empleado'
            referencia_id INTEGER,
            valor_ajustado REAL,
            imputar_costo INTEGER DEFAULT 1, -- 1 = Imputar al costo unitario, 0 = Gasto General
            PRIMARY KEY (tipo, referencia_id)
        )
    """)
    conn.commit()
    return conn

def query(sql, params=()):
    return pd.read_sql_query(sql, get_conn(), params=params)


# ── PERSISTENCIA DE AJUSTES EN DB ─────────────────────────────────────────────

def guardar_ajuste_overhead_bd(tipo, ref_id, valor, imputar_costo=1):
    conn = get_conn()
    conn.execute("""
        INSERT INTO ajustes_overhead (tipo, referencia_id, valor_ajustado, imputar_costo)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(tipo, referencia_id) 
        DO UPDATE SET valor_ajustado=excluded.valor_ajustado, imputar_costo=excluded.imputar_costo
    """, (tipo, ref_id, valor, imputar_costo))
    conn.commit()

def eliminar_ajustes_overhead_bd():
    conn = get_conn()
    conn.execute("DELETE FROM ajustes_overhead")
    conn.commit()

def cargar_ajustes_overhead_bd():
    try:
        df = query("SELECT tipo, referencia_id, valor_ajustado, imputar_costo FROM ajustes_overhead")
        return df
    except Exception:
        return pd.DataFrame()


# ── ACTUALIZACIÓN DE RECETAS EN DB ────────────────────────────────────────────

def actualizar_cantidad_ingrediente_bd(receta_id, materia_prima_id, nueva_cantidad):
    conn = get_conn()
    conn.execute("""
        UPDATE receta_ingredientes 
        SET cantidad = ? 
        WHERE receta_id = ? AND materia_prima_id = ?
    """, (nueva_cantidad, receta_id, materia_prima_id))
    conn.commit()
    # Limpiamos cachés para que se reflejen los cambios inmediatamente
    get_ingredientes_raw.clear()


# ── ACTUALIZACIÓN DE ENVASE Y FLETE EN DB (SOLUCIÓN NOT NULL CONSTRAINT) ──────

def insertar_precio_envase_bd(envase_id, nuevo_precio):
    conn = get_conn()
    hoy = date.today().strftime("%Y-%m-%d")
    cursor = conn.cursor()
    
    # 1. Intentar buscar el último proveedor_id registrado para ese envase específico
    cursor.execute("""
        SELECT proveedor_id FROM entradas_envases 
        WHERE envase_id = ? AND proveedor_id IS NOT NULL 
        ORDER BY fecha_ingreso DESC LIMIT 1
    """, (envase_id,))
    row = cursor.fetchone()
    proveedor_id = row[0] if row else None
    
    # 2. Si no hay registros previos del envase, buscar el primer proveedor de la tabla proveedores
    if proveedor_id is None:
        try:
            cursor.execute("SELECT id FROM proveedores LIMIT 1")
            row_prov = cursor.fetchone()
            if row_prov:
                proveedor_id = row_prov[0]
        except sqlite3.OperationalError:
            pass
            
    # 3. Si sigue sin resolverse, buscar cualquier proveedor_id en entradas_envases
    if proveedor_id is None:
        try:
            cursor.execute("SELECT proveedor_id FROM entradas_envases WHERE proveedor_id IS NOT NULL LIMIT 1")
            row_any = cursor.fetchone()
            if row_any:
                proveedor_id = row_any[0]
        except Exception:
            pass
            
    # 4. Fallback final por defecto para el proveedor
    if proveedor_id is None:
        proveedor_id = 1
        
    # 5. Obtener o definir un número de comprobante para cumplir con la restricción NOT NULL de la DB
    cursor.execute("""
        SELECT numero_comprobante FROM entradas_envases 
        WHERE envase_id = ? AND numero_comprobante IS NOT NULL AND numero_comprobante != ''
        ORDER BY fecha_ingreso DESC LIMIT 1
    """, (envase_id,))
    row_comp = cursor.fetchone()
    
    if row_comp:
        numero_comprobante = row_comp[0]
    else:
        # Generar un comprobante simulado único con la fecha para evitar colisiones
        numero_comprobante = f"AJUSTE-{hoy}"

    # 6. Intentar obtener la última cantidad ingresada de entradas_envases para mantener la estructura o colocar 0/1
    # Como es un ajuste de precio, usualmente la cantidad ingresada por defecto para no desbalancear stock puede ser 0 o 1.
    # Colocaremos 0 como cantidad ingresada para que actúe únicamente como actualización de precio histórico.
    cantidad_ingresada = 0
    try:
        cursor.execute("""
            SELECT cantidad_ingresada FROM entradas_envases 
            WHERE envase_id = ? AND cantidad_ingresada IS NOT NULL
            ORDER BY fecha_ingreso DESC LIMIT 1
        """, (envase_id,))
        row_cant = cursor.fetchone()
        if row_cant:
            # Puedes optar por usar la última cantidad o dejarla en 0 para evitar distorsiones ficticias de stock.
            # Dejaremos 0 por seguridad de integridad de stock físico, o 1 si la BD requiere cantidad_ingresada > 0.
            cantidad_ingresada = int(row_cant[0]) if int(row_cant[0]) > 0 else 0
    except Exception:
        pass

    # Insertamos con los campos obligatorios 'numero_comprobante' y 'cantidad_ingresada' provistos
    conn.execute("""
        INSERT INTO entradas_envases (envase_id, precio_unitario, fecha_ingreso, proveedor_id, numero_comprobante, cantidad_ingresada)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (envase_id, nuevo_precio, hoy, proveedor_id, numero_comprobante, cantidad_ingresada))
    conn.commit()
    get_ultimo_precio_envase.clear()

def insertar_flete_receta_bd(receta_id, nuevo_flete):
    conn = get_conn()
    hoy = date.today().strftime("%Y-%m-%d")
    conn.execute("""
        INSERT INTO costos_flete_recetas (receta_id, monto, fecha_desde)
        VALUES (?, ?, ?)
    """, (receta_id, nuevo_flete, hoy))
    conn.commit()
    get_flete_receta.clear()


# ── FUNCIONES DE DATOS (Caché inteligente) ────────────────────────────────────

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
        "costo_total_bd":    c_total,
        "cantidad":          cantidad,
        "moneda":            moneda,
        "cotizacion_bd":     float(r["cotizacion_usd"] or 1.0),
        "fecha":             str(r["fecha"]),
        "fuente":            "compra directa" if not nro else f"comprobante {nro}",
        "nro_comprobante":   nro,
    }

@st.cache_data(ttl=60)
def get_comprobante_crudo(nro_comprobante):
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
def get_overhead_detalle():
    df_g = query("""
        SELECT g.id, g.beneficiario_nombre as nombre, ci.nombre as categoria,
               g.importe_total, g.moneda
        FROM gastos g
        LEFT JOIN categorias_imputacion ci ON g.categoria_id = ci.id
        ORDER BY g.importe_total DESC
    """)
    df_e = query("SELECT id, nombre, sueldo_base FROM empleados ORDER BY nombre")
    return df_g, df_e

@st.cache_data(ttl=60)
def get_flete_receta(receta_id):
    df = query("""
        SELECT monto FROM costos_flete_recetas
        WHERE receta_id=? ORDER BY fecha_desde DESC LIMIT 1
    """, (receta_id,))
    return float(df.iloc[0]["monto"]) if not df.empty else 0.0

@st.cache_data(ttl=60)
def get_cotizacion_dolar():
    df = query("SELECT compra, venta, fecha_hora FROM cotizacion_dolar ORDER BY fecha_hora DESC LIMIT 1")
    if df.empty:
        return None, None, None
    return float(df.iloc[0]["compra"]), float(df.iloc[0]["venta"]), str(df.iloc[0]["fecha_hora"])

@st.cache_data(ttl=60)
def get_ingredientes_raw(receta_id):
    return query("""
        SELECT ri.materia_prima_id, mp.nombre, ri.cantidad, ri.unidad
        FROM receta_ingredientes ri
        JOIN materias_primas mp ON ri.materia_prima_id = mp.id
        WHERE ri.receta_id=?
        ORDER BY ri.cantidad DESC
    """, (receta_id,))


# ── GENERACIÓN DE REPORTE PDF (ReportLab) ──────────────────────────────────────

def generar_pdf_presupuesto(items, cliente_nombre, cotizacion, total_costo, total_venta, total_gan, margen):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#151820'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#656d80'),
        spaceAfter=15
    )
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=colors.HexColor('#151820'),
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#1c2030')
    )
    bold_body_style = ParagraphStyle(
        'BoldBodyStyle',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    # Encabezado
    story.append(Paragraph("Minerva · Reporte de Presupuesto", title_style))
    story.append(Paragraph(f"Cliente: {cliente_nombre}  |  Fecha: {date.today().strftime('%d/%m/%Y')}  |  USD Cotización: ${cotizacion:,.2f}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#252a3a'), spaceBefore=2, spaceAfter=12))
    
    # Tabla resumen
    story.append(Paragraph("Resumen Financiero", heading_style))
    summary_data = [
        [Paragraph("Indicador", bold_body_style), Paragraph("Monto", bold_body_style)],
        [Paragraph("Costo Total Acumulado", body_style), Paragraph(f"$ {total_costo:,.2f}", body_style)],
        [Paragraph("Venta Total Esperada", body_style), Paragraph(f"$ {total_venta:,.2f}", body_style)],
        [Paragraph("Utilidad Estimada", body_style), Paragraph(f"$ {total_gan:,.2f}", body_style)],
        [Paragraph("Margen sobre Venta", body_style), Paragraph(f"{margen:.1f}%", bold_body_style)]
    ]
    summary_table = Table(summary_data, colWidths=[10*cm, 7*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1c2030')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a0a8bc')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8f9fa')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    for col in range(2):
        summary_data[0][col].style.textColor = colors.white
    story.append(summary_table)
    story.append(Spacer(1, 10))
    
    # Tabla detalle
    story.append(Paragraph("Detalle de Items Simulados", heading_style))
    detail_data = [
        [
            Paragraph("Producto", bold_body_style), 
            Paragraph("Envase", bold_body_style), 
            Paragraph("Unids.", bold_body_style), 
            Paragraph("Costo Unit.", bold_body_style), 
            Paragraph("Venta Unit.", bold_body_style), 
            Paragraph("Costo Total", bold_body_style)
        ]
    ]
    for col in range(6):
        detail_data[0][col].style.textColor = colors.white

    for item in items:
        detail_data.append([
            Paragraph(item["producto"], body_style),
            Paragraph(item["envase"], body_style),
            Paragraph(str(item["unidades"]), body_style),
            Paragraph(f"$ {item['costo_unit']:,.2f}", body_style),
            Paragraph(f"$ {item['precio_venta']:,.2f}", body_style),
            Paragraph(f"$ {item['costo_total']:,.2f}", body_style)
        ])
        
    detail_table = Table(detail_data, colWidths=[4.5*cm, 3.5*cm, 1.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
    detail_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1c2030')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a0a8bc')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(detail_table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# ── CÁLCULOS QUE DEPENDEN DE LA COTIZACIÓN ─────────────────────────────────────

def convertir_a_ars(valor, moneda, cotizacion_usuario):
    if moneda == "USD":
        return valor * cotizacion_usuario
    return valor

def receta_valida(receta_id):
    if receta_id is None:
        return False
    s = str(receta_id).strip().lower()
    if s in ("", "none", "nan", "null"):
        return False
    try:
        int(float(s))
        return True
    except (ValueError, TypeError):
        return False

def calcular_precio_mp_ars(materia_prima_id, cotizacion_usuario):
    datos = get_compra_cruda_mp(materia_prima_id)
    if datos is None:
        return None, None, 0.0, None, "sin precio"

    fecha    = datos["fecha"]
    fuente   = datos["fuente"]
    nro      = datos["nro_comprobante"]
    amount_mp = datos.get("cantidad", 1.0)

    if datos["precio_usd"] is not None:
        precio_base_ars = datos["precio_usd"] * cotizacion_usuario
    else:
        precio_base_ars = datos["precio_ars_directo"] or 0.0

    costo_esta_ars = precio_base_ars * amount_mp

    if nro:
        df_comp = get_comprobante_crudo(nro)
        if not df_comp.empty:
            flete_total_ars = float(df_comp["costo_flete"].max() or 0)
            suma_ars = 0.0
            for _, r in df_comp.iterrows():
                mon_r = str(r["moneda"] or "ARS").strip().upper()
                pu_r  = float(r["precio_unitario"])
                qty_r = float(r["cantidad"])
                suma_ars += convertir_a_ars(pu_r, mon_r, cotizacion_usuario) * qty_r

            suma_ars       = suma_ars or 1.0
            proporcion     = costo_esta_ars / suma_ars
            flete_unit_ars = (flete_total_ars * proporcion) / amount_mp if amount_mp > 0 else 0
        else:
            flete_unit_ars = 0.0
    else:
        flete_unit_ars = float(datos.get("flete_raw", 0.0)) / amount_mp if amount_mp > 0 else 0

    return precio_base_ars + flete_unit_ars, precio_base_ars, flete_unit_ars, fecha, fuente

def get_ingredientes_con_precio(receta_id, cotizacion_usuario):
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

    # Normalizar a 1 litro (receta base = 200L)
    df["cantidad_por_litro"]     = df["cantidad"] / 200.0
    df["costo_mp_por_litro"]     = df["cantidad_por_litro"] * df["precio_base"].fillna(0)
    df["flete_por_litro"]        = df["cantidad_por_litro"] * df["flete_unitario"].fillna(0)
    df["costo_total_por_litro"]  = df["costo_mp_por_litro"] + df["flete_por_litro"]
    df["costo_linea"]            = df["cantidad"] * df["precio_unitario"].fillna(0)
    return df


# ── INICIALIZAR SESSION STATE (Cargando datos desde la BD) ─────────────────────
if "oh_gastos" not in st.session_state or "oh_empleados" not in st.session_state:
    _df_g, _df_e = get_overhead_detalle()
    _ajustes_bd = cargar_ajustes_overhead_bd()
    
    # Valores de Gastos
    gastos_dict = {}
    imputar_gasto_dict = {}
    for _, r in _df_g.iterrows():
        gid = int(r["id"])
        monto_origen = float(r["importe_total"])
        moneda = str(r["moneda"]).strip().upper()
        
        # Guardamos en pesos nativamente
        gastos_dict[gid] = {
            "monto": monto_origen,
            "moneda": moneda
        }
        imputar_gasto_dict[gid] = True

    # Aplicar persistencia de ajustes sobre los gastos si existe en BD
    for _, r_aj in _ajustes_bd[_ajustes_bd["tipo"] == "gasto"].iterrows():
        gid = int(r_aj["referencia_id"])
        if gid in gastos_dict:
            gastos_dict[gid]["monto"] = float(r_aj["valor_ajustado"])
            imputar_gasto_dict[gid] = bool(int(r_aj["imputar_costo"]))

    st.session_state.oh_gastos    = gastos_dict
    st.session_state.oh_imputados_g = imputar_gasto_dict
    st.session_state.oh_nombres_g = {int(r["id"]): str(r["nombre"]) for _, r in _df_g.iterrows()}
    st.session_state.oh_categ_g   = {int(r["id"]): str(r["categoria"] or "") for _, r in _df_g.iterrows()}

    # Valores de Empleados
    empleados_dict = {}
    imputar_empleado_dict = {}
    for _, r in _df_e.iterrows():
        eid = int(r["id"])
        empleados_dict[eid] = float(r["sueldo_base"])
        imputar_empleado_dict[eid] = True

    # Aplicar persistencia de ajustes sobre los empleados
    for _, r_aj in _ajustes_bd[_ajustes_bd["tipo"] == "empleado"].iterrows():
        eid = int(r_aj["referencia_id"])
        if eid in empleados_dict:
            empleados_dict[eid] = float(r_aj["valor_ajustado"])
            imputar_empleado_dict[eid] = bool(int(r_aj["imputar_costo"]))

    st.session_state.oh_empleados = empleados_dict
    st.session_state.oh_imputados_e = imputar_empleado_dict
    st.session_state.oh_nombres_e = {int(r["id"]): str(r["nombre"]) for _, r in _df_e.iterrows()}


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
        help="Se aplica a insumos, envases y gastos en USD."
    )
    if dolar_fecha_bd:
        st.markdown(
            f'<div style="font-size:0.82rem;color:var(--muted);margin-top:-0.3rem;margin-bottom:0.5rem;">'
            f'BD: compra ${dolar_compra_bd:,.0f} / venta ${dolar_venta_bd:,.0f}<br>'
            f'Actualizado: {dolar_fecha_bd[:10]}</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-header">Prorrateo / Capacidad</div>', unsafe_allow_html=True)
    capacidad_planta = st.number_input(
        "Capacidad planta teórica (L/mes)", min_value=1000, max_value=200000,
        value=32000, step=1000,
    )
    uso_planta_pct = st.slider(
        "Uso real de capacidad (%)", 
        min_value=10, max_value=100, value=100, step=5,
        help="Si la planta no opera al 100%, el costo unitario de overhead aumenta por capacidad ociosa."
    )
    
    st.markdown('<div class="section-header">Parámetros de Margen</div>', unsafe_allow_html=True)
    margen_objetivo = st.slider("Margen deseado (%)", min_value=0, max_value=200, value=30)
    precio_venta_manual = st.number_input(
        "Precio venta manual (ARS, 0 = BD)",
        min_value=0.0, value=0.0, step=100.0,
    )

    st.markdown('<div class="section-header">Opciones de visualización</div>', unsafe_allow_html=True)
    mostrar_grafico_ing      = st.checkbox("Gráfico ingredientes", value=True)


# ── PROCESAMIENTO DINÁMICO DE GASTOS Y SUELDOS (MULTIDIVISA Y CAPACIDAD REAL) ──
# Calcular los totales unificados convirtiendo gastos en USD a ARS en tiempo real
total_gastos_ars = 0.0
total_gastos_imputados_ars = 0.0

for gid, g_info in st.session_state.oh_gastos.items():
    monto_ars = convertir_a_ars(g_info["monto"], g_info["moneda"], cotizacion_dolar)
    total_gastos_ars += monto_ars
    if st.session_state.oh_imputados_g.get(gid, True):
         total_gastos_imputados_ars += monto_ars

total_sueldos_ars = sum(st.session_state.oh_empleados.values())
total_sueldos_imputados_ars = sum(
    sueldo for eid, sueldo in st.session_state.oh_empleados.items()
    if st.session_state.oh_imputados_e.get(eid, True)
)

total_overhead_ars = total_gastos_ars + total_sueldos_ars
total_overhead_imputado_ars = total_gastos_imputados_ars + total_sueldos_imputados_ars

# Driver de capacidad real
capacidad_real_litros = capacidad_planta * (uso_planta_pct / 100.0)
overhead_por_litro = total_overhead_imputado_ars / capacidad_real_litros if capacidad_real_litros > 0 else 0
overhead_por_unidad = overhead_por_litro * 1.0


# ── CÁLCULO DE PRODUCTO ────────────────────────────────────────────────────────
receta_id    = prod_row.get("id_receta")
envase_id    = prod_row.get("envase_id")
tipo_caja_id = prod_row.get("tipo_caja_id")
prod_id      = int(prod_row["id"])
cap_litros   = float(prod_row.get("capacidad_litros") or 1.0)
envase_desc  = prod_row.get("envase_desc") or "—"

# Insumos (Recalculado con cotización actual)
costo_insumos     = 0.0
ingred_df         = pd.DataFrame()
avisos_sin_precio = []
if receta_valida(receta_id):
    ingred_df = get_ingredientes_con_precio(int(receta_id), cotizacion_dolar)
    sin_p_df  = ingred_df[ingred_df["precio_unitario"].isna() | (ingred_df["precio_unitario"] == 0)]
    avisos_sin_precio = sin_p_df["nombre"].tolist()
    costo_insumos = ingred_df["costo_total_por_litro"].sum() * cap_litros
else:
    avisos_sin_precio = [f"Este producto no tiene receta asignada en la BD (id_receta={receta_id!r})"]

# Envase
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
    try:
        df_tc = query("SELECT costo_unitario FROM tipo_cajas WHERE id=?", (tipo_caja_id,))
        if not df_tc.empty and df_tc.iloc[0]["costo_unitario"]:
            _precio_caja = float(df_tc.iloc[0]["costo_unitario"])
            upc = int(caja_info["unidades_por_caja"]) if int(caja_info["unidades_por_caja"]) > 0 else 1
            costo_caja_por_unidad = _precio_caja / upc
    except Exception:
        pass

# Flete de receta
flete_receta_por_unidad = 0.0
if receta_valida(receta_id):
    flete_receta_por_unidad = get_flete_receta(int(receta_id)) * cap_litros / 200.0

# Totales finales de la simulación unitaria
costo_total = costo_insumos + costo_envase + costo_caja_por_unidad + (overhead_por_litro * cap_litros) + flete_receta_por_unidad
precio_bd, fecha_precio_bd = get_ultimo_precio_venta(cliente_id, prod_id, int(envase_id) if envase_id else 0)
precio_venta    = precio_venta_manual if precio_venta_manual > 0 else float(precio_bd or 0)
precio_sugerido = costo_total * (1 + margen_objetivo / 100) if costo_total > 0 else 0
ganancia_abs    = precio_venta - costo_total if precio_venta > 0 else 0
ganancia_pct    = (ganancia_abs / precio_venta * 100) if precio_venta > 0 else 0
markup_pct      = (ganancia_abs / costo_total * 100) if costo_total > 0 else 0


# ── AVISOS ────────────────────────────────────────────────────────────────────
for av in avisos_sin_precio[:3]:
    if "sin receta" in av.lower() or "receta asignada" in av.lower():
        st.markdown(f'<div class="info-box">ℹ {av} · Los insumos aparecen en $0.00</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="aviso">⚠ Insumo sin precio de compra: <b>{av}</b></div>', unsafe_allow_html=True)
if precio_venta == 0:
    st.markdown('<div class="info-box">ℹ Sin precio de venta registrado. Ingresá uno en el panel lateral para analizar la rentabilidad.</div>', unsafe_allow_html=True)


# ── TABS PRINCIPALES ──────────────────────────────────────────────────────────
tabs = st.tabs(["📊 Resumen", "🧪 Receta e Ingredientes", "🏭 Overhead y Prorrateo", "📋 Comparativa", "🧮 Simulador"])


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

        fila_costo("Insumos (Fórmula Receta)", costo_insumos, costo_total, "🧬")
        fila_costo("Envase", costo_envase, costo_total, "🫙")
        fila_costo("Caja / Embalaje", costo_caja_por_unidad, costo_total, "📦")
        fila_costo("Overhead Imputado (Gastos/Sueldos)", overhead_por_litro * cap_litros, costo_total, "🏭")
        fila_costo("Flete Prorrateado de Receta", flete_receta_por_unidad, costo_total, "🚛")

        st.markdown(f"""
        <div style="margin-top:0.8rem;padding:0.8rem 0;border-top:2px solid var(--accent);">
            <div class="costo-row" style="border:none;padding:0;">
                <span style="font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;">COSTO TOTAL UNITARIO ({cap_litros}L)</span>
                <span style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.2rem;color:var(--accent);">$ {costo_total:,.2f}</span>
            </div>
        </div>""", unsafe_allow_html=True)

        # Detalles del envase
        fecha_envase_html = (
            f"<div style='font-size:0.88rem;color:var(--muted);margin-top:0.4rem;'>"
            f"Último precio de compra: <b>USD {precio_envase_usd:,.3f}</b> = <b>ARS $ {costo_envase:,.2f}</b> ({fecha_envase})</div>"
            if fecha_envase else ""
        )
        st.markdown(f"""
        <div class="block-box" style="margin-top:1rem;">
            <div style="font-size:0.85rem;letter-spacing:2px;color:var(--muted);text-transform:uppercase;margin-bottom:0.5rem;">Envase / Presentación</div>
            <div style="font-size:1.05rem;">{envase_desc} &nbsp;·&nbsp; <span style="color:var(--muted);">{cap_litros} L/unidad</span></div>
            {fecha_envase_html}
        </div>""", unsafe_allow_html=True)

        # Capacidad de Planta e Impacto Ocioso
        impacto_ocio_ars = (total_overhead_imputado_ars / capacidad_real_litros - total_overhead_imputado_ars / capacidad_planta) * cap_litros if uso_planta_pct < 100 else 0
        st.markdown(f"""
        <div class="block-box">
            <div style="font-size:0.85rem;letter-spacing:2px;color:var(--muted);text-transform:uppercase;margin-bottom:0.5rem;">Capacidad y Driver ABC</div>
            <div style="font-size:1.05rem;">Uso de planta: <span style="color:var(--yellow);">{uso_planta_pct}%</span> de capacidad teórica</div>
            <div style="font-size:0.88rem;color:var(--muted);margin-top:0.3rem;">
                Capacidad real procesada: <b>{capacidad_real_litros:,.0f} L/mes</b> (Ociosidad: {(100-uso_planta_pct)}%)
                <br>Sobrecosto por ociosidad en esta unidad: <b style="color:var(--danger);">$ {impacto_ocio_ars:,.2f}</b>
            </div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">Precio de venta y rentabilidad</div>', unsafe_allow_html=True)

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
            <div class="metric-label">Ganancia neta por unidad</div>
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

        st.markdown('<div class="section-header" style="margin-top:1.4rem;">Precio sugerido óptimo</div>', unsafe_allow_html=True)
        diferencia = precio_sugerido - precio_venta
        dif_pct    = (diferencia / precio_venta * 100) if precio_venta > 0 else 0
        dif_color  = "var(--green)" if diferencia <= 0 else "var(--danger)"
        dif_signo  = "+" if diferencia > 0 else ""
        st.markdown(f"""
        <div class="block-box">
            <div style="font-size:0.85rem;letter-spacing:2px;color:var(--muted);text-transform:uppercase;margin-bottom:0.6rem;">
                Con {margen_objetivo}% de margen objetivo deseado
            </div>
            <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:var(--accent2);">
                $ {precio_sugerido:,.2f}
            </div>
            <div style="font-size:0.9rem;margin-top:0.5rem;color:{dif_color};">
                {dif_signo}$ {diferencia:,.2f} &nbsp;({dif_signo}{dif_pct:.1f}%) vs. precio actual de venta
            </div>
        </div>""", unsafe_allow_html=True)


# ══ TAB 2 — RECETA E INGREDIENTES (Con editor de receta integrado) ═══════════
with tabs[1]:
    if ingred_df.empty:
        st.markdown('<div class="aviso">Sin receta asignada a este producto en la base de datos.</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="info-box">Receta ID activa: <b>{receta_id}</b> · '
            f'Escala de formulación: 200 Litros de base → Rendimiento para {cap_litros} L ({cap_litros/200*100:.1f}%) · '
            f'Precios al dólar simulado $ {cotizacion_dolar:,.0f}</div>',
            unsafe_allow_html=True
        )

        col_rec_1, col_rec_2 = st.columns([1.3, 0.7], gap="large")

        with col_rec_1:
            st.markdown('<div class="section-header">Ingredientes actuales de la Receta</div>', unsafe_allow_html=True)
            
            c1, c2, c3, c4, c5 = st.columns([2.5, 1.2, 1.2, 1.2, 1.2])
            for col, h in zip([c1, c2, c3, c4, c5], ["Insumo", "Cant. Total (200L)", "$ MP/u", "Flete/u", "Costo Total/u"]):
                with col:
                    st.markdown(f'<div style="font-size:0.8rem;letter-spacing:1px;color:var(--muted);text-transform:uppercase;">{h}</div>', unsafe_allow_html=True)
            st.markdown('<hr style="border-color:var(--border);margin:0.4rem 0;">', unsafe_allow_html=True)

            for _, row in ingred_df.iterrows():
                sin_p = pd.isna(row["precio_unitario"]) or row["precio_unitario"] == 0
                
                # Todo escalado al volumen unitario
                costo_mp_u  = float(row.get("costo_mp_por_litro", 0)) * cap_litros
                flete_u     = float(row.get("flete_por_litro", 0)) * cap_litros
                costo_tot_u = float(row.get("costo_total_por_litro", 0)) * cap_litros

                c1, c2, c3, c4, c5 = st.columns([2.5, 1.2, 1.2, 1.2, 1.2])
                with c1:
                    tag = '<span class="tag-sin-precio">sin precio</span>' if sin_p else ""
                    st.markdown(f'<div style="font-size:0.92rem;padding:0.3rem 0;">{row["nombre"]} {tag}</div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div style="font-size:0.92rem;padding:0.3rem 0;color:var(--text);">{row["cantidad"]:,.3f} {row["unidad"]}</div>', unsafe_allow_html=True)
                with c3:
                    st.markdown(f'<div style="font-size:0.92rem;padding:0.3rem 0;color:var(--accent2);">$ {costo_mp_u:,.2f}</div>', unsafe_allow_html=True)
                with c4:
                    st.markdown(f'<div style="font-size:0.92rem;padding:0.3rem 0;color:var(--yellow);">$ {flete_u:,.2f}</div>', unsafe_allow_html=True)
                with c5:
                    cc = "var(--muted)" if sin_p else "var(--accent)"
                    st.markdown(f'<div style="font-size:0.92rem;padding:0.3rem 0;color:{cc}; font-weight:600;">$ {costo_tot_u:,.2f}</div>', unsafe_allow_html=True)

            st.markdown('<hr style="border-color:var(--border);margin:0.6rem 0;">', unsafe_allow_html=True)
            ct1, _, _, _, ct5 = st.columns([2.5, 1.2, 1.2, 1.2, 1.2])
            with ct1:
                st.markdown('<div style="font-family:Syne,sans-serif;font-weight:700;font-size:1.05rem;">TOTAL INSUMOS</div>', unsafe_allow_html=True)
            with ct5:
                st.markdown(f'<div style="font-family:Syne,sans-serif;font-weight:800;font-size:1.05rem;color:var(--accent);">$ {costo_insumos:,.2f}</div>', unsafe_allow_html=True)

            if mostrar_grafico_ing:
                df_chart = ingred_df.copy()
                df_chart["costo_escalado"] = df_chart["costo_total_por_litro"] * cap_litros
                df_chart = df_chart[df_chart["costo_escalado"] > 0].sort_values("costo_escalado", ascending=False)
                if not df_chart.empty:
                    st.bar_chart(df_chart.set_index("nombre")["costo_escalado"], color="#c8ff4e")

        with col_rec_2:
            st.markdown('<div class="section-header">✏️ Editor de Proporciones (DB)</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="info-box" style="font-size:0.85rem;">Modifica los valores '
                'de formulación base para el lote de 200L. Los cambios se guardarán '
                '<b>permanentemente</b> en la base de datos de Minerva.</div>',
                unsafe_allow_html=True
            )

            # Selector de ingrediente para editar
            ingredientes_opciones = {r["nombre"]: (int(r["materia_prima_id"]), float(r["cantidad"]), r["unidad"]) for _, r in ingred_df.iterrows()}
            ingrediente_a_editar_nombre = st.selectbox("Ingrediente a editar", list(ingredientes_opciones.keys()))
            
            if ingrediente_a_editar_nombre:
                mp_id_editar, cant_actual, unidad_editar = ingredientes_opciones[ingrediente_a_editar_nombre]
                
                st.markdown(f"**Unidad de medida:** `{unidad_editar}`")
                nueva_cantidad_receta = st.number_input(
                    f"Nueva cantidad en Receta (lote 200L)",
                    min_value=0.0,
                    value=cant_actual,
                    step=0.1,
                    format="%.4f"
                )
                
                if st.button("💾 Guardar cambio en Receta", use_container_width=True):
                    try:
                        actualizar_cantidad_ingrediente_bd(int(receta_id), mp_id_editar, nueva_cantidad_receta)
                        st.success(f"✓ {ingrediente_a_editar_nombre} actualizado a {nueva_cantidad_receta} {unidad_editar}")
                        st.cache_data.clear() # Limpiar toda la cache de datos
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")

            # ── SECCIÓN DE EDITOR DE ENVASE Y FLETE EN LA BASE DE DATOS ──────
            st.markdown('<div class="section-header" style="margin-top:2rem;">✏️ Editor de Envase y Flete (DB)</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="info-box" style="font-size:0.85rem;">Registra un nuevo precio de envase '
                'o el flete correspondiente a la receta de fabricación. Se guardará de manera permanente en el historial.</div>',
                unsafe_allow_html=True
            )

            if envase_id:
                nuevo_precio_envase_val = st.number_input(
                    f"Precio Unitario del Envase (USD) - {envase_desc}",
                    min_value=0.0,
                    value=float(precio_envase_usd),
                    step=0.01,
                    format="%.4f",
                    key="input_envase_usd"
                )
                if st.button("💾 Guardar Precio de Envase", use_container_width=True):
                    try:
                        insertar_precio_envase_bd(int(envase_id), nuevo_precio_envase_val)
                        st.success(f"✓ Envase actualizado a USD {nuevo_precio_envase_val:.4f} en la base de datos.")
                        st.cache_data.clear()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al registrar envase: {e}")
            else:
                st.warning("Este producto no tiene un envase activo asignado para editar.")

            if receta_valida(receta_id):
                flete_actual_receta = get_flete_receta(int(receta_id))
                nuevo_flete_val = st.number_input(
                    "Costo de Flete de la Receta (ARS total para lote 200L)",
                    min_value=0.0,
                    value=float(flete_actual_receta),
                    step=500.0,
                    format="%.2f",
                    key="input_flete_ars"
                )
                if st.button("💾 Guardar Flete de Receta", use_container_width=True):
                    try:
                        insertar_flete_receta_bd(int(receta_id), nuevo_flete_val)
                        st.success(f"✓ Flete de receta registrado a $ {nuevo_flete_val:,.2f} en la base de datos.")
                        st.cache_data.clear()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al registrar flete: {e}")
            else:
                st.warning("Este producto no posee una receta válida asignada para calcular fletes.")


# ══ TAB 3 — OVERHEAD Y PRORRATEO (Segmentado, multi-moneda y persistente) ══════
with tabs[2]:
    st.markdown(
        '<div class="info-box">✏️ Los ajustes de gastos y sueldos se guardan en la '
        'base de datos SQLite presionado el botón de guardar. Los gastos clasificados en USD '
        'son convertidos dinámicamente usando el tipo de cambio del panel lateral.</div>',
        unsafe_allow_html=True
    )

    col_ov1, col_ov2 = st.columns(2, gap="large")

    with col_ov1:
        st.markdown('<div class="section-header">Gastos operativos desglosados</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.82rem;color:var(--muted);margin-bottom:0.8rem;">Desmarca para omitir de la imputación unitaria de costos.</div>', unsafe_allow_html=True)
        
        cambio_g = False
        cambio_imp_g = False
        
        for gid, g_info in st.session_state.oh_gastos.items():
            nombre  = st.session_state.oh_nombres_g.get(gid, f"Gasto {gid}")
            categ   = st.session_state.oh_categ_g.get(gid, "")
            label_display   = f"{nombre}" + (f" ({categ})" if categ and categ != nombre else "")
            moneda  = g_info["moneda"]
            
            # Formatear el label con divisa
            label_final = f"{label_display} [{moneda}]"
            
            cg_col1, cg_col2 = st.columns([3, 1])
            with cg_col1:
                nuevo_monto = st.number_input(
                    label_final, min_value=0.0, value=g_info["monto"], step=1000.0,
                    format="%.0f", key=f"g_val_{gid}"
                )
                if nuevo_monto != g_info["monto"]:
                    st.session_state.oh_gastos[gid]["monto"] = nuevo_monto
                    cambio_g = True
            with cg_col2:
                st.markdown("<div style='height:1.7rem;'></div>", unsafe_allow_html=True)
                imp_estado = st.checkbox("Imputar CIF", value=st.session_state.oh_imputados_g.get(gid, True), key=f"g_chk_{gid}")
                if imp_estado != st.session_state.oh_imputados_g.get(gid, True):
                    st.session_state.oh_imputados_g[gid] = imp_estado
                    cambio_imp_g = True

        if cambio_g or cambio_imp_g:
            st.rerun()

        # Display del total convertido a ARS
        st.markdown(f"""
        <div style="margin-top:0.8rem;padding:0.8rem 0;border-top:2px solid var(--accent2);">
            <div class="costo-row" style="border:none;padding:0;">
                <span style="font-family:'Syne',sans-serif;font-weight:700;">TOTAL GASTOS (ARS)</span>
                <span style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.1rem;color:var(--accent2);">$ {total_gastos_ars:,.0f}</span>
            </div>
            <div class="costo-row" style="border:none;padding:0;font-size:0.85rem;color:var(--muted)">
                <span>Total Imputado al Costo Unitario (CIF)</span>
                <span>$ {total_gastos_imputados_ars:,.0f}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    with col_ov2:
        st.markdown('<div class="section-header">Sueldos de Personal</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.82rem;color:var(--muted);margin-bottom:0.8rem;">Permite asignar sueldos fijos o simular modificaciones de nómina.</div>', unsafe_allow_html=True)

        cambio_e = False
        cambio_imp_e = False
        
        for eid, sueldo in st.session_state.oh_empleados.items():
            nombre = st.session_state.oh_nombres_e.get(eid, f"Empleado {eid}")
            
            ce_col1, ce_col2 = st.columns([3, 1])
            with ce_col1:
                nuevo_sueldo = st.number_input(
                    nombre, min_value=0.0, value=sueldo, step=5000.0,
                    format="%.0f", key=f"e_val_{eid}"
                )
                if nuevo_sueldo != sueldo:
                    st.session_state.oh_empleados[eid] = nuevo_sueldo
                    cambio_e = True
            with ce_col2:
                st.markdown("<div style='height:1.7rem;'></div>", unsafe_allow_html=True)
                imp_sueldo_estado = st.checkbox("Imputar MOD", value=st.session_state.oh_imputados_e.get(eid, True), key=f"e_chk_{eid}")
                if imp_sueldo_estado != st.session_state.oh_imputados_e.get(eid, True):
                    st.session_state.oh_imputados_e[eid] = imp_sueldo_estado
                    cambio_imp_e = True

        if cambio_e or cambio_imp_e:
            st.rerun()

        st.markdown(f"""
        <div style="margin-top:0.8rem;padding:0.8rem 0;border-top:2px solid var(--yellow);">
            <div class="costo-row" style="border:none;padding:0;">
                <span style="font-family:'Syne',sans-serif;font-weight:700;">TOTAL SUELDOS (ARS)</span>
                <span style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.1rem;color:var(--yellow);">$ {total_sueldos_ars:,.0f}</span>
            </div>
            <div class="costo-row" style="border:none;padding:0;font-size:0.85rem;color:var(--muted)">
                <span>Total Imputado al Costo Unitario (MOD)</span>
                <span>$ {total_sueldos_imputados_ars:,.0f}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    # Botones de persistencia permanente
    st.markdown('<div class="section-header" style="margin-top:1rem;">Guardar Escenario de Costos en BD</div>', unsafe_allow_html=True)
    c_btn1, c_btn2, _ = st.columns([1.2, 1.2, 1.6])
    
    with c_btn1:
        if st.button("💾 Guardar escenario de costos", use_container_width=True):
            try:
                # Guardamos gastos
                for gid, g_info in st.session_state.oh_gastos.items():
                    imp_val = 1 if st.session_state.oh_imputados_g.get(gid, True) else 0
                    guardar_ajuste_overhead_bd("gasto", gid, g_info["monto"], imp_val)
                # Guardamos empleados
                for eid, sueldo in st.session_state.oh_empleados.items():
                    imp_val = 1 if st.session_state.oh_imputados_e.get(eid, True) else 0
                    guardar_ajuste_overhead_bd("empleado", eid, sueldo, imp_val)
                st.success("✓ ¡Escenario guardado en base de datos correctamente!")
            except Exception as e:
                st.error(f"Error al guardar escenario: {e}")
                
    with c_btn2:
        if st.button("↩ Reestablecer valores por defecto", use_container_width=True):
            try:
                eliminar_ajustes_overhead_bd()
                # Forzar recarga de session_state eliminando las llaves
                del st.session_state["oh_gastos"]
                del st.session_state["oh_empleados"]
                st.cache_data.clear()
                st.success("✓ Configuración de base de datos reestablecida.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al resetear: {e}")

    # Tarjetas informativas de Resumen del Tab Overhead
    st.markdown('<div class="section-header" style="margin-top:1.5rem;">Estructura final de Overhead prorrateado</div>', unsafe_allow_html=True)
    rc1, rc2, rc3, rc4 = st.columns(4)

    def oh_card(col, label, valor, color):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="padding:0.9rem 1rem;">
                <div class="metric-label">{label}</div>
                <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.3rem;color:{color};">$ {valor:,.0f}</div>
            </div>""", unsafe_allow_html=True)

    oh_card(rc1, "Gastos de Operación (Total)", total_gastos_ars, "var(--accent2)")
    oh_card(rc2, "Nómina Salarial (Total)", total_sueldos_ars, "var(--yellow)")
    oh_card(rc3, "OVERHEAD GLOBAL (CIF+MOD)", total_overhead_imputado_ars, "var(--accent)")
    with rc4:
        st.markdown(f"""
        <div class="metric-card" style="padding:0.9rem 1rem;">
            <div class="metric-label">Overhead Unitario Real</div>
            <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.1rem;color:var(--accent);">
                $ {overhead_por_litro:,.2f} / L
            </div>
            <div style="font-size:0.88rem;color:var(--muted);margin-top:0.3rem;">
                Eficiencia: {uso_planta_pct}% de planta
            </div>
        </div>""", unsafe_allow_html=True)


# ══ TAB 4 — COMPARATIVA ══════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header">Todos los productos del cliente</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="info-box">Precios calculados al dólar $ {cotizacion_dolar:,.0f} · '
        f'Flete prorrateado por receta · Overhead prorrateado según volumen ({uso_planta_pct}% de planta)</div>',
        unsafe_allow_html=True
    )

    rows_comp = []
    for _, prod in productos_df.iterrows():
        p_id  = int(prod["id"])
        p_rec = prod.get("id_receta")
        p_env = prod.get("envase_id")
        p_cap = float(prod.get("capacidad_litros") or 1.0)

        ci = 0.0
        if receta_valida(p_rec):
            try:
                idf = get_ingredientes_con_precio(int(p_rec), cotizacion_dolar)
                ci  = idf["costo_total_por_litro"].sum() * p_cap
            except Exception:
                ci = 0.0

        ce = 0.0
        if p_env:
            try:
                pe, _ = get_ultimo_precio_envase(int(p_env))
                ce    = float(pe or 0) * cotizacion_dolar
            except Exception:
                ce = 0.0

        oh = overhead_por_litro * p_cap

        fl = 0.0
        if receta_valida(p_rec):
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
        st.markdown('<div class="section-header" style="margin-top:1.5rem;">Comparativa de Margen neto</div>', unsafe_allow_html=True)
        st.bar_chart(df_comp.set_index("Producto")["Margen %"], color="#4ef0ff")
    else:
        st.markdown('<div class="aviso">No hay productos con precio de venta registrado para este cliente.</div>', unsafe_allow_html=True)


# ══ TAB 5 — SIMULADOR DE PRESUPUESTO ════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header">Simulador multi-producto</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="info-box">Armá un presupuesto combinando varios productos y cantidades. '
        'Los costos y el overhead se ajustan según la cotización del dólar y el uso de planta del panel lateral.</div>',
        unsafe_allow_html=True
    )

    if "presupuesto_items" not in st.session_state:
        st.session_state.presupuesto_items = []

    col_ag1, col_ag2, col_ag3 = st.columns([3, 1, 1])
    with col_ag1:
        prod_sim = st.selectbox("Producto a agregar", list(prod_opciones.keys()), key="sim_prod")
    with col_ag2:
        cant_sim = st.number_input("Unidades", min_value=1, value=100, step=10, key="sim_cant")
    with col_ag3:
        st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)
        if st.button("➕ Agregar al presupuesto"):
            row_s      = prod_opciones[prod_sim]
            p_id_s     = int(row_s["id"])
            p_rec_s    = row_s.get("id_receta")
            p_env_s    = row_s.get("envase_id")
            p_cap_s    = float(row_s.get("capacidad_litros") or 1.0)
            p_env_desc = row_s.get("envase_desc") or "—"

            ci_s = 0.0
            if receta_valida(p_rec_s):
                try:
                    idf_s = get_ingredientes_con_precio(int(p_rec_s), cotizacion_dolar)
                    ci_s  = idf_s["costo_total_por_litro"].sum() * p_cap_s
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
            if receta_valida(p_rec_s):
                try:
                    fl_s = get_flete_receta(int(p_rec_s)) * p_cap_s / 200.0
                except Exception:
                    fl_s = 0.0

            # Asignación del overhead imputable al simular
            costo_u_s = ci_s + ce_s + (overhead_por_litro * p_cap_s) + fl_s
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

    if st.session_state.presupuesto_items:
        st.markdown('<div class="section-header">Detalle del Presupuesto</div>', unsafe_allow_html=True)

        items = st.session_state.presupuesto_items
        df_pres = pd.DataFrame(items)

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
                st.markdown(f'<div style="font-size:0.88rem;padding:0.5rem 0;color:var(--muted);">Costo: <b style="color:var(--text);">$ {item["costo_unit"]:,.2f}</b></div>', unsafe_allow_html=True)
            with c4:
                gan_item = item["precio_venta"] - item["costo_unit"]
                color_gi = "var(--green)" if gan_item > 0 else "var(--danger)"
                st.markdown(f'<div style="font-size:0.88rem;padding:0.5rem 0;">Gan: <b style="color:{color_gi};">$ {gan_item:,.2f}</b></div>', unsafe_allow_html=True)
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

        st.markdown('<hr style="border-color:var(--border);margin:0.8rem 0;">', unsafe_allow_html=True)

        total_costo_pres  = sum(i["costo_total"] for i in items)
        total_venta_pres  = sum(i["venta_total"] for i in items)
        total_gan_pres    = total_venta_pres - total_costo_pres
        margen_pres       = (total_gan_pres / total_venta_pres * 100) if total_venta_pres > 0 else 0
        total_unidades    = sum(i["unidades"] for i in items)

        mc1, mc2, mc3, mc4 = st.columns(4)
        metric_sim(mc1, f"Costo total ({total_unidades} u)", total_costo_pres, "var(--accent2)")
        metric_sim(mc2, "Venta total esperada", total_venta_pres, "var(--text)")
        metric_sim(mc3, "Ganancia acumulada", total_gan_pres, "var(--green)" if total_gan_pres > 0 else "var(--danger)")

        with mc4:
            st.markdown(f"""
            <div class="metric-card" style="padding:0.9rem 1rem;">
                <div class="metric-label">Margen del presupuesto</div>
                <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.4rem;color:var(--yellow);">{margen_pres:.1f}%</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:1rem;">Análisis y Optimización del Presupuesto</div>', unsafe_allow_html=True)

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
                <div style="font-size:0.85rem;color:var(--muted);margin-bottom:0.4rem;">Precio de venta sugerido ({margen_pres_obj}% margen)</div>
                <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:var(--accent2);">$ {precio_presup_sugerido:,.2f}</div>
                <div style="font-size:0.88rem;margin-top:0.3rem;color:{dif_color_p};">{dif_signo_p}$ {diferencia_presup:,.2f} vs. base de datos</div>
            </div>""", unsafe_allow_html=True)

        with col_adj2:
            st.markdown('<div style="font-size:0.85rem;color:var(--muted);margin-bottom:0.6rem;">Representatividad de costos en el presupuesto</div>', unsafe_allow_html=True)
            for item in items:
                pct_item = (item["costo_total"] / total_costo_pres * 100) if total_costo_pres > 0 else 0
                st.markdown(f"""
                <div class="costo-row" style="font-size:0.88rem;">
                    <span style="color:var(--text);">{item['producto'][:30]} (x{item['unidades']})</span>
                    <span><span style="color:var(--accent);">$ {item['costo_total']:,.0f}</span>
                    <span style="color:var(--muted);margin-left:0.4rem;">{pct_item:.0f}%</span></span>
                </div>""", unsafe_allow_html=True)

        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            if st.button("🗑 Limpiar simulación"):
                st.session_state.presupuesto_items = []
                st.rerun()
        with btn_col2:
            if st.button("📄 Generar reporte en PDF"):
                pdf_bytes = generar_pdf_presupuesto(
                    items=items,
                    cliente_nombre=cliente_sel,
                    cotizacion=cotizacion_dolar,
                    total_costo=total_costo_pres,
                    total_venta=total_venta_pres,
                    total_gan=total_gan_pres,
                    margen=margen_pres,
                )
                nombre_archivo = f"presupuesto_{cliente_sel.replace(' ','_')}_{date.today().strftime('%Y%m%d')}.pdf"
                st.download_button(
                    label="⬇️ Descargar PDF",
                    data=pdf_bytes,
                    file_name=nombre_archivo,
                    mime="application/pdf",
                    key="dl_pdf"
                )

    else:
        st.markdown("""
        <div class="block-box" style="text-align:center;padding:2rem;">
            <div style="font-size:2rem;margin-bottom:0.5rem;">📋</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.1rem;color:var(--muted);">
                Seleccioná productos en la sección superior para calcular el presupuesto
            </div>
        </div>""", unsafe_allow_html=True)


# ── UTILIDADES DE MÉTRICAS SIMULADOR ───────────────────────────────────────────
def metric_sim(col, label, valor, color="var(--accent)"):
    with col:
        st.markdown(f"""
        <div class="metric-card" style="padding:0.9rem 1rem;">
            <div class="metric-label">{label}</div>
            <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.4rem;color:{color};">$ {valor:,.2f}</div>
        </div>""", unsafe_allow_html=True)