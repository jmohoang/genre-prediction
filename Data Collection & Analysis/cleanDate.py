import csv
import datetime


def split_date(date):
    """"""
    try:
        month, day, year = date.split("/")
        month = int(month)
        day = int(day)
        year = int(year)
        return month, day, year
    except: ValueError


def combine_date(month, day, year):
    date_string = str(month) + "/" + str(day) + "/" + str(year)
    return date_string


def diff_dates(date1, date2):
    """"""
    try:
        month1, day1, year1 = split_date(date1)
        month2, day2, year2 = split_date(date2)
        date1 = datetime.date(year1, month1, day1)  # Overriding date1 so that it is a date object not a string
        date2 = datetime.date(year2, month2, day2)
        days_between = abs(date1 - date2).days
        return str(days_between)
    except: TypeError
#print(diff_dates("11/1/2012", "11/5/2016"))


def date_created_change_format(date):
    """"""
    months = ["January",
              "February",
              "March",
              "April",
              "May",
              "June",
              "July",
              "August",
              "September",
              "October",
              "November",
              "December"]
    try:
        month, day, year = date.split()
        if month in months:
            month = months.index(month)+1
        day = day.strip(",")
        new_date = combine_date(month, day, year)
        return new_date
    except: ValueError
#print(date_created_change_format("January 27, 2016"))



def edit_days(date, interval):
    """
    This functions reverses a date by certain interval of days.
    :param date:
    :param interval:
    :return: the modified date
    """
    month, day, year = split_date(date)
    thirty_one = [1, 3, 5, 7, 8, 10, 12]  # months that have 31 days
    thirty = [4, 6, 9, 11]
    if interval < day:
        day -= interval
        date = combine_date(month, day, year)
        return date
    else:
        month -= 1
        if month == 0:  # if month was January, we should go back to December, and reduce the year.
            year -= 1
            month = 12
        if month in thirty:
            month_end = 30
        elif month in thirty_one:
            month_end = 31
        else:
            if year % 4 == 0:
                month_end = 29
            else:
                month_end = 28
        day = month_end - (interval % day)
        date = combine_date(month, day, year)
        return date
#print(edit_days("1/5/2016", 5))


def edit_months(date, interval):
    """"""
    month, day, year = split_date(date)
    if interval < month:
        month -= interval
        date = combine_date(month, day, year)
        return date
    else:
        year -= interval // 12
        month -= interval % 12
        if month == 0:
            year -= 1
            month = 12
        date = combine_date(month, day, year)
        return date
        # print(edit_months("11/05/2016", 12))


def reverse_date(old_date, interval):
    """"""
    if len(interval.split()) != 3:
        return ""
    time_interval, interval_type, not_important = interval.split()  # interval_type: something like days or months
    time_interval = int(time_interval)  # this is teh integer part of the interval

    if interval_type == "day" or interval_type == "days":
        return edit_days(old_date, time_interval)
    if interval_type == "month" or interval_type == "months":
        return edit_months(old_date, time_interval)
    return old_date
#print(reverse_date("11/05/2016", "1 day ago"))


def main():
    """"""
    fr = open('goFund.csv', newline='')
    fw = open("go2.csv", "w", newline="")
    writer = csv.writer(fw)
    reader = csv.reader(fr)

    for row in reader:
        new_row = []  # new row that has more information than just the row.

        # Calculate the Last Donation Date
        time = row[1]
        time_interval = row[8]
        lastDonationDate = reverse_date(time, time_interval)

        # Calculate the Difference between Date Created and Last Donaiton Time
        date_created = date_created_change_format(row[7])
        day_difference = diff_dates(time, date_created)

        # Appending information to new_row
        for i in range(9):
            new_row.append(row[i])
        new_row.append(lastDonationDate)
        new_row.append(day_difference)
        for i in range(9, 17):
            new_row.append(row[i])

        # writing new_row to the output file
        writer.writerow(new_row)

    fr.close()
    fw.close()


main()