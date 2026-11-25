"""
Traffic fine utilities - hardened version (Lab 7, fuzz testing)

Fixed by: Samvith Vaddiparthi (PES1UG24AM468)

Bugs found with Hypothesis in the original code and how they are fixed:
  * None / non-string input crashed with AttributeError ('.split')
      -> every function checks isinstance(value, str) first
  * wrong number of parts ('', 'TF2024', '72', '72/60/50') crashed while
    unpacking (ValueError)
      -> the number of parts is checked before unpacking
  * empty or non-numeric parts ('--', '500,,300', '/') crashed in int()
      -> every number is validated with _to_int() before use
  * int() silently accepted '+5', ' 7 ', '1_000' and non-ASCII digits
      -> only plain ASCII digits (after trimming spaces) are accepted
  * an empty ticket prefix ('-0- 7 ') was accepted
      -> the prefix must be 1-5 ASCII letters and the year exactly 4 digits
  * negative fines ('-1', '1,-1') produced a negative or wrong total
      -> negative amounts are rejected (they are not valid fines)
  * a limit of 0 ('72/0', '0/0') raised ZeroDivisionError
      -> the speed limit must be greater than 0
  * a speed below the limit ('0/1') returned a negative "percent over limit"
      -> 0 is returned when the driver was not over the limit

Contract: every function returns None for invalid input and never raises.
"""

MAX_FINE_TOTAL = 10000


def _to_int(text, max_digits):
    """Return text as a non-negative int, or None if it is not plain ASCII digits."""
    if not isinstance(text, str):
        return None
    text = text.strip()
    if not text or len(text) > max_digits:
        return None
    if not (text.isascii() and text.isdigit()):
        return None
    return int(text)


def parse_ticket_id(ticket_id):
    """Parse 'PREFIX-YYYY-SERIAL' into (PREFIX, year, serial), or None if invalid."""
    if not isinstance(ticket_id, str):
        return None
    parts = ticket_id.strip().split('-')
    if len(parts) != 3:
        return None
    prefix, year_text, serial_text = (p.strip() for p in parts)
    if not (1 <= len(prefix) <= 5 and prefix.isascii() and prefix.isalpha()):
        return None
    if len(year_text) != 4:
        return None
    year = _to_int(year_text, max_digits=4)
    serial = _to_int(serial_text, max_digits=10)
    if year is None or serial is None:
        return None
    return prefix.upper(), year, serial


def total_fines(amounts_csv):
    """Sum comma-separated fine amounts (capped at 10000), or None if invalid."""
    if not isinstance(amounts_csv, str):
        return None
    amounts = []
    for part in amounts_csv.split(','):
        amount = _to_int(part, max_digits=9)
        if amount is None:          # empty, non-numeric or negative amount
            return None
        amounts.append(amount)
    total = sum(amounts)
    if total > MAX_FINE_TOTAL:
        total = MAX_FINE_TOTAL
    return total


def speed_excess(reading):
    """Percent over the limit for 'speed/limit' (0 if not over), or None if invalid."""
    if not isinstance(reading, str):
        return None
    parts = reading.split('/')
    if len(parts) != 2:
        return None
    speed = _to_int(parts[0], max_digits=4)
    limit = _to_int(parts[1], max_digits=4)
    if speed is None or limit is None or limit == 0:
        return None
    if speed <= limit:
        return 0
    return (speed - limit) * 100 // limit


def main():
    print("==== Running parse_ticket_id ====")
    user_input = input("Enter a ticket ID (e.g. TF-2024-0456): ")
    result = parse_ticket_id(user_input)
    if result is None:
        print("Invalid ticket ID. Expected PREFIX-YYYY-SERIAL, e.g. TF-2024-0456")
    else:
        print("Ticket Prefix, Year and Serial:", result)

    print("\n==== Running total_fines ====")
    user_input = input("Enter fine amounts as CSV (e.g. 500,1200,300): ")
    result = total_fines(user_input)
    if result is None:
        print("Invalid fine amounts. Enter non-negative whole numbers separated by commas")
    else:
        print("Total Fines:", result)

    print("\n==== Running speed_excess ====")
    user_input = input("Enter speed/limit (e.g. 72/60): ")
    result = speed_excess(user_input)
    if result is None:
        print("Invalid reading. Enter speed/limit as whole numbers with limit > 0, e.g. 72/60")
    else:
        print("Percent Over Limit:", result)


if __name__ == "__main__":
    main()
