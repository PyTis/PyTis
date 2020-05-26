import mx.DateTime
from time import strptime, strftime

def first_of_week(date):
    return date - date.day_of_week

def auto_year(tup, today):
    """ Implicit year algorithm.
    
    tup is a tuple of month/day
    We've got to figure out the year. We do this by seeing
    which one is closer to today. If the date is before
    today then we are going to use.
        
    Input    Today         Output        Note
    05/06    05/06/2006    05/06/2006    Short circuit today
    11/02    11/01/2006    11/02/2006    Greater than, but this year closer
    11/02    01/02/2006    11/02/2005    Greater than, compare this year and
                                         last year
    02/01    02/02/2006    02/02/2006    Less than, but this year closer
    02/01    12/02/2006    02/02/2007    Less than, next year greater
    """
    if tup[0] == today.month and tup[1] == today.day:
        return today
    
    this_year = (today.year,) + tup
    this_year = mx.DateTime.DateTime(*this_year)
    last_year = (today.year-1,) + tup
    last_year = mx.DateTime.DateTime(*last_year)
    next_year = (today.year+1,) + tup
    next_year = mx.DateTime.DateTime(*next_year)
    
    if this_year > today:
        # compare this year and last year
        if this_year - today <= today - last_year:
            return this_year
        else:
            return last_year
    else:
        # today is larger, compare next_year
        if today - this_year <= next_year - today:
            return this_year
        else:
            return next_year

def parse_date(str, today):
    """ This is the mack daddy of American date parsing,
    automatically handling implicit years.
    
    
    """
    try:
        tup = strptime(str, "%m/%d")
        return auto_year(tup[1:3], today)
    except ValueError:
        pass
    return mx.DateTime.DateFrom(str)
    
def relative_fmt(date, today):
    """ Produces a nice format, relative to today. """
    if date.year == today.year:
        return date.strftime("%a %m/%d")
    else:
        return date.strftime("%a %m/%d/%y")