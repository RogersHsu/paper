import datetime
today = datetime.date.today()
nextMonday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
thisMonday = today - datetime.timedelta(days=today.weekday())
print(thisMonday)