def get_data(filename):
    #we consider all the numbers of the line except the last one to be input
    data=[]
    with open(filename,"r") as f:
        for line in f:
            elems=[]
            line=line.split()
            for element in line:
                elems.append(float(element))

            data.append(elems)
    return data

def prepare_data_for_predicting_price_considering_only_time():
    #this function reads from the file "raw_data.txt" which contains rows describing stock prices of amazon shares throughout last year
    #it filters out the data and puts into "amazon.txt" only the day and the closing price of the day
    #this specific data is taken from https://www.nasdaq.com/market-activity/stocks/amzn/historical , the one-year data
    #could use data from incoming days to test for variability
    # i will start counting days as following: day 0 is 12/02/2019, any day number can be used as an input to verify the alforithm


    output_file=open("amazon.txt","a")
    current_day=0
    #the "x" of the f(x)=a*x+b, a*x+b being considered the price
    with open("raw_data.txt","r") as f:
        for line in f:
            line=line.split()

            current_price=line[1]
            #we have to procces the current price, it contains the dollar sign and the comma, which we have to remove
            processed_current_price=""
            for i in range(1,len(current_price)-1,1):
                processed_current_price=processed_current_price+current_price[i]

            #now in data_to_put we have day/price pairs, we put them in the file
            data_to_put=(str(current_day)+" "+str(processed_current_price))
            output_file.write(data_to_put)
            output_file.write("\n")
            current_day=current_day+1

    output_file.close()

def normalise_data(data,minimum_price):
    # since we are not working with data from the beginning of the company, i will try to normalise it by substracting the minimum price from all values so that the predictions are relevant
    # otherwise, the algorithm will find a curve which begins from time 0, which is gonna mess up the sum of squared residuals
    #we initialize it with the first price
    for sample in data:
        sample[len(sample)-1]=sample[len(sample)-1]-minimum_price
    return data

def get_real_price_based_on_date(date):
    with open("all_time_data","r") as f:
        for line in f:
            line=line.split()
            if(line[0]==date):
                return line[1]
    return "no data for this date in the file!"

def get_experimental_data():
    #for option 3, custom parameters, the user can try to test the algorithm using day/SP500 closing price/ amazon stock price data
    #there is data for this in the "experiment" file, the first row denotes the index of the day of november 2020, the second denotes the colsing price of SP500 and the third, respective amazon stock price
    data=[]
    with open("experiment","r") as f:
        for line in f:
            elems=[]
            line=line.split()
            for element in line:
                elems.append(float(element))

            data.append(elems)
    return data

def eliminate_unneccesary_fields_of_data():
    g=open("all_time_data","w")
    with open("all_data","r") as f:
        for line in f:
            line=line.split()
            g.write(line[0])
            g.write(" ")
            g.write(line[1])
            g.write("\n")

