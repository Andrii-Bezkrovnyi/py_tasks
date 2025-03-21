import heapq
import time


class TradeOrder:
    """
    Represents a trade order in the order book.

    Attributes:
        trader_id (int): Unique identifier for the trader.
        volume (float): Amount of UAH to be traded.
        rate (float): Exchange rate in USD.
        is_buy (bool): True for buy orders, False for sale orders.
    """

    def __init__(self, trader_id: int, volume: float, rate: float, is_buy: bool):
        """
        Initializes a TradeOrder.

        Args:
            trader_id (int): Unique identifier for the trader.
            volume (float): Amount of UAH to be traded.
            rate (float): Exchange rate in USD.
            is_buy (bool): True for buy orders, False for sale orders.
        """
        self.trader_id = trader_id
        self.volume = volume
        self.rate = rate
        self.is_buy = is_buy

    def __lt__(self, other: 'TradeOrder') -> bool:
        """
        Compares two TradeOrder instances for sorting in the heap.

        Args:
            other (TradeOrder): The other trade order to compare with.

        Returns:
            bool: True if the current order has higher priority in the heap,
            False otherwise.
        """
        if self.is_buy:  # Buy orders should form a max-heap (higher rate has higher priority)
            return self.rate > other.rate
        else:  # Sell orders should form a min-heap (lower rate has higher priority)
            return self.rate < other.rate


class AccountBalance:
    """
    Manages the account balances for each trader.

    Attributes:
        records (dict[int, dict[str, float]]): A dictionary storing the balances
        for each trader.
    """

    def __init__(self):
        """
        Initializes an AccountBalance object.
        """
        self.records: dict[int, dict[str, float]] = {}

    def modify_balance(self, trader_id: int, amount: float, currency: str):
        """
        Modifies the balance for a trader.

        Args:
            trader_id (int): Unique identifier for the trader.
            amount (float): The amount to modify the balance by
            (positive for deposit, negative for withdrawal).
            currency (str): The currency to modify ('UAH' or 'USD').
        """
        if trader_id not in self.records:
            self.records[trader_id] = {"UAH": 0, "USD": 0}  # Initialize balance if not present
        self.records[trader_id][currency] += amount  # Update balance

    def display_balances(self):
        """
        Displays the current balances for all traders.
        """
        print("\n=== Current Balances ===")
        for trader_id, balances in self.records.items():
            print(f"Trader {trader_id}: {balances}")


class TradingBook:
    """
    Manages the order book and executes trades.

    Attributes:
        buy_queue (list): A max-heap for buy orders.
        sell_queue (list): A min-heap for sale orders.
        account_balance (AccountBalance): The account balances for each trader.
    """

    def __init__(self):
        """
        Initializes a TradingBook object.
        """
        self.buy_queue: list = []  # Max-heap for buy orders
        self.sell_queue: list = []  # Min-heap for sale orders
        self.account_balance = AccountBalance()

    def submit_order(self, trade_order: TradeOrder):
        """
        Submits a trade order to the order book and attempts to process it.

        Args:
            trade_order (TradeOrder): The trade order to submit.
        """
        if trade_order.is_buy:
            heapq.heappush(
                self.buy_queue,
                (-trade_order.rate, trade_order)
            )  # Store buy orders as max-heap
        else:
            heapq.heappush(
                self.sell_queue,
                (trade_order.rate, trade_order)
            )  # Store sell orders as min-heap

        self.process_orders()

    def process_orders(self):
        """
        Processes the orders in the buy and sell queues and executes matching trades.
        """
        while self.buy_queue and self.sell_queue:
            buy_rate, buy_order = self.buy_queue[0]
            sell_rate, sell_order = self.sell_queue[0]

            if -buy_rate >= sell_rate:  # Check if trade can be executed
                trade_volume = min(buy_order.volume, sell_order.volume)
                transaction_value = trade_volume * sell_rate

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

                print(
                    f"Trade Executed: Trader {buy_order.trader_id} buys {trade_volume} UAH at {sell_rate} USD")
                print(
                    f"Trade Executed: Trader {sell_order.trader_id} sells {trade_volume} UAH at {sell_rate} USD")

                buy_order.volume -= trade_volume
                sell_order.volume -= trade_volume

                if buy_order.volume == 0:
                    heapq.heappop(self.buy_queue)
                if sell_order.volume == 0:
                    heapq.heappop(self.sell_queue)
            else:
                break  # No suitable trades available

if __name__ == "__main__":
    # Measure execution time
    start_time = time.perf_counter()

    # Initialize order book
    order_book = TradingBook()

    # Sample trade orders
    order_list = [
        TradeOrder(1, 60, 30, True),
        TradeOrder(2, 60, 24, False),
        TradeOrder(3, 30, 25, True),
        TradeOrder(4, 20, 24, False),
        TradeOrder(5, 80, 27, True),
        TradeOrder(6, 60, 23, False),
        TradeOrder(7, 60, 20, True)
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
