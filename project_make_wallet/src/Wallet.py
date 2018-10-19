import collections


def make_wallet_money_format(input_dict):
    new_format_wallet = collections.OrderedDict(
        {1: 0, 10: 0, 50: 0, 100: 0, 500: 0, 1000: 0, 5000: 0, 10000: 0, 50000: 0})
    for k, v in input_dict.items():
        if v == 0:
            new_format_wallet[k] = v
    return new_format_wallet


class Wallet:

    def __init__(self, wallet_money):
        self.wallet_money = wallet_money
        balance = 0

        for cash in self.wallet_money.keys():
            if self.wallet_money.get(cash) is not 0:
                balance += cash * self.wallet_money.get(cash)
                self.balance = balance

    def calculate_balance(self):
        balance = 0
        for cash in self.wallet_money.keys():
            if self.wallet_money.get(cash) is not 0:
                balance += cash * self.wallet_money.get(cash)
        self.balance = balance
        return self.balance

    @staticmethod
    def check_money(money):
        cash_type_list = [1, 10, 50, 100, 500, 1000, 5000, 10000, 50000]
        money_dict_format = dict()
        tmp_money = money
        for cash_type in reversed(cash_type_list):
            quotient = tmp_money // cash_type
            remainder = tmp_money % cash_type
            if quotient > 0:
                money_dict_format[cash_type] = quotient
                tmp_money = remainder
            else:
                pass
            if tmp_money == 0:
                break
        return money_dict_format

    def insert_money(self, inserted_money):
        if inserted_money > 0:
            money_dict_format = self.check_money(inserted_money)
            inserted_money_type = list(money_dict_format.keys())
            for money_type in inserted_money_type:
                self.wallet_money[money_type] += money_dict_format.get(money_type)
            self.balance = self.calculate_balance()
            print("추가 금액: {}원, 현재 잔고: {}원".format(inserted_money, self.balance))
        else:
            print("check again.")

    def spend_money(self, spent_money):
        if spent_money > 0:
            total_change = self.balance - spent_money
            if total_change >= 0:
                for cash_type in reversed(list(self.wallet_money.keys())):
                    count = self.wallet_money.get(cash_type)
                    each_balance = cash_type * count
                    each_change = each_balance - spent_money
                    if each_change >= 0:
                        if each_change > 0:
                            self.wallet_money[cash_type] = 0
                            self.insert_money(each_change)
                        else:
                            self.wallet_money[cash_type] = 0
                        break
                    else:
                        self.wallet_money[cash_type] = 0
                        spent_money -= each_balance
            else:
                print("잔액이 부족합니다. \n"
                      "현재 잔고: {}원, 필요 금액: {}원".format(self.balance, total_change * (-1)))
        else:
            print("This is wrong")

    def summary_wallet_balance(self):

        if set(self.wallet_money.values()) == {0}:
            print("Nothing in your wallet!")

        else:
            exist_cash = []
            for cash in self.wallet_money.keys():
                count = self.wallet_money.get(cash)
                if count is not 0:
                    values = (cash, count)
                    exist_cash.append(values)

            summary_strings = ""
            for ex in exist_cash:
                if ex[0] in [1000, 5000, 10000, 50000]:
                    summary_strings += "{}원 {}장 ".format(ex[0], ex[1])
                else:
                    summary_strings += "{}원은 {}개 ".format(ex[0], ex[1])
            summary_strings += "이 있습니다." if summary_strings[-2] == '장' else "가 있습니다."
            summary_strings += "전체 지갑이 있는 금액은 {}원입니다.".format(self.balance)
            print(summary_strings)


if __name__ == '__main__':
    boo_money = collections.OrderedDict({1: 10, 10: 10, 50: 10, 100: 10, 500: 10, 1000: 10, 5000: 10, 10000: 10, 50000: 10})
    boo_wallet = Wallet(boo_money)
    boo_wallet.summary_wallet_balance()

    boo_wallet.insert_money(500)
    boo_wallet.summary_wallet_balance()

    boo_wallet.insert_money(5000)
    boo_wallet.summary_wallet_balance()

    boo_wallet.spend_money(12000)
    boo_wallet.summary_wallet_balance()

    boo_wallet.spend_money(120000)
    boo_wallet.summary_wallet_balance()

    boo_wallet.insert_money(12387478)
    boo_wallet.summary_wallet_balance()
