import pandas as pd
from recurrent import RecurringEvent
from dateutil import rrule

def update_totals(df):
    if 'total' and 'cum_total' in df:
        df['total'] = 0
        df['cum_total'] = 0
    df['total'] = df.sum(axis=1)
    df['cum_total'] = df['total'].cumsum()
    return df

def plot_budget(df, plt):
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df.total, label='Daily Total')
    plt.plot(df.index, df.cum_total, label='Cumulative Total')
    plt.legend()
    
def get_dates(frequency, today, end):
    try:
        return [pd.Timestamp(frequency).normalize()]
    except ValueError:
        pass
    try:
        r = RecurringEvent()
        r.parse(frequency)
        rr = rrule.rrulestr(r.get_RFC_rrule())
        return [
            pd.to_datetime(date).normalize()
            for date in rr.between(today, end)
        ]
    except ValueError as e:
        raise ValueError('Invalid Frequecy')

def build_calendar(budget, today, end):
    calendar = pd.DataFrame(index=pd.date_range(start=today, end=end))
    for k, v in budget.items():
        frequency = v.get('frequency')
        amount = v.get('amount')
        dates = get_dates(frequency, today, end)
        i = pd.DataFrame(
            data={k: amount},
            index=pd.DatetimeIndex(pd.Series(dates))
        )
        calendar = pd.concat([calendar, i], axis=1).fillna(0)

    calendar = update_totals(calendar)
    return calendar