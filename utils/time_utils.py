from datetime import datetime

def get_current_date():
    current_date = datetime.now().strftime('%Y-%m-%d')
    return current_date

if __name__ == '__main__':
    print(get_current_date())