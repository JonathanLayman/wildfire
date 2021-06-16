import json
from Connector import broker

# print(broker.assets)


class BudgetCategory:
    """
    This is the base class that will be used for creating budget strategies
    - This will save information about each category in a dataframe
    - The dataframe will be backed up to a file

    """
    def __init__(self, broker, **kwargs):
        self.broker = broker
        self.name = kwargs["Name"]
        self.type = kwargs["Type"]
        self.assets = kwargs["Assets"]
        self.cash = kwargs["Cash"]
        self.value = 0

        self.get_value()

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
    def __init__(self, broker, minimum, growth=0.02, **kwargs):
        super().__init__(broker, **kwargs)
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
            # if we have the cash in this budget to fill the diff we set that as cash needed
            if self.cash >= diff:
                self.cash_needed = diff
            # if we don't have enough cash, we allocate all that we do have
            else:
                self.cash_needed = self.cash
        # if we have equal or greater than the goal amount don't spend cash, send to other accounts
        else:
            self.cash_needed = 0
            # create ability to send cash to other accounts here

        # else:
        #     # Calculate if target is on track to match inflation estimated at 2% per year
        #     growth_target = round(self.minimum + (self.minimum * (self.growth / 12)), 2)
        #     print(growth_target)
        #     if self.value > growth_target:
        #         print(f"current value {self.value}, target {growth_target}, no funds need to be committed")
        #     else:
        #         diff = round(growth_target - self.value, 2)
        #         print(f"current value {self.value}, target {growth_target}, need to add {diff}")

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


with open("Budgets/default.json", "r") as f:
    budget_data = json.load(f)
budget = EmergencyFund(broker, minimum=1000, **budget_data["EmergencySavings"])
print(budget.value)
budget.calculate_growth()
