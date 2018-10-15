import collections


class Wallet:

    def __init__(self, wallet_money):
        self.wallet_money = wallet_money
        self.balance = 0

        for cash in self.wallet_money.keys():
            if self.wallet_money.get(cash) is not 0:
                self.balance += cash * self.wallet_money.get(cash)

    # @property
    # def insert_money(self):
    #     return self.wallet_money
    #
    # @insert_money.setter
    def insert_money(self, inserted_money):
        def check_money(cash):
            cash_list = [1, 10, 50, 100, 500, 1000, 5000, 10000, 50000]
            if isinstance(cash, int):
                if cash in cash_list:
                    return True
                else:
                    print("Please, check money again.")
            else:
                print("Money type is wrong. only integer!")

        check = check_money(inserted_money)
        if check is True:
            self.wallet_money[inserted_money] += 1
        else:
            print("No Way!")

        self.balance += inserted_money
        return self.balance

    @property
    def calculate_balance(self):
        for cash in self.wallet_money.keys():
            if self.wallet_money.get(cash) is not 0:
                self.balance += cash * self.wallet_money.get(cash)
        return self.balance

    @property
    def summary_wallet_balance(self):
        exist_cash = []
        for cash in self.wallet_money.keys():
            count = self.wallet_money.get(cash)
            if count is not 0:
                values = (cash, count)
                exist_cash.append(values)

        summary_strings = ""
        for ex in exist_cash:
            if ex[0] in [1000, 5000, 10000, 50000]:
                print(111, ex)
                summary_strings += "{}원 {}장 ".format(ex[0], ex[1])
            else:
                summary_strings += "{}원은 {}개 ".format(ex[0], ex[1])

        summary_strings += "전체 지갑이 있는 금액은 {}원입니다.".format(self.balance)
        return print(summary_strings)


if __name__ == '__main__':
    boo_money = collections.OrderedDict({1: 0, 10: 210, 50: 0, 100: 0, 500: 0, 1000: 0, 5000: 0, 10000: 0, 50000: 0})
    boo_wallet = Wallet(boo_money)
    boo_wallet.summary_wallet_balance

    boo_wallet.insert_money(500)
    boo_wallet.summary_wallet_balance

    boo_wallet.insert_money(5000)
    boo_wallet.summary_wallet_balance
