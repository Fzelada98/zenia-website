"""
Genera el xlsx demo COMPLETO para grabar el Loom.
- 5 pestañas: Portada, Dashboard, Transacciones, Cashflow, Deudas
- 15 transacciones demo con variedad de categorias
- 2 prestamos demo, 1 cisterna rotativa demo
- 3 buckets de efectivo calculados con formulas
- Match con la captura Zelle fake (Maria Gonzalez $500)
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

DARK_BG = "0F172A"
GOLD = "D4B88C"
GOLD_DARK = "8B6914"
GOLD_LIGHT = "F5ECD7"
INPUT_COLOR = "2563EB"
LINK_COLOR = "059669"
WHITE = "FFFFFF"
TEXT_PRIMARY = "1A1A1A"
TEXT_MUTED = "94A3B8"
GREEN_BG = "DCFCE7"
GREEN_TEXT = "166534"
RED_BG = "FEE2E2"
RED_TEXT = "991B1B"
BLUE_BG = "DBEAFE"

wb = Workbook()
thin = Side(border_style="thin", color="E2E8F0")
border = Border(left=thin, right=thin, top=thin, bottom=thin)


def fill(color):
    return PatternFill("solid", fgColor=color)


# === PORTADA ===
ws = wb.active
ws.title = "Portada"
ws.sheet_view.showGridLines = False

ws['B2'] = "GOLDEN OIL DEMO  ·  Repositorio Zelle"
ws['B2'].font = Font(size=22, bold=True, color=GOLD)
ws['B2'].fill = fill(DARK_BG)
ws.merge_cells('B2:I2')
ws['B2'].alignment = Alignment(horizontal='left', vertical='center')
ws.row_dimensions[2].height = 50

ws['B3'] = "Demo creado por ZENIA  ·  zeniapartners.com  ·  Datos ficticios"
ws['B3'].font = Font(size=11, italic=True, color="64748B")
ws.merge_cells('B3:I3')

# Saldo inicial banco
ws['B5'] = "SALDO INICIAL BANCO (editable):"
ws['B5'].font = Font(size=11, italic=True, color="64748B")
ws.merge_cells('B5:D5')
ws['B5'].alignment = Alignment(horizontal='right')
ws['E5'] = 35000
ws['E5'].font = Font(size=11, bold=True, color=INPUT_COLOR)
ws['E5'].fill = fill(BLUE_BG)
ws['E5'].number_format = '"$"#,##0.00'

# Trazabilidad header
ws['B7'] = "TRAZABILIDAD DEL EFECTIVO"
ws['B7'].font = Font(size=14, bold=True, color=GOLD)
ws['B7'].fill = fill(DARK_BG)
ws.merge_cells('B7:I7')
ws['B7'].alignment = Alignment(horizontal='left', vertical='center')
ws.row_dimensions[7].height = 32

# 4 cards horizontales (rows 9-11)
cards = [
    ('B', 'C', 'EFECTIVO EN BANCO',
     '=E5+SUMIFS(Transacciones!D:D,Transacciones!E:E,"in")-SUMIFS(Transacciones!D:D,Transacciones!E:E,"out")-(SUMIFS(Transacciones!D:D,Transacciones!F:F,"entrega_gandola")-SUMIFS(Transacciones!D:D,Transacciones!F:F,"retorno_gandola"))-(SUMIFS(Transacciones!D:D,Transacciones!F:F,"venta_credito")-SUMIFS(Transacciones!D:D,Transacciones!F:F,"cobro_credito"))',
     'Saldo liquido', BLUE_BG),
    ('D', 'E', 'DINERO EN GANDOLAS',
     '=SUMIFS(Transacciones!D:D,Transacciones!F:F,"entrega_gandola")-SUMIFS(Transacciones!D:D,Transacciones!F:F,"retorno_gandola")',
     'Capital en transito', "FEF3C7"),
    ('F', 'G', 'CUENTAS POR COBRAR',
     '=SUMIFS(Transacciones!D:D,Transacciones!F:F,"venta_credito")-SUMIFS(Transacciones!D:D,Transacciones!F:F,"cobro_credito")+IFERROR(Deudas!I35,0)',
     'Pendiente de cobrar', "FED7AA"),
    ('H', 'I', 'TOTAL TRAZADO', '=C10+E10+G10', 'Suma de los 3', GREEN_BG),
]
for c_left, c_right, label, formula, sub, bg in cards:
    rng = f"{c_left}9:{c_right}9"
    ws.merge_cells(rng)
    ws[f"{c_left}9"] = label
    ws[f"{c_left}9"].font = Font(size=10, bold=True, color=DARK_BG)
    ws[f"{c_left}9"].fill = fill(bg)
    ws[f"{c_left}9"].alignment = Alignment(horizontal='center', vertical='center')

    rng2 = f"{c_left}10:{c_right}10"
    ws.merge_cells(rng2)
    ws[f"{c_left}10"] = formula
    ws[f"{c_left}10"].font = Font(size=20, bold=True, color=INPUT_COLOR)
    ws[f"{c_left}10"].fill = fill(bg)
    ws[f"{c_left}10"].alignment = Alignment(horizontal='center', vertical='center')
    ws[f"{c_left}10"].number_format = '"$"#,##0.00'

    rng3 = f"{c_left}11:{c_right}11"
    ws.merge_cells(rng3)
    ws[f"{c_left}11"] = sub
    ws[f"{c_left}11"].font = Font(size=9, italic=True, color="64748B")
    ws[f"{c_left}11"].fill = fill(bg)
    ws[f"{c_left}11"].alignment = Alignment(horizontal='center')

ws.row_dimensions[9].height = 22
ws.row_dimensions[10].height = 60
ws.row_dimensions[11].height = 18

# KPIs DEL PERIODO
ws['B13'] = "KPIs DEL PERIODO"
ws['B13'].font = Font(size=14, bold=True, color=GOLD)
ws['B13'].fill = fill(DARK_BG)
ws.merge_cells('B13:I13')
ws['B13'].alignment = Alignment(horizontal='left', vertical='center')
ws.row_dimensions[13].height = 32

kpi_cards = [
    ('B', 'C', 'INGRESOS COBRADOS', '=SUMIFS(Transacciones!D:D,Transacciones!E:E,"in")', 'Total in', GREEN_BG),
    ('D', 'E', 'GASTOS PAGADOS', '=SUMIFS(Transacciones!D:D,Transacciones!E:E,"out")', 'Total out', RED_BG),
    ('F', 'G', 'FLUJO NETO', '=C16-E16', 'Cashflow del periodo', GOLD_LIGHT),
    ('H', 'I', 'TICKET PROMEDIO', '=IFERROR(C16/COUNTIFS(Transacciones!E:E,"in"),0)', 'Por transferencia', BLUE_BG),
]
for c_left, c_right, label, formula, sub, bg in kpi_cards:
    rng = f"{c_left}15:{c_right}15"
    ws.merge_cells(rng)
    ws[f"{c_left}15"] = label
    ws[f"{c_left}15"].font = Font(size=10, bold=True, color=DARK_BG)
    ws[f"{c_left}15"].fill = fill(bg)
    ws[f"{c_left}15"].alignment = Alignment(horizontal='center', vertical='center')

    rng2 = f"{c_left}16:{c_right}16"
    ws.merge_cells(rng2)
    ws[f"{c_left}16"] = formula
    ws[f"{c_left}16"].font = Font(size=20, bold=True, color=LINK_COLOR)
    ws[f"{c_left}16"].fill = fill(bg)
    ws[f"{c_left}16"].alignment = Alignment(horizontal='center', vertical='center')
    ws[f"{c_left}16"].number_format = '"$"#,##0.00'

    rng3 = f"{c_left}17:{c_right}17"
    ws.merge_cells(rng3)
    ws[f"{c_left}17"] = sub
    ws[f"{c_left}17"].font = Font(size=9, italic=True, color="64748B")
    ws[f"{c_left}17"].fill = fill(bg)
    ws[f"{c_left}17"].alignment = Alignment(horizontal='center')

ws.row_dimensions[15].height = 22
ws.row_dimensions[16].height = 60
ws.row_dimensions[17].height = 18

# Top 5 Pagadores (mini)
ws['B20'] = "TOP 5 PAGADORES"
ws['B20'].font = Font(size=12, bold=True, color=GOLD)
ws['B20'].fill = fill(DARK_BG)
ws.merge_cells('B20:I20')
ws['B20'].alignment = Alignment(horizontal='left', vertical='center')

ws['B21'] = "Cliente"
ws['D21'] = "Total Cobrado"
ws['F21'] = "# Pagos"
for cell in ['B21', 'D21', 'F21']:
    ws[cell].font = Font(size=10, bold=True, color=DARK_BG)
    ws[cell].fill = fill(GOLD_LIGHT)
    ws[cell].alignment = Alignment(horizontal='center')

# Top 5 hardcoded based on demo data
top_clients = [
    ("Maria Gonzalez", 500.00, 1),
    ("Carlos Perez", 1200.00, 2),
    ("Empresa XYZ", 850.00, 1),
    ("Lucia Ramirez", 650.00, 1),
    ("Pedro Lopez", 400.00, 1),
]
for i, (name, total, count) in enumerate(top_clients, 22):
    ws.cell(row=i, column=2, value=name).font = Font(size=10, bold=True, color=TEXT_PRIMARY)
    ws.cell(row=i, column=4, value=total).font = Font(size=11, bold=True, color=GREEN_TEXT)
    ws.cell(row=i, column=4).number_format = '"$"#,##0.00'
    ws.cell(row=i, column=4).alignment = Alignment(horizontal='right')
    ws.cell(row=i, column=6, value=count).font = Font(size=10, color=TEXT_PRIMARY)
    ws.cell(row=i, column=6).alignment = Alignment(horizontal='center')

for col, w in zip(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
                  [3, 22, 18, 22, 18, 22, 18, 22, 22]):
    ws.column_dimensions[col].width = w

# === TRANSACCIONES (15 rows demo) ===
ws2 = wb.create_sheet("Transacciones")
ws2.sheet_view.showGridLines = False

headers = ["ID", "Fecha", "Nombre", "Monto", "Direccion", "Categoria", "Conf#", "Estado", "Notas"]
for i, h in enumerate(headers, 1):
    c = ws2.cell(row=1, column=i, value=h)
    c.font = Font(bold=True, color=GOLD, size=11)
    c.fill = fill(DARK_BG)
    c.alignment = Alignment(horizontal='center', vertical='center')
    c.border = border
ws2.row_dimensions[1].height = 32

# 15 transacciones demo - LA PRIMERA es "Maria Gonzalez $500" para matchear captura
demo_txs = [
    # FILA MAGIC: la que aparece "nueva" en el video, debe coincidir con captura
    ("D-001", "2026-05-04", "Maria Gonzalez", 500.00, "in", "cobro_cliente", "ABC123XYZ", "completed", "Pago anticipo orden #1247"),
    ("D-002", "2026-05-03", "Carlos Perez", 700.00, "in", "cobro_cliente", "XYZ789DEF", "completed", "Pago final pedido"),
    ("D-003", "2026-05-03", "Empresa XYZ", 850.00, "in", "cobro_cliente", "QWE456RTY", "completed", "Pago factura mayo"),
    ("D-004", "2026-05-02", "Carlos Perez", 500.00, "in", "cobro_cliente", "MNB789POI", "completed", "Anticipo pedido grande"),
    ("D-005", "2026-05-02", "Lucia Ramirez", 650.00, "in", "cobro_cliente", "ZXC123ASD", "completed", "Pago semanal"),
    ("D-006", "2026-05-01", "Gandola Beleva", 5000.00, "out", "entrega_gandola", "", "completed", "Capital viaje Caracas"),
    ("D-007", "2026-05-01", "Pedro Lopez", 400.00, "in", "cobro_cliente", "WER567TYU", "completed", "Pago"),
    ("D-008", "2026-04-30", "Juan Rodriguez", 800.00, "out", "venta_credito", "", "completed", "Mercancia paga el 15 de mayo"),
    ("D-009", "2026-04-30", "Planilla Equipo", 2500.00, "out", "planilla", "", "completed", "Quincena fin abril"),
    ("D-010", "2026-04-29", "Aduana DAE", 1350.00, "out", "impuesto_gandola", "", "completed", "Permiso ingreso Venezuela"),
    ("D-011", "2026-04-28", "Luis Mendoza", 1600.00, "out", "pago_deuda_interes", "", "completed", "Interes mensual abril"),
    ("D-012", "2026-04-28", "Pedro Ramos", 2500.00, "out", "pago_deuda_interes", "", "completed", "Interes mensual abril"),
    ("D-013", "2026-04-27", "Logistica Andes", 2800.00, "out", "gasto_logistica", "", "completed", "Flete contenedor"),
    ("D-014", "2026-04-26", "Gandola Beleva", 4200.00, "in", "retorno_gandola", "", "completed", "Cierre viaje Caracas - efectivo"),
    ("D-015", "2026-04-25", "Viaticos chofer", 320.00, "out", "viaticos", "", "completed", "Comida + peajes Caracas"),
]
for i, row_data in enumerate(demo_txs, 2):
    for j, val in enumerate(row_data, 1):
        c = ws2.cell(row=i, column=j, value=val)
        c.font = Font(size=10, color=TEXT_PRIMARY)
        c.border = border
        if j == 4:
            c.font = Font(size=10, bold=True, color=INPUT_COLOR)
            c.number_format = '"$"#,##0.00'
            c.alignment = Alignment(horizontal='right')
        elif j == 5:
            c.font = Font(size=10, bold=True, color=GREEN_TEXT if val == "in" else RED_TEXT)
            c.alignment = Alignment(horizontal='center')

widths = [10, 12, 22, 12, 11, 22, 14, 12, 32]
for i, w in enumerate(widths, 1):
    ws2.column_dimensions[get_column_letter(i)].width = w

# === DEUDAS ===
ws3 = wb.create_sheet("Deudas")
ws3.sheet_view.showGridLines = False

ws3['A1'] = "DEUDAS  ·  Por cobrar / Por pagar"
ws3['A1'].font = Font(size=14, bold=True, color=GOLD)
ws3['A1'].fill = fill(DARK_BG)
ws3.merge_cells('A1:N1')
ws3['A1'].alignment = Alignment(horizontal='left', vertical='center')
ws3.row_dimensions[1].height = 32

deudas_headers = [
    "Deudor / Acreedor", "Tipo", "Capital Original", "Fecha Inicio",
    "Tasa Mensual %", "Meses Transc.", "Interes Mensual Fijo", "Pagos a Capital",
    "Saldo Vivo", "Fecha Vcto.", "Dias p/Vcto.", "Forma de Pago",
    "Status", "Notas"
]
for i, h in enumerate(deudas_headers, 1):
    c = ws3.cell(row=3, column=i, value=h)
    c.font = Font(bold=True, color=DARK_BG, size=10)
    c.fill = fill(GOLD_LIGHT)
    c.alignment = Alignment(horizontal='center', vertical='center')
ws3.row_dimensions[3].height = 26

# 2 deudas demo (Luis y Pedro)
deudas_data = [
    ("Luis Mendoza", "Por Pagar", 40000, "2025-12-15", 4, 4, 1600, 0, 40000, "", "", "Transferencia mensual", "Sin vcto.",
     "Prestamo dic 2025. Capital $40,000. Interes 4% mensual fijo $1,600. Solo se pagan intereses; capital intacto."),
    ("Pedro Ramos", "Por Pagar", 50000, "2025-12-15", 5, 4, 2500, 0, 50000, "", "", "Transferencia mensual", "Sin vcto.",
     "Prestamo dic 2025. Capital $50,000. Interes 5% mensual fijo $2,500. Solo se pagan intereses; capital intacto."),
]
for i, row_data in enumerate(deudas_data, 4):
    for j, val in enumerate(row_data, 1):
        c = ws3.cell(row=i, column=j, value=val)
        c.font = Font(size=10, color=TEXT_PRIMARY)
        if j == 3 or j == 7 or j == 8 or j == 9:
            c.font = Font(size=10, bold=True, color=INPUT_COLOR if j == 3 else LINK_COLOR if j in [7, 8] else TEXT_PRIMARY)
            c.number_format = '"$"#,##0.00'
            c.alignment = Alignment(horizontal='right')
        elif j == 5:
            c.number_format = '0.00\\%'
            c.alignment = Alignment(horizontal='center')

# Totales
ws3.cell(row=10, column=1, value="TOTAL POR PAGAR").font = Font(bold=True, color=DARK_BG)
ws3.cell(row=10, column=1).fill = fill(GOLD_LIGHT)
ws3.cell(row=10, column=3, value=90000).font = Font(bold=True, size=11, color=INPUT_COLOR)
ws3.cell(row=10, column=3).number_format = '"$"#,##0.00'
ws3.cell(row=10, column=7, value=4100).font = Font(bold=True, size=11, color=LINK_COLOR)
ws3.cell(row=10, column=7).number_format = '"$"#,##0.00'
ws3.cell(row=10, column=9, value=90000).font = Font(bold=True, size=11)
ws3.cell(row=10, column=9).number_format = '"$"#,##0.00'

# Sub-seccion CREDITO ROTATIVO
ws3.cell(row=14, column=1, value="CREDITO ROTATIVO PROVEEDOR").font = Font(size=12, bold=True, color=GOLD)
ws3.cell(row=14, column=1).fill = fill(DARK_BG)
ws3.merge_cells('A14:E14')

ws3.cell(row=15, column=1, value="Proveedor").font = Font(bold=True, color=DARK_BG, size=10)
ws3.cell(row=15, column=2, value="Cisterna Pendiente").font = Font(bold=True, color=DARK_BG, size=10)
ws3.cell(row=15, column=3, value="Monto").font = Font(bold=True, color=DARK_BG, size=10)
ws3.cell(row=15, column=4, value="Fecha Entrega").font = Font(bold=True, color=DARK_BG, size=10)
for col in [1, 2, 3, 4]:
    ws3.cell(row=15, column=col).fill = fill(GOLD_LIGHT)
    ws3.cell(row=15, column=col).alignment = Alignment(horizontal='center')

ws3.cell(row=16, column=1, value="Royal Caribena").font = Font(size=10, bold=True, color=INPUT_COLOR)
ws3.cell(row=16, column=2, value="Cisterna 15 (BS150)").font = Font(size=10, color=INPUT_COLOR)
ws3.cell(row=16, column=3, value=65637.82).font = Font(size=10, bold=True, color=INPUT_COLOR)
ws3.cell(row=16, column=3).number_format = '"$"#,##0.00'
ws3.cell(row=16, column=4, value="2026-04-15").font = Font(size=10, color=INPUT_COLOR)

ws3_widths = [22, 14, 14, 12, 14, 14, 18, 16, 16, 12, 12, 18, 14, 35]
for i, w in enumerate(ws3_widths, 1):
    ws3.column_dimensions[get_column_letter(i)].width = w

# === KPIs Tab ===
ws4 = wb.create_sheet("KPIs")
ws4.sheet_view.showGridLines = False
ws4['B2'] = "KPIs (referencia)"
ws4['B2'].font = Font(size=16, bold=True, color=DARK_BG)

kpi_list = [
    ("Total Ingresos", '=SUMIFS(Transacciones!D:D,Transacciones!E:E,"in")', "money"),
    ("Total Gastos", '=SUMIFS(Transacciones!D:D,Transacciones!E:E,"out")', "money"),
    ("Flujo Neto", '=C5-C6', "money"),
    ("# Cobros", '=COUNTIFS(Transacciones!E:E,"in")', "count"),
    ("# Pagos", '=COUNTIFS(Transacciones!E:E,"out")', "count"),
    ("Banco (calculado)", '=Portada!C10', "money"),
    ("Gandolas (calculado)", '=Portada!E10', "money"),
    ("Por Cobrar (calculado)", '=Portada!G10', "money"),
]
for i, (label, formula, fmt) in enumerate(kpi_list, 5):
    ws4.cell(row=i, column=2, value=label).font = Font(size=11, color=TEXT_PRIMARY)
    c = ws4.cell(row=i, column=3, value=formula)
    c.font = Font(size=12, bold=True, color=INPUT_COLOR)
    c.number_format = '#,##0' if fmt == "count" else '"$"#,##0.00'

ws4.column_dimensions['B'].width = 32
ws4.column_dimensions['C'].width = 22

import os
output_path = os.path.join("posts", "demo-sheet-for-loom.xlsx")
wb.save(output_path)
print("Saved:", output_path)
print("Size:", os.path.getsize(output_path), "bytes")
