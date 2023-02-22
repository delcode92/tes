import json

def calculate_parking_payment(parking_hours):
    total_payment = 0
    base_price = 2000
    max_flat_price = 6000
    
    # Define the rates and the maximum hours for each rate
    
    # init list
    price_increase = []
    
    # get rules from DB
    rules = json.loads('{"4":"1000", "6":"1000", "24":"6000"}')

    # add rules to list
    for k, v in rules.items():
        price_increase.append( (k,v) )
    
    # price_increase = [
    #     (4, 1000),
    #     (6, 1000),
    
            
    #     (24, 6000)
    # ]

    # get price now
    for i in range(len(price_increase)):
        rate_hours, rate_price = price_increase[i]

        rate_hours = int(rate_hours)
        rate_price = int(rate_price)

        if parking_hours < rate_hours:
            # get index now
            # then loop price increase before this index position
            # add each loop  price 
            
            # print("lesser", i)
            # print("PH", parking_hours, "RH", rate_hours)

            each_loop_price = 0
            for j in range(i):
                rh, rp = price_increase[j]
                rh = int(rh)
                rp = int(rp)

                each_loop_price += rp

            total_payment = base_price + each_loop_price
            break

        # elif parking_hours == rate_hours:
        #     # get index now
        #     # then loop price increase before this index position
        #     # add each loop  price + price now
        #     print("same")
        #     if parking_hours != 24:
        #         each_loop_price = 0
        #         for j in range(i):
        #             rh, rp = price_increase[j]

        #             each_loop_price += rp

        #         total_payment = base_price + each_loop_price + rate_price

        elif parking_hours >= 24:
            total_payment = (parking_hours // 24) * max_flat_price
            
    return total_payment

print("\n\n============ 12 hours ================")
print( calculate_parking_payment(12) )

# print("\n\n============ 4 hours ================")
# print( calculate_parking_payment(4) )

# print("\n\n============ 5 hours ================")
# print( calculate_parking_payment(5) )

# print("\n\n============ 6 hours ================")
# print( calculate_parking_payment(6) )

# print("\n\n============ 8 hours ================")
# print( calculate_parking_payment(8) )

# print("\n\n============ 24 hours ================")
# print( calculate_parking_payment(24) )