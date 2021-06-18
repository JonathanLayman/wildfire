import Budget_Creator
import Connector
import json


class App:
    def __init__(self, budget_file=None):
        self.broker_vendor = "Alpaca"
        self.file = budget_file

        # Assign the proper vendor api
        if self.broker_vendor == "Alpaca":
            self.broker = Connector.AlpacaBroker()
        else:
            print("No other broker has been developed")
            quit()

        # Get information about assets of the brokerage
        self.assets = self.broker.assets
        self.allocated_assets = {}
        for asset in self.assets:
            self.allocated_assets[asset] = 0
        self.unallocated_assets = self.assets.copy()
        self.cash = self.broker.cash
        self.allocated_cash = 0
        self.unallocated_cash = self.cash
        
        # print(self.assets, self.unallocated_assets)
        # self.unallocated_assets["QQQ"] += 10
        # print(self.assets, self.unallocated_assets)

        # read in the budget file if applicable or create a new one
        if self.file is None:
            self.create_initial_budget()
        else:
            self.read_budget_file()

    def create_initial_budget(self):
        """
        This will be used when there is no json file with allocations
        :return:
        """
        pass

    def read_budget_file(self):
        with open(self.file, "r") as f:
            budget_data = json.load(f)
        budget = Budget_Creator.EmergencyFund(self.broker, app=self, minimum=1000, **budget_data["EmergencySavings"])
        # print(budget.value)
        # budget.calculate_growth()
        print(self.unallocated_cash, self.unallocated_assets)
        budget.unallocate_assets_cash(cash=10, assets={"QQQ": 1, "QYLG": 20})
        budget.allocate_assets_cash(cash=10, assets={"QQQ": 1, "QYLG": 20})
        print(self.unallocated_cash, self.unallocated_assets)


if __name__ == "__main__":
    a = App("Budgets/default.json")
