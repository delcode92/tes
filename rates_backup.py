import json


def calculate_parking_payment(parking_seconds=0):
    tolerance = 10*60 # in seconds
    
    if parking_seconds > tolerance:
        total_payment = 0
        base_price = 2000
        max_flat_price = 6000
        
        # Define the rates and the maximum hours for each rate
        
        # init list
        price_increase = []
        
        # get rules from DB
        rules = json.loads('{ "2":"2000", "4":"1000", "6":"1000", "24":"6000" }')

        # add rules to list
        for k, v in rules.items():
            price_increase.append( (k,v) )
        
        # get price now
        for i in range(len(price_increase)):
            rate_hours, rate_price = price_increase[i]

            rate_seconds = int(rate_hours) * 3600
            rate_price = int(rate_price)

            if parking_seconds <= rate_seconds:
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

            elif parking_seconds > (24*3600):
                # get how many days
                day_in_seconds = parking_seconds // (24*3600) 
                total_payment = day_in_seconds * max_flat_price
                
                # get remaining time in second
                remaining_time = parking_seconds - day_in_seconds
                
                # run recursive funct --> get payment result
                # sum total payment before + recursive payment result
                total_payment = total_payment + calculate_parking_payment(remaining_time)
            
            elif parking_seconds == (24*3600):
                total_payment = (parking_seconds // (24*3600)) * max_flat_price
                
        return total_payment

p1 = 2000 # > 10 menit , <= 2 jam pertama
p2 = 3000 # <= 4 jam berikutnya
p3 = 4000 # <= 6jam berikutnya
p4 = 6000 # 24 jam
p5 = 8000 # 24 jam + <= 2 jam
p6 = 4000 # <24 jam , > 6 jam


assert p1 == calculate_parking_payment(parking_seconds=(10*60))
assert p1 == calculate_parking_payment(parking_seconds=(2*60*60))
assert p2 == calculate_parking_payment(parking_seconds=(3*60*60)), 'should be 3000'

assert p3 == calculate_parking_payment(parking_seconds=(5*60*60)), 'should be 4000'
assert p4 == calculate_parking_payment(parking_seconds=(24*60*60)), 'should be 6000'
assert p5 == calculate_parking_payment(parking_seconds=(24*60*60)+(1*60*60)), 'should be 8000'
assert p6 == calculate_parking_payment(parking_seconds=(7*60*60)), 'should be 4000'


# print("\n\n============ 10 minutes ================")
# print( calculate_parking_payment(10*60) )

# print("\n\n============ 2 hours ================")
# print( calculate_parking_payment(2*60*60) )

# print("\n\n============ 3 hours ================")
# print( calculate_parking_payment(3*60*60) )

# print("\n\n============ 6 hours ================")
# print( calculate_parking_payment(6) )

# print("\n\n============ 8 hours ================")
# print( calculate_parking_payment(8) )

# print("\n\n============ 24 hours ================")
# print( calculate_parking_payment(24) )