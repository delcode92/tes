import json


def calculate_parking_payment(parking_seconds=0):
    tolerance = 10*60 # in seconds
    total_payment = 0

    if parking_seconds >= tolerance:
        # base_price = 2000
        max_flat_price = 6000
        
        # Define the rates and the maximum hours for each rate
        
        # init list
        price_increase = []
        
        # get rules from DB
        # rules = json.loads('{ "2":"2000", "4":"1000", "6":"1000", "24":"6000" }')
        # rules = json.loads('{ "2":"2000", "6":"1000", "12":"1000", "18":"1000", "24":"6000" }')
        rules = json.loads('{ "1":"2000" }')
        
        
        print("rl", len(rules))
        if len(rules) > 1:
            # add rules to list
            for k, v in rules.items():
                price_increase.append( (k,v) )
                # [
                    # (2,2000), 
                    # (4, 1000), 
                    # (6,1000), 
                    # (24,6000)
                # ]
            
            # get price now
            for i in range(len(price_increase)):
                rate_hours, rate_price = price_increase[i]

                rate_seconds = int(rate_hours) * 3600
                rate_price = int(rate_price)

                if parking_seconds <= rate_seconds and parking_seconds != 24*60*60:
                    print("parking seconds", parking_seconds)
                    print("RH: ", rate_hours, "RS: ",rate_seconds)
                    
                    # get index now
                    # then loop price increase before this index position
                    # add each loop  price 
                    
                    # print("lesser", i)
                    # print("PH", parking_hours, "RH", rate_hours)

                    each_loop_price = 0
                    # print("i", i)
                    for j in range(i+1):
                        # print("price_increase: ", price_increase[j])
                        rh, rp = price_increase[j]
                        rh = int(rh)
                        rp = int(rp)
                        
                        each_loop_price += rp

                    # total_payment = base_price + each_loop_price
                    total_payment = each_loop_price

                    print("tot pay:", total_payment)
                    break

                elif parking_seconds > (24*3600):
                    # get how many days
                    days = parking_seconds // (24*3600) 
                    total_payment = days * max_flat_price
                    
                    # get remaining time in second

                    print("parking seconds:", parking_seconds)
                    remaining_time = parking_seconds - (days*24*60*60)
                    
                    # run recursive funct --> get payment result
                    # sum total payment before + recursive payment result
                    print("days:", days)
                    print("remaining time:", remaining_time)

                    total_payment = total_payment + calculate_parking_payment(remaining_time)
                    print("total pay:", total_payment)
                    break

                elif parking_seconds == (24*3600):
                    total_payment = (parking_seconds // (24*3600)) * max_flat_price
        
        elif len(rules) == 1:
            print("masuk")
            print("parking seconds==>", parking_seconds)
            # cari kelipatan jam nya dulu dari json di db
            k = int(next(iter(rules.keys()))) * 3600
            v = int(next(iter(rules.values())))
            
            if parking_seconds > k :
                mod = parking_seconds % k

                if mod==0:
                    h = parking_seconds//k
                elif mod > 0:
                    h = (parking_seconds//k) + 1
                        
                price = h * v

                print("hours==>", h)
                print("price", price)

            elif parking_seconds <= k :
                print("price", v) 

            # kalikan dengan keliptn tersebut
            # jika ada sisa maka genapkan kelipatnnya
            # x = rules.keys()
            # print(*x)
            

            

    return total_payment

p1 = 2000 # > 10 menit , <= 2 jam pertama
p2 = 3000 # <= 4 jam berikutnya
p3 = 4000 # <= 6jam berikutnya
p4 = 6000 # 24 jam
p5 = 8000 # 24 jam + <= 2 jam
p6 = 4000 # <24 jam , > 6 jam


# mobil
# 15:5:55 --> 5.000 ==> 
# 13:31:6 --> 5.000
# 14:3:38 --> 5.000
# 15:15:20 --> 5.000
# 12:1:1 --> 5.000
# 12:0:27 --> 5.000


# 7 Hari, 7:52:9 --> 46.000 ==> 7*6.000 + 4.000

# 1 Hari, 12:42:3 --> 11.000 ==> 6.000 + 5.000 
# 1 Hari, 1:1:54 --> 8.000  ==> 6.000 + 2.000
# 1 Hari, 1:17:55 --> 8.000  ==> 6.000 + 2.000
# 1 Hari, 1:52:3 --> 8.000  ==> 6.000 + 2.000
# 1 Hari, 3:13:30 --> 8.000  ==> 6.000 + 2.000
# 3 Hari, 0:34:51 --> 20.000  ==> 18.000 + 2.000


# calculate_parking_payment( parking_seconds=( 4*60*60 ) )
# calculate_parking_payment( parking_seconds=( (3*24*60*60) + (0*60*60) + (34*60) + 51) )
calculate_parking_payment( parking_seconds=( (3*60*60) + (1*60) + 0) )
# calculate_parking_payment( parking_seconds=(15*60) )

# print((24*60*60) + (12*60*60) + (42*60) + 3)
# print((12*60*60) + (42*60) + 3)

# assert p1 == calculate_parking_payment(parking_seconds=(10*60)), f'should be {p1}'
# assert p1 == calculate_parking_payment(parking_seconds=(2*60*60)), f'should be {p1}'
# assert p2 == calculate_parking_payment(parking_seconds=(3*60*60)), f'should be {p2}'

# assert p3 == calculate_parking_payment(parking_seconds=(5*60*60)), f'should be {p3}'
# assert p4 == calculate_parking_payment(parking_seconds=(24*60*60)), f'should be {p4}'

# # assert p5 == calculate_parking_payment(parking_seconds=(24*60*60)+(1*60*60)), f'should be {p5}'
# assert p6 == calculate_parking_payment(parking_seconds=(7*60*60)), f'should be {p6}'


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