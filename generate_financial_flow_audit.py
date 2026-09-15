import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def generate_financial_flow_xlsx():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Financial Flow Master"
    ws.views.sheetView[0].showGridLines = True

    # Palettes
    NAVY = "0A2540"
    NAVY_LIGHT = "1E3A5F"
    COL_BILL = "1E293B"    # Slate 800
    COL_COMM = "1E3A8A"    # Blue 900
    COL_CO = "064E3B"      # Emerald 900
    COL_BANK = "78350F"    # Amber 900
    WHITE = "FFFFFF"
    
    RED_FILL = "FEE2E2"
    RED_TXT = "991B1B"
    WARN_FILL = "FEF3C7"
    WARN_TXT = "92400E"
    GREEN_FILL = "DCFCE7"
    GREEN_TXT = "166534"
    ZEBRA = "F8FAFC"

    thin = Side(border_style="thin", color="CBD5E1")
    thick = Side(border_style="medium", color="0F172A")
    cell_b = Border(left=thin, right=thin, top=thin, bottom=thin)
    head_b = Border(left=thin, right=thin, top=thick, bottom=thick)
    tot_b = Border(left=thin, right=thin, top=thick, bottom=thick)

    # Title
    ws.merge_cells("A1:J1")
    ws["A1"] = "MASTER FINANCIAL FLOW & FRAUD CATCHER (DBBL, SIBL, UCB, MMBPLC)"
    ws["A1"].font = Font(name="Segoe UI", size=14, bold=True, color=WHITE)
    ws["A1"].fill = PatternFill("solid", fgColor=NAVY)
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:J2")
    ws["A2"] = "Tracking exact invoice amounts vs. Company Received vs. Actual Guard Payouts"
    ws["A2"].font = Font(name="Segoe UI", size=10, italic=True, color=NAVY)
    ws["A2"].fill = PatternFill("solid", fgColor="E8F0FE")
    ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 20

    # Headers
    headers = [
        ("SL NO", NAVY_LIGHT), ("BANK", NAVY_LIGHT), ("BRANCH / SUB-BRANCH", NAVY_LIGHT), ("DUTY POST", NAVY_LIGHT),
        ("TOTAL BILL OF\nSERVICE (INVOICED)", COL_BILL), 
        ("CO. RECEIVED:\nCOMMISSION ONLY", COL_COMM), ("CO. INVOICED:\nFULL BILL CLAIMED", COL_COMM),
        ("SALARY GIVEN\nBY COMPANY", COL_CO), ("SALARY GIVEN\nBY BANK", COL_BANK),
        ("REMARK", NAVY_LIGHT)
    ]
    ws.row_dimensions[4].height = 30
    for col_idx, (txt, color) in enumerate(headers, 1):
        c = ws.cell(row=4, column=col_idx, value=txt)
        c.font = Font(name="Segoe UI", size=9.5, bold=True, color=WHITE)
        c.fill = PatternFill("solid", fgColor=color)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = head_b

    # Master Data - Updated Tajmohal Road logic & Claim Reconciliation
    data = [
        ("SIBL", "Mohammadpur", "Tajmohal Road NCR ATM", 39000, 12000, None, 27000, 27000, "🚨 FRAUD (DOUBLE PAY): Both salary columns filled. 54k paid out for a 27k post. Jahed (Bank) vs Sabbir/Mabudul (Co)."),
        ("SIBL", "Dakkhin Khan", "Dakkhin Khan Branch", 55000, None, 47348, None, 34500, "⚖️ CLAIM RECONCILIATION: Bill-06 claimed Tk 47,348 net. Bank paid Nazrul Tk 34,500 direct; Company invoice requires salary deduction adjustment."),
        ("SIBL", "Dakkhin Khan", "Dakkhin Khan ATM", 44550, None, 38352, None, 24000, "⚖️ CLAIM RECONCILIATION: Bill-07 claimed Tk 38,352 net. Bank paid Sadek & Nurul Tk 24,000 direct; Invoice requires salary deduction adjustment."),
        ("SIBL", "Sherpur", "S.S Filling & Babor Rice Mill", 103950, None, 103950, None, 69100, "⚠️ AUDIT IRREGULARITY: Bills 88 & 89 claim Tk 103,950 while single person (Soukat Jahan) drew Tk 69,100 from bank advice. Verify field disbursement."),
        ("SIBL", "Khulna", "Hazi Mohshin Road ATM", 39000, None, None, None, 27000, "⚠️ POOLED ACCOUNT: 3 guards' salary (Tk 27,000) sent to single A/C of Utpal Biswas. Verify field distribution."),
        ("SIBL", "Shyamoli", "Shyamoli Branch", 71375, 5944, None, None, 55500, "✅ CLEAN: Bank paid guards direct (Tk 55.5k), Company billed & received commission only (Tk 5,944, Bill-08)."),
        ("SIBL", "Shyamoli", "Adabor NCR ATM", 44550, 9285, None, None, 27000, "✅ CLEAN: Bank paid guards direct (Tk 27k), Company billed & received commission only (Tk 9,285, Bill-09)."),
        ("UCB", "Chittagong", "Station Road Branch", 85000, None, None, 71000, 58000, "🚨 GHOST PAYROLL: Bank advice drained Tk 58,000 to fake names (Kamal/Mohi); Real on-site staff paid Tk 71,000 via Company Upay wallet."),
        ("UCB", "Chittagong", "Dampara Branch", 80000, None, None, 30000, 64000, "🚨 GHOST PAYROLL: Bank advice drained Tk 64,000 to 4 fake names; Real field messengers (Aslam & Ismail) paid Tk 30,000 via Upay."),
        ("UCB", "Ashulia", "Narshinghpur Branch", 75000, None, None, 52000, 55000, "🚨 GHOST PAYROLL: Bank advice drained Tk 55,000 to 3 fake accounts; Real field workers paid Tk 52,000 via Company Upay wallet."),
        ("UCB", "Tejgaon", "BAF Shaheen College ATM", 39000, None, 33000, None, 29800, "⚠️ POOLED ACCOUNT: Bill-18 claimed Tk 33,000 for 3 guards, but bank paid Tk 29,800 into single A/C of Idris Ali Sardar."),
        ("UCB", "Karnafuli", "Bohaddarhat Branch", 45000, None, None, None, 32000, "⚠️ SUSPICIOUS PAYOUT: Abnormally high single disbursement to Jasim Uddin (Tk 32,000). Verify duty roster."),
        ("UCB", "Moulavi Bazar", "Moulvibazar Branch (11 Staff)", 198163, 9513, None, 187500, None, "✅ CLEAN: Direct branch settlement. Company disbursed local bill for 11 specific staff (Bill-05)."),
        ("UCB", "Keraniganj", "Keraniganj ATM", 11000, 1000, None, 10000, None, "✅ CLEAN: ADC Bill-18 matched. Guard Ripon paid Tk 10,000; Margin Tk 1,000."),
        ("DBBL", "Boro Bazar", "Boro Bazar Branch", 85000, None, None, None, 35250, "🚨 POOLED ACCOUNT: Hafizul Islam paid Tk 35,250 single draw; Gunman Labu Sheikh draws Tk 25,000 separately."),
        ("DBBL", "Turag", "Ranavola Sub Branch", 44850, 4600, None, None, 34400, "✅ CLEAN: Bill-24 verified. Bank paid guards Tk 34.4k (Apel & Enamul), Company took margin Tk 4.6k."),
        ("DBBL", "Basaboo", "Basaboo Tempo Stand FT", 44850, 4000, None, None, 35000, "✅ CLEAN: ADC Bill-23 verified. 2 Guards paid Tk 35k, company margin Tk 4k."),
        ("MMBPLC", "Central (27 Locs)", "Master Bill (151+ Staff)", 2384700, None, 2052915, None, None, "ℹ️ CENTRALIZED MASTER BILL: Net bill claim of Tk 2,052,915 deposited into vendor A/C 111011100000526 for 27 locations nationwide.")
    ]

    start_r = 5
    for idx, (bank, branch, post, bill, cocomm, cofull, salco, salbank, remark) in enumerate(data):
        curr_r = start_r + idx
        ws.row_dimensions[curr_r].height = 24
        
        is_z = (idx % 2 == 1)
        bg_fill = PatternFill("solid", fgColor=ZEBRA) if is_z else None
        
        if "🚨" in remark:
            bg_fill = PatternFill("solid", fgColor=RED_FILL)
        elif "⚠️" in remark:
            bg_fill = PatternFill("solid", fgColor=WARN_FILL)
        elif "⚖️" in remark:
            bg_fill = PatternFill("solid", fgColor="EFF6FF")
        elif "✅" in remark:
            bg_fill = PatternFill("solid", fgColor=GREEN_FILL)

        row_vals = [idx+1, bank, branch, post, bill, cocomm, cofull, salco, salbank, remark]
        
        for c_idx, val in enumerate(row_vals, 1):
            c = ws.cell(row=curr_r, column=c_idx, value=val)
            c.border = cell_b
            if bg_fill: c.fill = bg_fill
            
            c.font = Font(name="Segoe UI", size=9.5)
            
            if c_idx in [1, 2]: c.alignment = Alignment(horizontal="center", vertical="center")
            elif c_idx in [3, 4, 10]: c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            elif c_idx >= 5 and c_idx <= 9:
                c.alignment = Alignment(horizontal="right", vertical="center")
                if val is not None:
                    c.number_format = '[$BDT] #,##0.00'
                    c.font = Font(name="Segoe UI", size=9.5, bold=True)
                    
            if c_idx == 10:
                if "🚨" in remark: c.font = Font(name="Segoe UI", size=9.5, bold=True, color=RED_TXT)
                elif "⚠️" in remark: c.font = Font(name="Segoe UI", size=9.5, bold=True, color=WARN_TXT)
                elif "⚖️" in remark: c.font = Font(name="Segoe UI", size=9.5, bold=True, color="1E40AF")
                elif "✅" in remark: c.font = Font(name="Segoe UI", size=9.5, bold=True, color=GREEN_TXT)

    tot_r = start_r + len(data)
    ws.row_dimensions[tot_r].height = 26
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

    widths = {1: 6, 2: 10, 3: 20, 4: 28, 5: 18, 6: 18, 7: 18, 8: 18, 9: 18, 10: 55}
    for c, w in widths.items(): ws.column_dimensions[get_column_letter(c)].width = w
    ws.freeze_panes = "A5"

    fn = "Financial_Flow_Fraud_Catcher_Master.xlsx"
    wb.save(fn)
    print(f"Generated: {fn}")

if __name__ == "__main__":
    generate_financial_flow_xlsx()
