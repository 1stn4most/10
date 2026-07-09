from datetime import datetime

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.formatting.rule import ColorScaleRule, DataBarRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.workbook.defined_name import DefinedName

OUTPUT_FILE = "QC_Operations_Management_System_v1.xlsx"
MAX_QC_ROWS = 6000
MAX_CAPACITY_ROWS = 250
REPORT_ROWS = 500


HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
HEADER_FONT = Font(color="FFFFFF", bold=True)
TITLE_FILL = PatternFill("solid", fgColor="0F243E")
TITLE_FONT = Font(color="FFFFFF", bold=True, size=13)
SECTION_FILL = PatternFill("solid", fgColor="D9E1F2")


def style_header_row(ws, row, max_col):
    for col in range(1, max_col + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def style_title(ws, cell, title):
    ws[cell] = title
    ws[cell].fill = TITLE_FILL
    ws[cell].font = TITLE_FONT
    ws[cell].alignment = Alignment(horizontal="left")


def autosize_columns(ws, width_map):
    for col, width in width_map.items():
        ws.column_dimensions[col].width = width


def add_table(ws, name, ref):
    table = Table(displayName=name, ref=ref)
    table.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2", showRowStripes=True, showColumnStripes=False
    )
    ws.add_table(table)


def create_reference_sheet(wb):
    ws = wb.create_sheet("Reference Data")
    ws.sheet_state = "hidden"

    lists = {
        "service_status": [
            "Completed",
            "Partially Completed",
            "Service Not Done (Internal)",
            "Turn Away (Customer)",
        ],
        "yes_no": ["Yes", "No"],
        "closed_status": ["Open", "Closed"],
        "capacity_status": ["Full Time", "Part Time", "As Needed", "Vacation", "Leave"],
        "photo_score": [1, 2, 3, 4, 5],
    }

    col = 1
    for key, values in lists.items():
        ws.cell(row=1, column=col, value=key)
        for idx, value in enumerate(values, start=2):
            ws.cell(row=idx, column=col, value=value)
        start = ws.cell(row=2, column=col).coordinate
        end = ws.cell(row=len(values) + 1, column=col).coordinate
        wb.defined_names[key] = DefinedName(name=key, attr_text=f"'Reference Data'!${start}:${end}")
        col += 1


def create_qc_log_sheet(wb):
    ws = wb.active
    ws.title = "QC LOG"
    style_title(ws, "A1", "QC LOG (MASTER DATABASE)")

    headers = [
        "Date",
        "Job Number",
        "Customer",
        "Location",
        "Technician",
        "Service Status",
        "Reason Missed",
        "Reason Code",
        "Go Back Required",
        "Complaint",
        "Accident",
        "Abnormal Event",
        "CAT Required",
        "Hot List",
        "Site Condition",
        "Photo Audit",
        "Photos Uploaded",
        "Before Photos",
        "During Photos",
        "After Photos",
        "Roof Photos",
        "Fan Photos",
        "Horizontal Duct Photos",
        "Vertical Duct Photos",
        "Overall Photo Score (1-5)",
        "Comments",
        "Fan Left Running",
        "Horizontal Duct Properly Cleaned",
        "Vertical Duct Properly Cleaned",
        "Hoods Properly Cleaned",
        "Grease Remaining",
        "Access Panels Installed",
        "Equipment Left Properly",
        "Area Cleaned",
        "Final QC Score",
        "Corrective Action Taken",
        "Incident",
        "Action Taken",
        "Responsible Party",
        "Follow-up Required",
        "Closed",
        "Date Closed",
        "Notes",
        "General Notes",
    ]

    header_row = 3
    for idx, header in enumerate(headers, start=1):
        ws.cell(row=header_row, column=idx, value=header)
    style_header_row(ws, header_row, len(headers))

    last_row = header_row + MAX_QC_ROWS
    add_table(ws, "tblQCLog", f"A{header_row}:AR{last_row}")
    ws.freeze_panes = "A4"

    widths = {
        "A": 12,
        "B": 14,
        "C": 20,
        "D": 24,
        "E": 18,
        "F": 22,
        "G": 20,
        "H": 14,
        "I": 13,
        "J": 12,
        "K": 10,
        "L": 14,
        "M": 13,
        "N": 10,
        "O": 13,
        "P": 11,
        "Q": 13,
        "R": 12,
        "S": 12,
        "T": 12,
        "U": 11,
        "V": 11,
        "W": 16,
        "X": 14,
        "Y": 17,
        "Z": 28,
        "AA": 18,
        "AB": 24,
        "AC": 24,
        "AD": 22,
        "AE": 17,
        "AF": 18,
        "AG": 17,
        "AH": 14,
        "AI": 13,
        "AJ": 22,
        "AK": 11,
        "AL": 14,
        "AM": 30,
        "AN": 30,
    }
    autosize_columns(ws, widths)

    formulas = {
        "AI": '=IF(COUNTA([@[Fan Left Running]]:[@[Area Cleaned]])=0,"",ROUND(COUNTIF([@[Fan Left Running]]:[@[Area Cleaned]],"Yes")/8*100,0))',
        "AL": '=IF([@Closed]="Yes",IF([@[Date Closed]]="",TODAY(),[@[Date Closed]]),"")',
    }

    for row in range(header_row + 1, last_row + 1):
        for col, formula in formulas.items():
            ws[f"{col}{row}"] = formula

    dv_date = DataValidation(type="date", allow_blank=True)
    dv_status = DataValidation(type="list", formula1="=service_status", allow_blank=True)
    dv_yes_no = DataValidation(type="list", formula1="=yes_no", allow_blank=True)
    dv_photo = DataValidation(type="list", formula1="=photo_score", allow_blank=True)

    ws.add_data_validation(dv_date)
    ws.add_data_validation(dv_status)
    ws.add_data_validation(dv_yes_no)
    ws.add_data_validation(dv_photo)

    dv_date.add(f"A4:A{last_row}")
    dv_date.add(f"AL4:AL{last_row}")
    dv_status.add(f"F4:F{last_row}")
    for col in ["I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AK"]:
        dv_yes_no.add(f"{col}4:{col}{last_row}")
    dv_photo.add(f"Y4:Y{last_row}")


def create_technician_capacity_sheet(wb):
    ws = wb.create_sheet("TECHNICIAN CAPACITY")
    style_title(ws, "A1", "TECHNICIAN CAPACITY")

    headers = [
        "Technician",
        "Jobs Per Night",
        "Days Per Week",
        "Maximum Weekly Capacity",
        "Status",
    ]
    row = 3
    for idx, header in enumerate(headers, start=1):
        ws.cell(row=row, column=idx, value=header)
    style_header_row(ws, row, len(headers))

    last_row = row + MAX_CAPACITY_ROWS
    add_table(ws, "tblCapacity", f"A{row}:E{last_row}")

    for r in range(row + 1, last_row + 1):
        ws[f"D{r}"] = "=IF(OR([@[Jobs Per Night]]="" ,[@[Days Per Week]]=""),"",[@[Jobs Per Night]]*[@[Days Per Week]])"

    dv_status = DataValidation(type="list", formula1="=capacity_status", allow_blank=True)
    ws.add_data_validation(dv_status)
    dv_status.add(f"E4:E{last_row}")

    ws.freeze_panes = "A4"
    autosize_columns(ws, {"A": 18, "B": 15, "C": 15, "D": 24, "E": 14})


def create_technician_utilization_sheet(wb):
    ws = wb.create_sheet("TECHNICIAN UTILIZATION")
    style_title(ws, "A1", "TECHNICIAN UTILIZATION")

    headers = [
        "Technician",
        "Capacity",
        "Completed",
        "Unique Locations",
        "Completion Rate",
        "Capacity Utilization",
        "Missed Jobs",
        "Go Backs",
        "Complaints",
        "Photo Compliance",
        "Average QC",
    ]

    for idx, header in enumerate(headers, start=1):
        ws.cell(row=3, column=idx, value=header)
    style_header_row(ws, 3, len(headers))

    ws["A4"] = "=LET(t1,FILTER(tblCapacity[Technician],tblCapacity[Technician]<>\"\"),t2,FILTER(tblQCLog[Technician],tblQCLog[Technician]<>\"\"),SORT(UNIQUE(VSTACK(t1,t2))))"

    for row in range(4, 304):
        ws[f"B{row}"] = '=IF($A{0}="","",IFERROR(XLOOKUP($A{0},tblCapacity[Technician],tblCapacity[Maximum Weekly Capacity],0),0))'.format(row)
        ws[f"C{row}"] = '=IF($A{0}="","",COUNTIFS(tblQCLog[Technician],$A{0},tblQCLog[Service Status],"Completed"))'.format(row)
        ws[f"D{row}"] = '=IF($A{0}="","",COUNTA(UNIQUE(FILTER(tblQCLog[Location],tblQCLog[Technician]=$A{0}))))'.format(row)
        ws[f"E{row}"] = '=IF($A{0}="","",IFERROR($C{0}/COUNTIFS(tblQCLog[Technician],$A{0}),0))'.format(row)
        ws[f"F{row}"] = '=IF($A{0}="","",IFERROR($C{0}/$B{0},0))'.format(row)
        ws[f"G{row}"] = '=IF($A{0}="","",COUNTIFS(tblQCLog[Technician],$A{0},tblQCLog[Service Status],"Service Not Done (Internal)")+COUNTIFS(tblQCLog[Technician],$A{0},tblQCLog[Service Status],"Turn Away (Customer)"))'.format(row)
        ws[f"H{row}"] = '=IF($A{0}="","",COUNTIFS(tblQCLog[Technician],$A{0},tblQCLog[Go Back Required],"Yes"))'.format(row)
        ws[f"I{row}"] = '=IF($A{0}="","",COUNTIFS(tblQCLog[Technician],$A{0},tblQCLog[Complaint],"Yes"))'.format(row)
        ws[f"J{row}"] = '=IF($A{0}="","",IFERROR(COUNTIFS(tblQCLog[Technician],$A{0},tblQCLog[Photos Uploaded],"Yes")/COUNTIFS(tblQCLog[Technician],$A{0}),0))'.format(row)
        ws[f"K{row}"] = '=IF($A{0}="","",IFERROR(AVERAGEIFS(tblQCLog[Final QC Score],tblQCLog[Technician],$A{0}),0))'.format(row)

    ws.conditional_formatting.add("F4:F303", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="63C384"))
    ws.conditional_formatting.add("K4:K303", ColorScaleRule(start_type="num", start_value=0, start_color="F8696B", mid_type="num", mid_value=75, mid_color="FFEB84", end_type="num", end_value=100, end_color="63BE7B"))

    ws.freeze_panes = "A4"
    autosize_columns(ws, {"A": 20, "B": 12, "C": 10, "D": 16, "E": 16, "F": 18, "G": 12, "H": 10, "I": 11, "J": 16, "K": 12})


def create_dashboard_sheet(wb):
    ws = wb.create_sheet("DASHBOARD")
    style_title(ws, "A1", "QUALITY CONTROL & OPERATIONS DASHBOARD")

    kpis = [
        ("Jobs Completed Today", '=COUNTIFS(tblQCLog[Date],TODAY(),tblQCLog[Service Status],"Completed")'),
        ("Jobs Completed This Pay Period", '=LET(start,TODAY()-MOD(TODAY()-DATE(2024,1,1),14),COUNTIFS(tblQCLog[Date],">="&start,tblQCLog[Date],"<"&start+14,tblQCLog[Service Status],"Completed"))'),
        ("Jobs Missed", '=COUNTIFS(tblQCLog[Service Status],"Service Not Done (Internal)")+COUNTIFS(tblQCLog[Service Status],"Turn Away (Customer)")'),
        ("Revenue Lost", "=SUM('MISSED JOBS & MISSED REVENUE'!G7:G506)"),
        ("Go Backs", '=COUNTIFS(tblQCLog[Go Back Required],"Yes")'),
        ("Complaint Rate", '=IFERROR(COUNTIFS(tblQCLog[Complaint],"Yes")/COUNTA(tblQCLog[Job Number]),0)'),
        ("Photo Compliance", '=IFERROR(COUNTIFS(tblQCLog[Photos Uploaded],"Yes")/COUNTA(tblQCLog[Job Number]),0)'),
        ("Average QC Score", '=IFERROR(AVERAGE(tblQCLog[Final QC Score]),0)'),
        ("Average Photo Score", '=IFERROR(AVERAGE(tblQCLog[Overall Photo Score (1-5)]),0)'),
    ]

    ws["A3"] = "KPI"
    ws["B3"] = "Value"
    style_header_row(ws, 3, 2)
    for idx, (name, formula) in enumerate(kpis, start=4):
        ws[f"A{idx}"] = name
        ws[f"B{idx}"] = formula

    ws["D3"] = "Technician Rankings (by Utilization)"
    ws["D3"].fill = SECTION_FILL
    ws["D3"].font = Font(bold=True)
    ws["D4"] = "Technician"
    ws["E4"] = "Utilization"
    style_header_row(ws, 4, 5)
    ws["D5"] = "=TAKE(SORTBY(FILTER('TECHNICIAN UTILIZATION'!A4:K303,'TECHNICIAN UTILIZATION'!A4:A303<>\"\"),'TECHNICIAN UTILIZATION'!F4:F303,-1),10,1)"
    ws["E5"] = "=TAKE(SORT(FILTER('TECHNICIAN UTILIZATION'!F4:F303,'TECHNICIAN UTILIZATION'!A4:A303<>\"\"),,-1),10)"

    ws["G3"] = "Top Missed Reasons"
    ws["G3"].fill = SECTION_FILL
    ws["G3"].font = Font(bold=True)
    ws["G4"] = "Reason"
    ws["H4"] = "Count"
    style_header_row(ws, 4, 8)
    ws["G5"] = "=TAKE(SORTBY(UNIQUE(FILTER(tblQCLog[Reason Missed],tblQCLog[Reason Missed]<>\"\")),COUNTIF(tblQCLog[Reason Missed],UNIQUE(FILTER(tblQCLog[Reason Missed],tblQCLog[Reason Missed]<>\"\"))),-1),10)"
    ws["H5"] = "=COUNTIF(tblQCLog[Reason Missed],G5#)"

    ws["A16"] = "Month"
    ws["B16"] = "Completed Jobs"
    style_header_row(ws, 16, 2)
    ws["A17"] = "=EOMONTH(TODAY(),-11)"
    for r in range(18, 29):
        ws[f"A{r}"] = f"=EOMONTH(A{r-1},1)"
    for r in range(17, 29):
        ws[f"B{r}"] = f'=COUNTIFS(tblQCLog[Date],">="&EOMONTH(A{r},-1)+1,tblQCLog[Date],"<="&EOMONTH(A{r},0),tblQCLog[Service Status],"Completed")'

    bar_chart = BarChart()
    bar_chart.title = "Top Missed Reasons"
    bar_chart.y_axis.title = "Count"
    bar_chart.x_axis.title = "Reason"
    data = Reference(ws, min_col=8, min_row=4, max_row=14)
    cats = Reference(ws, min_col=7, min_row=5, max_row=14)
    bar_chart.add_data(data, titles_from_data=True)
    bar_chart.set_categories(cats)
    bar_chart.height = 6
    bar_chart.width = 8
    ws.add_chart(bar_chart, "G16")

    line_chart = LineChart()
    line_chart.title = "Monthly Completed Trend"
    trend_data = Reference(ws, min_col=2, min_row=16, max_row=28)
    trend_cats = Reference(ws, min_col=1, min_row=17, max_row=28)
    line_chart.add_data(trend_data, titles_from_data=True)
    line_chart.set_categories(trend_cats)
    line_chart.height = 6
    line_chart.width = 8
    ws.add_chart(line_chart, "A30")

    pie_chart = PieChart()
    pie_chart.title = "Service Status Mix"
    ws["D16"] = "Status"
    ws["E16"] = "Count"
    style_header_row(ws, 16, 5)
    statuses = ["Completed", "Partially Completed", "Service Not Done (Internal)", "Turn Away (Customer)"]
    for i, status in enumerate(statuses, start=17):
        ws[f"D{i}"] = status
        ws[f"E{i}"] = f'=COUNTIFS(tblQCLog[Service Status],"{status}")'
    pie_data = Reference(ws, min_col=5, min_row=16, max_row=20)
    pie_labels = Reference(ws, min_col=4, min_row=17, max_row=20)
    pie_chart.add_data(pie_data, titles_from_data=True)
    pie_chart.set_categories(pie_labels)
    pie_chart.height = 6
    pie_chart.width = 7
    ws.add_chart(pie_chart, "D30")

    autosize_columns(ws, {"A": 34, "B": 18, "D": 28, "E": 14, "G": 28, "H": 12})


def create_technician_scorecards_sheet(wb):
    ws = wb.create_sheet("TECHNICIAN SCORECARDS")
    style_title(ws, "A1", "TECHNICIAN SCORECARD")

    ws["A3"] = "Select Technician"
    ws["B3"] = "=IFERROR(INDEX(SORT(UNIQUE(FILTER(tblQCLog[Technician],tblQCLog[Technician]<>\"\"))),1),\"\")"

    metrics = [
        ("Jobs Completed", '=IF($B$3="","",COUNTIFS(tblQCLog[Technician],$B$3,tblQCLog[Service Status],"Completed"))'),
        ("Unique Locations", '=IF($B$3="","",COUNTA(UNIQUE(FILTER(tblQCLog[Location],tblQCLog[Technician]=$B$3))))'),
        ("Completion Rate", '=IF($B$3="","",IFERROR(COUNTIFS(tblQCLog[Technician],$B$3,tblQCLog[Service Status],"Completed")/COUNTIFS(tblQCLog[Technician],$B$3),0))'),
        ("Capacity", '=IF($B$3="","",IFERROR(XLOOKUP($B$3,tblCapacity[Technician],tblCapacity[Maximum Weekly Capacity],0),0))'),
        ("Capacity Utilization", '=IFERROR(B8/B9,0)'),
        ("Go Backs", '=COUNTIFS(tblQCLog[Technician],$B$3,tblQCLog[Go Back Required],"Yes")'),
        ("Complaints", '=COUNTIFS(tblQCLog[Technician],$B$3,tblQCLog[Complaint],"Yes")'),
        ("Average QC Score", '=IFERROR(AVERAGEIFS(tblQCLog[Final QC Score],tblQCLog[Technician],$B$3),0)'),
        ("Average Photo Score", '=IFERROR(AVERAGEIFS(tblQCLog[Overall Photo Score (1-5)],tblQCLog[Technician],$B$3),0)'),
        ("Photo Compliance", '=IFERROR(COUNTIFS(tblQCLog[Technician],$B$3,tblQCLog[Photos Uploaded],"Yes")/COUNTIFS(tblQCLog[Technician],$B$3),0)'),
        ("Revenue Missed", '=SUMIFS(\'MISSED JOBS & MISSED REVENUE\'!G7:G506,\'MISSED JOBS & MISSED REVENUE\'!E7:E506,$B$3)'),
        ("CAT Events", '=COUNTIFS(tblQCLog[Technician],$B$3,tblQCLog[CAT Required],"Yes")'),
        ("Accidents", '=COUNTIFS(tblQCLog[Technician],$B$3,tblQCLog[Accident],"Yes")'),
        ("Outstanding Events", '=COUNTIFS(tblQCLog[Technician],$B$3,tblQCLog[Closed],"No")'),
        ("Trend vs Previous Pay Period", '=LET(start,TODAY()-MOD(TODAY()-DATE(2024,1,1),14),curr,COUNTIFS(tblQCLog[Technician],$B$3,tblQCLog[Date],">="&start,tblQCLog[Date],"<"&start+14,tblQCLog[Service Status],"Completed"),prev,COUNTIFS(tblQCLog[Technician],$B$3,tblQCLog[Date],">="&start-14,tblQCLog[Date],"<"&start,tblQCLog[Service Status],"Completed"),curr-prev)')
    ]

    ws["A5"] = "Metric"
    ws["B5"] = "Value"
    style_header_row(ws, 5, 2)

    for i, (metric, formula) in enumerate(metrics, start=6):
        ws[f"A{i}"] = metric
        ws[f"B{i}"] = formula

    ws.conditional_formatting.add("B6:B20", ColorScaleRule(start_type="num", start_value=0, start_color="F8696B", mid_type="num", mid_value=50, mid_color="FFEB84", end_type="num", end_value=100, end_color="63BE7B"))
    autosize_columns(ws, {"A": 34, "B": 22})


def create_missed_jobs_sheet(wb):
    ws = wb.create_sheet("MISSED JOBS & MISSED REVENUE")
    style_title(ws, "A1", "MISSED JOBS & MISSED REVENUE")

    headers = [
        "Date",
        "Job Number",
        "Customer",
        "Location",
        "Technician",
        "Reason",
        "Revenue Lost (Manual)",
        "Recovered?",
        "Recovery Date",
        "Recovery Technician",
    ]
    for idx, header in enumerate(headers, start=1):
        ws.cell(row=6, column=idx, value=header)
    style_header_row(ws, 6, len(headers))

    for row in range(7, 507):
        ws[f"B{row}"] = '=IFERROR(INDEX(FILTER(tblQCLog[Job Number],(tblQCLog[Service Status]="Service Not Done (Internal)")+(tblQCLog[Service Status]="Turn Away (Customer)")),ROW()-6),"")'
        ws[f"A{row}"] = '=IF($B{0}="","",XLOOKUP($B{0},tblQCLog[Job Number],tblQCLog[Date],""))'.format(row)
        ws[f"C{row}"] = '=IF($B{0}="","",XLOOKUP($B{0},tblQCLog[Job Number],tblQCLog[Customer],""))'.format(row)
        ws[f"D{row}"] = '=IF($B{0}="","",XLOOKUP($B{0},tblQCLog[Job Number],tblQCLog[Location],""))'.format(row)
        ws[f"E{row}"] = '=IF($B{0}="","",XLOOKUP($B{0},tblQCLog[Job Number],tblQCLog[Technician],""))'.format(row)
        ws[f"F{row}"] = '=IF($B{0}="","",XLOOKUP($B{0},tblQCLog[Job Number],tblQCLog[Reason Missed],""))'.format(row)

    dv_yes_no = DataValidation(type="list", formula1="=yes_no", allow_blank=True)
    dv_date = DataValidation(type="date", allow_blank=True)
    ws.add_data_validation(dv_yes_no)
    ws.add_data_validation(dv_date)
    dv_yes_no.add("H7:H506")
    dv_date.add("I7:I506")

    ws["L6"] = "Revenue Analytics"
    ws["L6"].fill = SECTION_FILL
    ws["L6"].font = Font(bold=True)
    ws["L7"] = "Total Lost Revenue"
    ws["M7"] = "=SUM(G7:G506)"

    ws["L9"] = "Lost Revenue by Technician"
    ws["L10"] = "Technician"
    ws["M10"] = "Revenue"
    style_header_row(ws, 10, 13)
    ws["L11"] = '=SORT(UNIQUE(FILTER(E7:E506,E7:E506<>"")))'
    ws["M11"] = "=SUMIF(E7:E506,L11#,G7:G506)"

    ws["O9"] = "Lost Revenue by Reason"
    ws["O10"] = "Reason"
    ws["P10"] = "Revenue"
    style_header_row(ws, 10, 16)
    ws["O11"] = '=SORT(UNIQUE(FILTER(F7:F506,F7:F506<>"")))'
    ws["P11"] = "=SUMIF(F7:F506,O11#,G7:G506)"

    rev_chart = BarChart()
    rev_chart.title = "Lost Revenue by Technician"
    rev_data = Reference(ws, min_col=13, min_row=10, max_row=30)
    rev_cats = Reference(ws, min_col=12, min_row=11, max_row=30)
    rev_chart.add_data(rev_data, titles_from_data=True)
    rev_chart.set_categories(rev_cats)
    rev_chart.height = 6
    rev_chart.width = 8
    ws.add_chart(rev_chart, "L22")

    autosize_columns(ws, {"A": 12, "B": 14, "C": 20, "D": 22, "E": 18, "F": 20, "G": 20, "H": 12, "I": 14, "J": 20, "L": 24, "M": 14, "O": 22, "P": 14})


def create_cat_log_sheet(wb):
    ws = wb.create_sheet("CAT LOG")
    style_title(ws, "A1", "CORRECTIVE ACTION TAKEN (CAT) LOG")

    headers = [
        "Date",
        "Job Number",
        "Incident",
        "Root Cause",
        "Corrective Action Taken",
        "Responsible Party",
        "Technician",
        "Customer",
        "Follow-up",
        "Closed",
        "Date Closed",
        "Status",
    ]
    for idx, header in enumerate(headers, start=1):
        ws.cell(row=4, column=idx, value=header)
    style_header_row(ws, 4, len(headers))

    ws["A5"] = '=FILTER(CHOOSE({1,2,3,4,5,6,7,8,9,10,11,12},tblQCLog[Date],tblQCLog[Job Number],tblQCLog[Incident],tblQCLog[Comments],tblQCLog[Corrective Action Taken],tblQCLog[Responsible Party],tblQCLog[Technician],tblQCLog[Customer],tblQCLog[Follow-up Required],tblQCLog[Closed],tblQCLog[Date Closed],IF(tblQCLog[Closed]="Yes","Closed","Open")),tblQCLog[CAT Required]="Yes","")'
    autosize_columns(ws, {"A": 12, "B": 14, "C": 22, "D": 28, "E": 26, "F": 18, "G": 16, "H": 20, "I": 16, "J": 10, "K": 12, "L": 12})


def create_hot_list_sheet(wb):
    ws = wb.create_sheet("HOT LIST")
    style_title(ws, "A1", "HOT LIST (REPEAT ISSUE WATCHLIST)")

    headers = [
        "Expected Next Service Date",
        "Customer",
        "Location",
        "Previous Technician",
        "Issue To Watch",
        "Priority",
        "Assigned Technician",
        "Completed",
    ]
    for idx, header in enumerate(headers, start=1):
        ws.cell(row=4, column=idx, value=header)
    style_header_row(ws, 4, len(headers))

    ws["A5"] = '=FILTER(CHOOSE({1,2,3,4,5,6,7,8},tblQCLog[Date]+30,tblQCLog[Customer],tblQCLog[Location],tblQCLog[Technician],tblQCLog[Comments],IF(tblQCLog[Complaint]="Yes","High",IF(tblQCLog[Go Back Required]="Yes","Medium","Low")),tblQCLog[Technician],tblQCLog[Closed]),(tblQCLog[Hot List]="Yes")*(tblQCLog[Closed]<>"Yes"),"")'

    ws.conditional_formatting.add("F5:F505", ColorScaleRule(start_type="num", start_value=1, start_color="63BE7B", mid_type="num", mid_value=2, mid_color="FFEB84", end_type="num", end_value=3, end_color="F8696B"))
    autosize_columns(ws, {"A": 24, "B": 20, "C": 24, "D": 20, "E": 30, "F": 12, "G": 20, "H": 12})


def create_site_conditions_sheet(wb):
    ws = wb.create_sheet("SITE CONDITIONS LOG")
    style_title(ws, "A1", "SITE CONDITIONS LOG")

    headers = [
        "Customer",
        "Location",
        "Issue",
        "Area",
        "Date First Reported",
        "Last Reported",
        "Customer Notified",
        "Resolved",
        "Resolution Date",
        "Notes",
    ]
    for idx, header in enumerate(headers, start=1):
        ws.cell(row=4, column=idx, value=header)
    style_header_row(ws, 4, len(headers))

    ws["A5"] = '=FILTER(CHOOSE({1,2,3,4,5,6,7,8,9,10},tblQCLog[Customer],tblQCLog[Location],tblQCLog[Comments],tblQCLog[Reason Code],tblQCLog[Date],tblQCLog[Date],tblQCLog[Photo Audit],tblQCLog[Closed],tblQCLog[Date Closed],tblQCLog[Notes]),tblQCLog[Site Condition]="Yes","")'
    autosize_columns(ws, {"A": 20, "B": 24, "C": 30, "D": 16, "E": 18, "F": 15, "G": 18, "H": 12, "I": 16, "J": 24})


def create_biweekly_report_sheet(wb):
    ws = wb.create_sheet("BIWEEKLY MANAGEMENT REPORT")
    style_title(ws, "A1", "BIWEEKLY MANAGEMENT REPORT")

    ws["A3"] = "Executive Summary KPI"
    ws["B3"] = "Current Pay Period"
    style_header_row(ws, 3, 2)

    rows = [
        ("Jobs Completed", '=LET(start,TODAY()-MOD(TODAY()-DATE(2024,1,1),14),COUNTIFS(tblQCLog[Date],">="&start,tblQCLog[Date],"<"&start+14,tblQCLog[Service Status],"Completed"))'),
        ("Jobs Missed", '=LET(start,TODAY()-MOD(TODAY()-DATE(2024,1,1),14),COUNTIFS(tblQCLog[Date],">="&start,tblQCLog[Date],"<"&start+14,tblQCLog[Service Status],"Service Not Done (Internal)")+COUNTIFS(tblQCLog[Date],">="&start,tblQCLog[Date],"<"&start+14,tblQCLog[Service Status],"Turn Away (Customer)"))'),
        ("Revenue Lost", "=SUM('MISSED JOBS & MISSED REVENUE'!G7:G506)"),
        ("Go Backs", '=LET(start,TODAY()-MOD(TODAY()-DATE(2024,1,1),14),COUNTIFS(tblQCLog[Date],">="&start,tblQCLog[Date],"<"&start+14,tblQCLog[Go Back Required],"Yes"))'),
        ("Complaints", '=LET(start,TODAY()-MOD(TODAY()-DATE(2024,1,1),14),COUNTIFS(tblQCLog[Date],">="&start,tblQCLog[Date],"<"&start+14,tblQCLog[Complaint],"Yes"))'),
        ("Photo Compliance", '=LET(start,TODAY()-MOD(TODAY()-DATE(2024,1,1),14),IFERROR(COUNTIFS(tblQCLog[Date],">="&start,tblQCLog[Date],"<"&start+14,tblQCLog[Photos Uploaded],"Yes")/COUNTIFS(tblQCLog[Date],">="&start,tblQCLog[Date],"<"&start+14),0))'),
        ("Average QC", '=LET(start,TODAY()-MOD(TODAY()-DATE(2024,1,1),14),IFERROR(AVERAGEIFS(tblQCLog[Final QC Score],tblQCLog[Date],">="&start,tblQCLog[Date],"<"&start+14),0))'),
    ]

    for i, (name, formula) in enumerate(rows, start=4):
        ws[f"A{i}"] = name
        ws[f"B{i}"] = formula

    ws["D3"] = "Technician Rankings"
    ws["D3"].fill = SECTION_FILL
    ws["D3"].font = Font(bold=True)
    ws["D4"] = "Technician"
    ws["E4"] = "Utilization"
    style_header_row(ws, 4, 5)
    ws["D5"] = "=TAKE(SORTBY(FILTER('TECHNICIAN UTILIZATION'!A4:A303,'TECHNICIAN UTILIZATION'!A4:A303<>\"\"),'TECHNICIAN UTILIZATION'!F4:F303,-1),15)"
    ws["E5"] = "=TAKE(SORT(FILTER('TECHNICIAN UTILIZATION'!F4:F303,'TECHNICIAN UTILIZATION'!A4:A303<>\"\"),,-1),15)"

    ws["G3"] = "Outstanding Hot List Items"
    ws["G3"].fill = SECTION_FILL
    ws["G3"].font = Font(bold=True)
    ws["G4"] = "Customer"
    ws["H4"] = "Location"
    style_header_row(ws, 4, 8)
    ws["G5"] = '=FILTER(\'HOT LIST\'!B5:C505,\'HOT LIST\'!B5:B505<>"","")'

    perf_chart = BarChart()
    perf_chart.title = "Top Performer Utilization"
    perf_data = Reference(ws, min_col=5, min_row=4, max_row=15)
    perf_cats = Reference(ws, min_col=4, min_row=5, max_row=15)
    perf_chart.add_data(perf_data, titles_from_data=True)
    perf_chart.set_categories(perf_cats)
    perf_chart.height = 6
    perf_chart.width = 8
    ws.add_chart(perf_chart, "A14")

    autosize_columns(ws, {"A": 28, "B": 20, "D": 20, "E": 14, "G": 24, "H": 24})


def finalize_workbook(wb):
    wb.defined_names["PayPeriodStart"] = DefinedName(
        name="PayPeriodStart",
        attr_text="=TODAY()-MOD(TODAY()-DATE(2024,1,1),14)",
    )

    for ws in wb.worksheets:
        ws.sheet_view.showGridLines = True


def build_workbook(path=OUTPUT_FILE):
    wb = Workbook()
    create_reference_sheet(wb)
    create_qc_log_sheet(wb)
    create_technician_capacity_sheet(wb)
    create_technician_utilization_sheet(wb)
    create_dashboard_sheet(wb)
    create_technician_scorecards_sheet(wb)
    create_missed_jobs_sheet(wb)
    create_cat_log_sheet(wb)
    create_hot_list_sheet(wb)
    create_site_conditions_sheet(wb)
    create_biweekly_report_sheet(wb)
    finalize_workbook(wb)
    wb.save(path)


if __name__ == "__main__":
    build_workbook()
    print(f"Workbook created: {OUTPUT_FILE}")
