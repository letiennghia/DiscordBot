import gspread
import datetime
gs=gspread.service_account()
sh=gs.open("Copy of |AAC| Database V2")
wsh=sh.worksheet("3rd Wing")
cell=wsh.find("leonarddhi")
print(cell.row)
print(datetime.datetime.today())