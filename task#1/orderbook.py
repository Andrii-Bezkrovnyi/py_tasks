import time

class TradeOrder:
    def __init__(self, trader_id, volume, rate, is_buy):
        self.trader_id = trader_id
        self.volume = volume
        self.rate = rate
        self.is_buy = is_buy

class AccountBalance:
    def __init__(self):
        self.records = {}

    def modify_balance(self, trader_id, amount, currency):
        if trader_id not in self.records:
            self.records[trader_id] = {"UAH": 0, "USD": 0}
        self.records[trader_id][currency] += amount

    def display_balances(self):
        print("\n=== Current Balances ===")
        for trader_id, balances in self.records.items():
            print(f"Trader {trader_id}: {balances}")

class TradingBook:
    def __init__(self):
        self.buy_queue = []  # Buy orders
        self.sell_queue = []  # Sell orders
        self.account_balance = AccountBalance()

    def submit_order(self, trade_order):
        if trade_order.is_buy:
            self.buy_queue.append(trade_order)
            self.buy_queue.sort(key=lambda x: -x.rate)  # Sort by descending price
        else:
            self.sell_queue.append(trade_order)
            self.sell_queue.sort(key=lambda x: x.rate)  # Sort by ascending price

        self.process_orders()

    def process_orders(self):
        while self.buy_queue and self.sell_queue:
            buy_order = self.buy_queue[0]
            sell_order = self.sell_queue[0]

            if buy_order.rate >= sell_order.rate:
                trade_volume = min(buy_order.volume, sell_order.volume)
                transaction_value = trade_volume * sell_order.rate

                # Verify buyer's balance
                if self.account_balance.records.get(buy_order.trader_id, {}).get("USD", 0) < transaction_value:
                    print(f"Trader {buy_order.trader_id} lacks sufficient USD.")
                    return

                # Verify seller's balance
                if self.account_balance.records.get(sell_order.trader_id, {}).get("UAH", 0) < trade_volume:
                    print(f"Trader {sell_order.trader_id} lacks sufficient UAH.")
                    return

                # Update balances
                self.account_balance.modify_balance(buy_order.trader_id, -transaction_value, "USD")
                self.account_balance.modify_balance(buy_order.trader_id, trade_volume, "UAH")
                self.account_balance.modify_balance(sell_order.trader_id, -trade_volume, "UAH")
                self.account_balance.modify_balance(sell_order.trader_id, transaction_value, "USD")

                print(f"Trade Executed: Trader {buy_order.trader_id} buys {trade_volume} UAH at {sell_order.rate} USD")
                print(f"Trade Executed: Trader {sell_order.trader_id} sells {trade_volume} UAH at {sell_order.rate} USD")

                buy_order.volume -= trade_volume
                sell_order.volume -= trade_volume

                if buy_order.volume == 0:
                    self.buy_queue.pop(0)
                if sell_order.volume == 0:
                    self.sell_queue.pop(0)
            else:
                break

if __name__ == "__main__":
    # Measure execution time
    start_time = time.perf_counter()

    # Initialize order book
    order_book = TradingBook()

    # Sample orders
    order_list = [
        TradeOrder(1, 50, 25, True),
        TradeOrder(2, 50, 24, False),
        TradeOrder(3, 30, 26, True),
        TradeOrder(4, 20, 23, False),
        TradeOrder(5, 70, 27, True),
        TradeOrder(6, 60, 22, False),
        TradeOrder(7, 40, 28, True)
    ]

    # Set initial balances
    order_book.account_balance.modify_balance(1, 2000, "USD")
    order_book.account_balance.modify_balance(2, 100, "UAH")
    order_book.account_balance.modify_balance(3, 1500, "USD")
    order_book.account_balance.modify_balance(4, 50, "UAH")
    order_book.account_balance.modify_balance(5, 3000, "USD")
    order_book.account_balance.modify_balance(6, 120, "UAH")
    order_book.account_balance.modify_balance(7, 500, "USD")

    # Place orders
    for order in order_list:
        order_book.submit_order(order)

    # Display final balances
    order_book.account_balance.display_balances()

    # Print execution time
    end_time = time.perf_counter()
    print(f"Execution Time: {end_time - start_time:.6f} seconds")
