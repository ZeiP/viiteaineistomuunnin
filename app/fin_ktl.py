import codecs
import datetime

class ReferenceTransferLine(object):

    fields = (('type', {'width': 1, 'required': True, 'just': 'r', 'filler': '0'}), # 3 = reference payment, 5 = direct withdrawal, 7 = reference withdrawal
              ('account_no', {'width': 14, 'required': True, 'just': 'r', 'filler': '0'}),
              ('booking_date', {'width': 6, 'required': True, 'just': 'r', 'filler': '0'}), # yymmdd
              ('payment_date', {'width': 6, 'required': True, 'just': 'r', 'filler': '0'}), # yymmdd
              ('archive_id', {'width': 16, 'required': True, 'just': 'l', 'filler': ' '}),
              ('reference_no', {'width': 20, 'required': True, 'just': 'r', 'filler': '0'}),
              ('payer', {'width': 12, 'required': True, 'just': 'l', 'filler': ' '}),
              ('currency_code', {'width': 1, 'required': True, 'just': 'l', 'filler': ' '}), # 1 = EUR
              ('name_source', {'width': 1, 'required': False, 'just': 'l', 'filler': ' '}), # A = customer-given, J = bank register based on account no, K = clerk-given
              ('amount', {'width': 10, 'required': True, 'just': 'r', 'filler': '0'}),
              ('event_type', {'width': 1, 'required': True, 'just': 'r', 'filler': '0'}), # 0 = normal, 1 = redress
              ('event_source', {'width': 1, 'required': False, 'just': 'l', 'filler': ' '}), # A = from customer, J = bank system, K = from clerk
              ('return_code', {'width': 1, 'required': False, 'just': 'l', 'filler': ' '}), # Used only for direct withdrawals
              )

    def __init__(self):
        for field_name, width in self.fields:
            setattr(self, field_name, '')
        self.type = '3'
        self.currency_code = '1'
        self.event_type = '0'

    @property
    def booking_date(self):
        return self.__booking_date.strftime('%y%m%d')

    @booking_date.setter
    def booking_date(self, x):
        if not isinstance(x, datetime.date):
            return False
        else:
            self.__booking_date = x

    @property
    def payment_date(self):
        return self.__payment_date.strftime('%y%m%d')

    @payment_date.setter
    def payment_date(self, x):
        if not isinstance(x, datetime.date):
            return False
        else:
            self.__payment_date = x

    def __str__(self):
        cont = []
        for field_name, opt in self.fields:
            if opt['required'] and not getattr(self, field_name):
                return False
            if opt['just'] == 'l':
                cont.append(getattr(self, field_name).ljust(opt['width'], opt['filler'])[:opt['width']])
            elif opt['just'] == 'r':
                cont.append(getattr(self, field_name).rjust(opt['width'], opt['filler'])[:opt['width']])
        return ''.join(cont)

if __name__ == "__main__":
    line = ReferenceTransferLine()
    line.account_no = '112233987654321'
    line.booking_date = datetime.date.today()
    line.payment_date = datetime.date.today()
    line.archive_id = 'asdfasdfasdfasdf'
    line.reference_no = '5555'
    line.payer = 'ESIMERKKI ESSI'
    amount = 1.5
    line.amount = str(int(amount * 100))

    print(line)
