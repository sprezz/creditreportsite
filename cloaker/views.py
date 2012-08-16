# Create your views here.



#get ip, ua, city, state, country
#get organization

def from_another_bank():
    pass

def visited_within_last():
    pass

def can_save_cookies():
    pass

def blocked_ips():
    pass

def blocked_states():
    pass

def blocked_cities():
    pass

def blocked_organizations():
    pass

def blocked_zip_codes():
    pass

def date_times():
    pass

try:
    can_save_cookies.count += 1
except AttributeError:
    can_save_cookies.count = 0
print(can_save_cookies.count)
