import json
# from Connector import broker

# print(broker.assets)


class BudgetCategory:
    """
    This is the base class that will be used for creating budget strategies
    - This will save information about each category in a dataframe
    - The dataframe will be backed up to a file

    """
    def __init__(self, broker, app, **kwargs):
        self.broker = broker
        self.app = app
        self.name = kwargs["Name"]
        self.type = kwargs["Type"]
        self.assets = kwargs["Assets"]
        self.cash = kwargs["Cash"]
        self.value = 0

        self.get_value()
        allocate_dict = {}
        for asset in self.assets:
            allocate_dict[asset["Symbol"]] = asset["Qty"]
        self.allocate_assets_cash(cash=self.cash, assets=allocate_dict)

    def get_value(self):
        """
        This will read assets assigned to the budget and calculate value
        :return: dict with information on assets assigned
        """
        value = 0
        for num, asset in enumerate(self.assets):
            # print(self.broker.get_stock_info(asset["Symbol"]))
            # print(self.broker.get_stock_info(asset["Symbol"])["price"])
            # print(asset["Qty"])
            price = self.broker.get_stock_info(asset["Symbol"])["price"]
            asset_value = price * asset["Qty"]
            self.assets[num]["price"] = price
            value += asset_value
            # print(f"{asset['Symbol']} - {asset_value}")
        self.value = round(value, 2)

    def allocate_assets_cash(self, cash=0, assets=None):
        """
        This is used to change the allocated_assets and cash functions in the main app
        :param cash:
        :param assets:
        :return:
        """
        self.app.allocated_cash += cash
        self.app.unallocated_cash -= cash
        if self.app.unallocated_cash < 0:
            raise Exception("Cash Less than zero")
        if assets:
            for asset in assets:
                self.app.unallocated_assets[asset] -= assets[asset]
                if self.app.unallocated_assets[asset] < 0:
                    raise Exception("Assets less than 0")
                self.app.allocated_assets[asset] += assets[asset]

    def unallocate_assets_cash(self, cash=0, assets=None):
        """
        This is used to change the unallocated_assets and cash functions in the main app
        :param cash:
        :param assets:
        :return:
        """
        self.app.allocated_cash -= cash
        if self.app.allocated_cash < 0:
            raise Exception("Cash Less than zero")
        self.app.unallocated_cash += cash
        if assets:
            for asset in assets:
                self.app.unallocated_assets[asset] += assets[asset]
                self.app.allocated_assets[asset] -= assets[asset]
                if self.app.allocated_assets[asset] < 0:
                    raise Exception("Assets Less than zero")

    def strategy(self):
        """
        This will create the basis on how the app tries to manage this budget
        - maximum growth?
        - Maximum dividend?
        - A mix between the two
        :return:
        """
        pass

    def apply_strategy(self):
        """
        This will take the strategy above and actually make the api calls to make it happen
        :return:
        """
        pass


class EmergencyFund(BudgetCategory):
    def __init__(self, broker, app, minimum, growth=0.02, **kwargs):
        super().__init__(broker, app, **kwargs)
        self.minimum = minimum
        self.growth = growth
        self.cash_needed = 0.0

    def calculate_growth(self):
        """
        My goal is to eventually add a tracker to keep this fund up with inflation. For now,
        let's only track weather or not it has met the goal.
        :return:
        """
        # find difference between goal and value
        diff = round(self.minimum - self.value, 2)
        # if there is a positive difference that means that more money needs to be allocated
        if diff > 0:
            print(f"Total needed to reach goal ${diff}, cash available {self.cash}")
            # if we have the cash in this budget to fill the diff we set that as cash needed
            if self.cash >= diff:
                self.cash_needed = diff
            # if we don't have enough cash, we allocate all that we do have
            else:
                self.cash_needed = self.cash
            print(f"${self.cash_needed} to allocate to this budget")
        # if we have equal or greater than the goal amount don't spend cash, send to other accounts
        else:
            self.cash_needed = 0
            print("No additional funding needed, sending excess to main app")

    def strategy(self):
        """
        Goals:
            1. Pick funds with downside protection so that in a volatile market, losses are minimal
            2. Increase this with inflation (2%) or to reach a target amount and then grow with inflation
            3. Pick funds that provide dividends to help control growth of this fund without selling
        :return:
        """
        # we need a way to see growth
        # Perhaps grab api data from stock over last 30 days and combine results
        pass

    def apply_strategy(self):
        if self.cash_needed > 0:
            print("Buy assets equalling cash needed")
        else:
            print("send cash back go main app")
            self.unallocate_assets_cash(cash=self.cash)


# with open("Budgets/default.json", "r") as f:
#     budget_data = json.load(f)
# budget = EmergencyFund(broker, minimum=1000, **budget_data["EmergencySavings"])
# print(budget.value)
# budget.calculate_growth()
