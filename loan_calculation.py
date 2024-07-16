import calendar
import datetime


def loan_calculation(payload):
    total_loan = payload['totalLoan']
    mrr = payload['mrr']
    mrr_in_account = payload['mrrInAccount']
    day = payload['day']
    mrr = float(mrr) + float(mrr_in_account)

    date_string = payload.get('currentDate')
    current_date = datetime.date.today()
    if date_string is not None:
        current_date = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()

    current_month = current_date.month
    current_year = current_date.year
    current_day = current_date.day
    last_day_current_month = calendar.monthrange(current_year, current_month)[1]
    last_day_prev_month = calendar.monthrange(current_year, current_month - 1)[1]
    total_interest = (total_loan * (mrr / 100)) / 12
    if day < current_day:
        days_difference = (current_day - day)
        total_interest = total_interest / (last_day_current_month * days_difference)
    else:
        days_difference = (last_day_prev_month - day) + current_day
        total_interest = total_interest / (last_day_prev_month * days_difference)
    return total_interest
