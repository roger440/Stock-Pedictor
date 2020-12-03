def validate_day(day):
    possible_days = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10","11", "12", "13", "14", "15", "16", "17", "18", "19", "20","21", "22", "23", "24", "25", "26", "27", "28", "29", "30","31"]
    if day not in possible_days:
        raise RuntimeError("invalid day")
def validate_month(month):

    possible_months=["01","02","03","04","05","06","07","08","09","10","11","12"]
    if month not in possible_months:
        raise RuntimeError("invalid month")

def validate_year(year):
    year=int(year)
    if(year < 0 or year > 2030):
        raise RuntimeError("That's an unusual year...")





