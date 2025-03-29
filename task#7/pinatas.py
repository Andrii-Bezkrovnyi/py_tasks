from functools import lru_cache
import argparse

def max_candies(pinatas):
    """
    Calculate the maximum number of candies that can be obtained by smashing the pinatas.

    The function uses dynamic programming with memoization to calculate the maximum amount of candies
    that can be obtained by smashing pinatas in a given sequence. The recursive function tries to break
    each pinata and calculates the candies that would drop, while considering the effects of breaking
    each pinata between the boundaries 'left' and 'right'.

    Args:
        pinatas (list): A list of integers representing the pinata values (candies).

    Returns:
        int: The maximum number of candies that can be obtained by smashing the pinatas optimally.
    """
    # Add 1 at the beginning and end of the list to handle edge cases easily.
    pinatas = [1] + pinatas + [1]

    @lru_cache(None)
    def dp(left, right):
        """
        A helper function that uses recursion and memoization to calculate the maximum number of candies
        that can be obtained by smashing pinatas between 'left' and 'right' indices.

        Args:
            left (int): The left boundary of the subarray.
            right (int): The right boundary of the subarray.

        Returns:
            int: The maximum candies from smashing the pinatas between the 'left' and 'right' indices.
        """
        if left + 1 == right:
            return 0  # If only one pinata remains, no more candies can be obtained.

        max_candy = 0
        # Iterate through all pinatas between left and right boundaries and simulate smashing each one.
        for i in range(left + 1, right):
            # Calculate candies dropped when pinata i is smashed.
            candies = pinatas[left] * pinatas[i] * pinatas[right]
            # Recursively calculate the candies for the remaining pinatas (before and after pinata i).
            candies += dp(left, i) + dp(i, right)
            # Track the maximum candies obtained.
            max_candy = max(max_candy, candies)

        print(f"dp({left}, {right}) -> {max_candy}")

        return max_candy

    return dp(0, len(pinatas) - 1)

def main():
    """
    Entry point of the program that parses command line arguments and prints the result.

    The script expects a list of integers as input, where each integer represents a pinata.
    It will then compute the maximum number of candies that can be obtained by smashing the pinatas optimally.
    """
    parser = argparse.ArgumentParser(
        description="Calculate max candies from pinatas."
    )
    parser.add_argument(
        "pinatas",
        metavar="12 1 12 2",
        type=int,
        nargs="+",
        help="List of pinata values"
    )

    args = parser.parse_args()
    print(max_candies(args.pinatas))

if __name__ == "__main__":
    main()
