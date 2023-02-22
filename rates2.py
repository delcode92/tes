import json

def calculate_parking_payment(parking_hours):
    total_payment = 0
    base_price = 2000
    max_flat_price = 6000
    
    # Define the rates and the maximum hours for each rate
    
    # init list
    price_increase = []
    
    # get rules from DB
    rules = json.loads('{"4":"1000", "6":"1000"}')

    # add rules to list
    for k, v in rules.items():
        price_increase.append( (k,v) )
    
    # price_increase = [
    #     (4, 1000),
    #     (6, 1000),
    
            
    # ]

    # get last hours
    last_hours, last_price = price_increase[-1]
    last_hours = int(last_hours)
    last_price = int(last_price)

    # get price now
    if parking_hours >= 24:
            total_payment = (parking_hours // 24) * max_flat_price
    
    elif parking_hours > last_hours:
        each_loop_price = 0
        for j in range(len(price_increase)):
            rh, rp = price_increase[j]
            rh = int(rh)
            rp = int(rp)

            each_loop_price += rp

        total_payment = base_price + each_loop_price

    else:

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

            elif parking_hours == rate_hours:
                print(f"elif {parking_hours} == {rate_hours} or {parking_hours} > {last_hours}:")
                # get index now
                # then loop price increase before this index position
                # add each loop  price + price now
                each_loop_price = 0
                for j in range(i):
                    rh, rp = price_increase[j]
                    rh = int(rh)
                    rp = int(rp)
                    
                    each_loop_price += rp

                total_payment = base_price + each_loop_price + rate_price
                break

            
    return total_payment

print("\n\n============ 6 hours ================")
print( "price:", calculate_parking_payment(6) )

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