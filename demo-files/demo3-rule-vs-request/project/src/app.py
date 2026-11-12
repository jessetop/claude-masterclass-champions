"""invoice-tool: prints a fictional invoice total."""
ITEMS = [("pallet wrap", 18.50), ("shipping labels", 7.25), ("tape", 4.10)]
print("Total: %.2f" % sum(price for _, price in ITEMS))
