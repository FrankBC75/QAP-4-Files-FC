#  Program to enter, update and calculate insurance policy information for its customers.
#  Author: Frank Corcoran
#  Date: March 18/23

import math
import time
import datetime
from tqdm import tqdm

import datetime

# Read default values from file
f = open('OSICDef.dat', 'r')
next_policy_number = int(f.readline())
basic_rate = float(f.readline())
discount_rate = float(f.readline())
liability = float(f.readline())
glass_coverage = float(f.readline())
loaner_cost = float(f.readline())
hst_rate = float(f.readline())
processing_fee = float(f.readline())

f.close()

# Initialize variables
policy_number = next_policy_number
total_sales = [0] * 12  # a list of 12 zeros, one for each month
provinces = ['NL', 'PE', 'NS', 'NB', 'QC', 'ON', 'MB', 'SK', 'AB', 'BC', 'YT', 'NT', 'NU']

# Loop to enter policies
while True:

    # Input customer information
    first_name = input("Enter customer's first name (or type END to exit):      ").title()
    if first_name.upper() == "END":
        break
    last_name = input("Enter customer's last name:                             ").title()
    address = input("Enter customer's address:                               ")
    city = input("Enter customer's city:                                  ").title()
    province = input("Enter customer's province (use 2-letter code):          ").upper()

    while province not in provinces:
        province = input("Invalid province, please enter a valid 2-letter code:   ").upper()
    postal_code = input("Enter customer's postal code:                           ")
    phone_number = input("Enter customer's phone number:                          ")
    num_cars = int(input("Enter number of cars to insure:                         "))
    liability = input("Extra liability coverage? (Y/N):                        ").upper() == 'Y'
    glass_coverage = input("Glass coverage? (Y/N):                                  ").upper() == 'Y'
    loaner_car = input("Loaner car coverage? (Y/N):                             ").upper() == 'Y'
    payment_method = input("Payment method? (F/M):                                  ").upper()

    # Calculate premium
    discount_factor = discount_rate ** max(num_cars - 1, 0)
    premium = basic_rate * discount_factor * num_cars

    #  Calculations

    total_extra_cost = (num_cars - 1) * basic_rate * discount_rate

    if liability == "Y":
        total_extra_cost = liability * num_cars

    if glass_coverage == "Y":
        total_extra_cost = num_cars * glass_coverage

    if loaner_car == "Y":
        total_extra_cost = num_cars * loaner_cost

    total_premium = basic_rate + total_extra_cost
    hst = total_premium * hst_rate
    total_cost = total_premium + hst

    if payment_method == "M":
        total_cost = total_cost / 8 + processing_fee
    monthly_payment = (total_cost + basic_rate) / 8

    total_premium = basic_rate + total_extra_cost
    hst = total_premium * hst_rate
    total_cost = total_premium + hst

    # Add processing fee to total cost
    total_cost = total_cost + processing_fee

    # Calculate the monthly payment
    monthly_payment = total_cost / 8

    # Determine the invoice date (current date)
    invoice_date = datetime.date.today()

    # Get the current date
    current_date = datetime.date.today()

    # Set the invoice date to the current date
    invoice_date = current_date

    # Set the next payment date to the first day of the next month
    if current_date.month == 12:
        next_payment_date = datetime.date(current_date.year + 1, 1, 1)
    else:
        next_payment_date = datetime.date(current_date.year, current_date.month + 1, 1)
    if payment_method == "M":
        monthly_payment = (total_cost + processing_fee) / 8
        next_payment_date = datetime.date.today().replace(day=1, month=datetime.date.today().month + 1)
        invoice_date = datetime.date.today()
    else:
        monthly_payment = None
        next_payment_date = None
        invoice_date = datetime.date.today()

    print()
    # Processing bar
    for _ in tqdm(range(20), desc="Processing", unit="ticks", ncols=30, bar_format="{desc}  {bar}"):
        time.sleep(.1)

    print()

    print("Policy information processed and saved")

    print()

    # Print receipt
    print("=" * 65)
    print(f"{'One Stop Insurance Company'}               Invoice Date: {invoice_date.strftime('%Y-%m-%d').ljust(30)}")
    print("=" * 65)
    print(f"Policy number:                                     {policy_number:}")
    print(f"Customer name:                                     {first_name} {last_name}")
    print(f"Street address:                                    {address:<23s}")
    print(f"City:                                              {city}")
    print(f"Province:                                          {province}")
    print(f"Postal code:                                       {postal_code}")
    print(f"Phone number:                                      {phone_number}")
    print(f"Number of cars:                                    {num_cars}")
    print(f"Extra liability coverage:                          {liability}")
    print(f"Glass coverage:                                    {glass_coverage}")
    print(f"Loaner car coverage:                               {loaner_car}")
    print(f"Payment method:                                    {'Full' if payment_method == 'F' else 'Monthly'}")
    print(f"Total cost:                                        ${total_cost:.2f}")
    print(f"HST:                                               ${hst:.2f}")
    print("=" * 65)
    if monthly_payment:
        print(f"Monthly Payment:                                   ${monthly_payment:.2f}")
        print(f"Next Payment Date:                                 {next_payment_date}")
    print("=" * 65)
    print("        Thank you for choosing One Stop Insurance Company")
    print("=" * 65)

    # Write files to Policies,dat
    f = open("Policies.dat", "a")
    f.write("{}, ".format(int(policy_number)))
    f.write("{}, ".format(str(first_name)))
    f.write("{}, ".format(str(last_name)))
    f.write("{}, ".format(str(address)))
    f.write("{}, ".format(str(city)))
    f.write("{}, ".format(str(province)))
    f.write("{}, ".format(str(postal_code)))
    f.write("{}, ".format(str(phone_number)))
    f.write("{}, ".format(str(num_cars)))
    f.write("{}, ".format(str(liability)))
    f.write("{}, ".format(str(glass_coverage)))
    f.write("{}, ".format(str(loaner_car)))
    f.write("{}, ".format(str(payment_method)))
    f.write("{}\n".format(str(total_premium)))

    f.close()

    print()

    print()

    # Increment policy number
    policy_number += 1

#  Write back to OSICDef.dat
f = open("OSICDef.dat", "w")
f.write("{}\n ".format(int(policy_number)))
f.write("{}\n ".format(str(basic_rate)))
f.write("{}\n ".format(str(discount_rate)))
f.write("{}\n ".format(str(liability)))
f.write("{}\n ".format(str(glass_coverage)))
f.write("{}\n ".format(str(loaner_cost)))
f.write("{}\n ".format(str(hst_rate)))
f.write("{}\n ".format(str(processing_fee)))

f.close()

print()

import matplotlib.pyplot as plt

# Create a list of months and initialize sales data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
sales = []

# Prompt user to enter sales data for each month
for month in months:
    sale = float(input(f"Enter sales for {month}: "))
    sales.append(sale)

# Plot sales data as a bar graph
plt.bar(months, sales)

# Add labels and title to graph
plt.xlabel("Month")
plt.ylabel("Total Sales ($)")
plt.title("Total Sales by Month")
print()
for _ in tqdm(range(20), desc="Processing", unit="ticks", ncols=30, bar_format="{desc}  {bar}"):
    time.sleep(.1)

# Show the graph
plt.show()
