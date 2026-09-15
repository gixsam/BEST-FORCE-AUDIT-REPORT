import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def generate_financial_flow_xlsx():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Financial Flow Master"
    
    # Enable Page Setup for A4 formatting
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
    # Fit to 1 page wide, unlimited pages tall
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.views.sheetView[0].showGridLines = False

    # Premium Corporate Palettes
    NAVY = "0F172A"        # Slate 900
    NAVY_LIGHT = "1E293B"  # Slate 800
    COL_BILL = "334155"    # Slate 700
    COL_COMM = "0369A1"    # Sky 700
    COL_CO = "166534"      # Green 800
    COL_BANK = "B45309"    # Amber 700
    WHITE = "FFFFFF"
    
    RED_FILL = "FEF2F2"
    RED_TXT = "991B1B"
    WARN_FILL = "FFFBEB"
    WARN_TXT = "92400E"
    GREEN_FILL = "F0FDF4"
    GREEN_TXT = "166534"
    ZEBRA = "F8FAFC"       # Slate 50

    thin = Side(border_style="thin", color="CBD5E1")
    thick = Side(border_style="medium", color="0F172A")
    
    cell_b = Border(left=thin, right=thin, top=thin, bottom=thin)
    head_b = Border(left=thin, right=thin, top=thick, bottom=thick)
    tot_b = Border(left=thin, right=thin, top=thick, bottom=thick)
    
    # Special Border Rule: Top, Left, Right ONLY (No Bottom)
    b_no_bottom = Border(left=thin, right=thin, top=thin, bottom=Side(border_style=None))
    b_last_row = Border(left=thin, right=thin, top=thin, bottom=thick)

    # Title
    ws.merge_cells("A1:J1")
    ws["A1"] = "MASTER FINANCIAL FLOW & FRAUD CATCHER (DBBL, SIBL, UCB, MMBPLC)"
    ws["A1"].font = Font(name="Segoe UI", size=15, bold=True, color=WHITE)
    ws["A1"].fill = PatternFill("solid", fgColor=NAVY)
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 32

    ws.merge_cells("A2:J2")
    ws["A2"] = "Tracking exact invoice amounts vs. Company Received vs. Actual Guard Payouts (Summary Hit-List)"
    ws["A2"].font = Font(name="Segoe UI", size=10.5, italic=True, color=NAVY)
    ws["A2"].fill = PatternFill("solid", fgColor="E8F0FE")
    ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 22

    # Headers
    headers = [
        ("SL NO", NAVY_LIGHT), ("BANK", NAVY_LIGHT), ("BRANCH / SUB-BRANCH", NAVY_LIGHT), ("DUTY POST", NAVY_LIGHT),
        ("TOTAL BILL OF\nSERVICE (INVOICED)", COL_BILL), 
        ("CO. RECEIVED:\nCOMMISSION ONLY", COL_COMM), ("CO. RECEIVED:\nFULL BILL", COL_COMM),
        ("SALARY GIVEN\nBY COMPANY", COL_CO), ("SALARY GIVEN\nBY BANK", COL_BANK),
        ("REMARK / AUDIT FINDING", NAVY_LIGHT)
    ]
    ws.row_dimensions[4].height = 34
    for col_idx, (txt, color) in enumerate(headers, 1):
        c = ws.cell(row=4, column=col_idx, value=txt)
        c.font = Font(name="Segoe UI", size=9.5, bold=True, color=WHITE)
        c.fill = PatternFill("solid", fgColor=color)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = head_b

    # Master Data Matches the logic
    data = [
        ("SIBL", "Mohammadpur", "Tajmohal Road NCR ATM", 39000, None, 39000, 27000, 27000, "🚨 FRAUD (DOUBLE PAY): Both salary columns filled. 54k paid out for a 27k post. Jahed (Bank) vs Sabbir/Mabudul (Co)."),
        ("SIBL", "Dakkhin Khan", "Dakkhin Khan Branch", 55000, None, 55000, None, 34500, "🚨 FRAUD (DOUBLE BILLING): Company took full bill but Bank paid Nazrul directly."),
        ("SIBL", "Dakkhin Khan", "Dakkhin Khan ATM", 44550, None, 44550, None, 24000, "🚨 FRAUD (DOUBLE BILLING): Company took full bill but Bank paid Sadek & Nurul directly."),
        ("SIBL", "Sherpur", "S.S Filling & Babor Rice Mill", 103950, None, 103950, None, 69100, "🚨 FRAUD: Full bill claimed while Bank directly paid Soukat Jahan Khan 69.1k."),
        ("SIBL", "Khulna", "Hazi Mohshin Road ATM", None, None, None, None, 27000, "⚠️ FRAUD: 3 guards' salary (27k) sent to single A/C of Utpal Biswas."),
        ("SIBL", "Shyamoli", "Shyamoli Branch", 71375, 5944, None, None, 55500, "✅ CLEAN: Bank paid guards direct, Company took commission."),
        ("SIBL", "Shyamoli", "Adabor NCR ATM", 44550, 9285, None, None, 27000, "✅ CLEAN: Bank paid guards direct, Company took commission."),
        ("UCB", "Station Road", "Station Road Branch", None, None, None, 71000, 58000, "🚨 FRAUD (GHOST PAYROLL): Bank paid fake names (Kamal/Mohi); Real workers paid via Upay (Company)."),
        ("UCB", "Dampara", "Dampara Branch", None, None, None, 30000, 64000, "🚨 FRAUD (GHOST PAYROLL): Bank paid 4 fake names; Real workers paid via Upay (Company)."),
        ("UCB", "Narshinghpur", "Narshinghpur Branch", None, None, None, 52000, 55000, "🚨 FRAUD (GHOST PAYROLL): Bank paid fake names; Real workers paid via Upay (Company)."),
        ("UCB", "Tejgaon", "BAF Shaheen College ATM", 39000, None, 39000, 29800, None, "⚠️ FRAUD (POOLING): Company received full bill, paid 3 guards' money to single A/C (Idris Ali)."),
        ("UCB", "Karnafuli", "Bohaddarhat Branch", None, None, None, None, 32000, "⚠️ SUSPICIOUS: Abnormally high single disbursement to Jasim Uddin."),
        ("UCB", "Moulavi Bazar", "Moulvibazar Branch (11 Staff)", 198163, 9513, None, 187500, None, "✅ CLEAN: Company disbursed local bill (Bill-05)."),
        ("UCB", "Keraniganj", "Keraniganj ATM", 11000, 1000, None, 10000, None, "✅ CLEAN: ADC Bill."),
        ("DBBL", "Boro Bazar", "Boro Bazar Branch", None, None, None, None, 35250, "🚨 FRAUD (POOLING): Hafizul Islam paid Tk 35.2k single draw."),
        ("DBBL", "Turag", "Ranavola Sub Branch", 44850, 4600, None, None, 34400, "✅ CLEAN: Math matches perfectly. Bank paid guards, company took commission."),
        ("DBBL", "Basaboo", "Basaboo Tempo Stand FT", 44850, 4000, None, None, 35000, "✅ CLEAN: ADC Bill-23 matches guard pay."),
        ("MMBPLC", "Central (27 Locs)", "Master Bill (151+ Staff)", 2384700, None, 2052915, None, None, "⚠️ AUDIT PENDING: Full net bill collected. Awaiting guard field payout reconciliation.")
    ]

    start_r = 5
    for idx, (bank, branch, post, bill, cocomm, cofull, salco, salbank, remark) in enumerate(data):
        curr_r = start_r + idx
        ws.row_dimensions[curr_r].height = 28
        
        is_z = (idx % 2 == 1)
        bg_fill = PatternFill("solid", fgColor=ZEBRA) if is_z else PatternFill("solid", fgColor=WHITE)
        
        if "🚨" in remark:
            bg_fill = PatternFill("solid", fgColor=RED_FILL)
        elif "⚠️" in remark:
            bg_fill = PatternFill("solid", fgColor=WARN_FILL)
        elif "✅" in remark:
            bg_fill = PatternFill("solid", fgColor=GREEN_FILL)

        # Apply specific border rule (No bottom border unless it's the last row)
        is_last_row = (idx == len(data) - 1)
        active_border = b_last_row if is_last_row else b_no_bottom

        row_vals = [idx+1, bank, branch, post, bill, cocomm, cofull, salco, salbank, remark]
        
        for c_idx, val in enumerate(row_vals, 1):
            c = ws.cell(row=curr_r, column=c_idx, value=val)
            c.border = active_border
            c.fill = bg_fill
            
            c.font = Font(name="Segoe UI", size=9.5)
            
            if c_idx in [1, 2]: 
                c.alignment = Alignment(horizontal="center", vertical="center")
                if c_idx == 2: c.font = Font(name="Segoe UI", size=9.5, bold=True)
            elif c_idx in [3, 4, 10]: 
                c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            elif c_idx >= 5 and c_idx <= 9:
                c.alignment = Alignment(horizontal="right", vertical="center")
                if val is not None:
                    # REAL CURRENCY FORMATTING
                    c.number_format = '[$BDT] #,##0.00'
                    c.font = Font(name="Segoe UI", size=9.5, bold=True)
                    
            if c_idx == 10:
                if "🚨" in remark: c.font = Font(name="Segoe UI", size=9.5, bold=True, color=RED_TXT)
                elif "⚠️" in remark: c.font = Font(name="Segoe UI", size=9.5, bold=True, color=WARN_TXT)
                elif "✅" in remark: c.font = Font(name="Segoe UI", size=9.5, bold=True, color=GREEN_TXT)

    tot_r = start_r + len(data)
    ws.row_dimensions[tot_r].height = 28
    ws.cell(row=tot_r, column=1, value="TOTALS").font = Font(name="Segoe UI", size=10, bold=True)
    ws.merge_cells(f"A{tot_r}:D{tot_r}")
    ws.cell(row=tot_r, column=1).alignment = Alignment(horizontal="right", vertical="center")

    for col_idx in range(5, 10):
        col_l = get_column_letter(col_idx)
        c = ws.cell(row=tot_r, column=col_idx, value=f"=SUM({col_l}5:{col_l}{tot_r-1})")
        c.number_format = '[$BDT] #,##0.00'
        c.font = Font(name="Segoe UI", size=10, bold=True, color=NAVY)
        c.alignment = Alignment(horizontal="right", vertical="center")

    for c_idx in range(1, 11):
        ws.cell(row=tot_r, column=c_idx).border = tot_b
        if c_idx > 4: ws.cell(row=tot_r, column=c_idx).fill = PatternFill("solid", fgColor="E2E8F0")

    # Column Widths optimized for A4
    widths = {1: 6, 2: 10, 3: 20, 4: 28, 5: 18, 6: 18, 7: 18, 8: 18, 9: 18, 10: 55}
    for c, w in widths.items(): ws.column_dimensions[get_column_letter(c)].width = w
    ws.freeze_panes = "A5"

    fn = "A4_Financial_Flow_Fraud_Catcher_Master.xlsx"
    wb.save(fn)
    print(f"Generated Premium File: {fn}")

if __name__ == "__main__":
    generate_financial_flow_xlsx()
