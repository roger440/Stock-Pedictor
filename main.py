import copy

from data_manipulation_functions import normalise_data, get_data, prepare_data_for_predicting_price_considering_only_time,get_real_price_based_on_date,eliminate_unneccesary_fields_of_data
from validations import *
from matplotlib import pyplot as plt
def get_value_of_function(sample,slopes,intercept):
    #sample is a line of numbers read from file (ignoring the last one, the result), slopes are the a,b,c... parameters
    result=float(0)

    for i in range(0,len(sample)-1,1):
        result=result+sample[i]*slopes[i]

    result=result+intercept
    return result



def get_nth_slope_derivate(data,current_slopes,current_intercept,index):
    #we consider the function to be in this form : ax + by + cz +......
    #where x,y,z are considered inputs, and a,b,c are the slopes we shall compute
    #this function returns the partial derivative for the n'th parameter(a,b,c...)
    #index specifies the current parameter (a is 1, b is 2...)
    derivate=float(0)
    for sample in data:
        current_function_value = get_value_of_function(sample, current_slopes, current_intercept)
        derivate=derivate+(-2*sample[index])*(sample[len(sample)-1] - current_function_value)

    return derivate


def get_minimum_price(data):
    #initialising it with the first price
    minimum_price=data[0][len(data[0])-1]
    for sample in data:
        if sample[len(sample)-1]< minimum_price:
            minimum_price=sample[len(sample)-1]
    return minimum_price





def get_intercept_derivative(data,current_slopes,current_intercept):
    derivate=float(0)
    for sample in data:
        current_function_value = get_value_of_function(sample, current_slopes, current_intercept)
        derivate = derivate + (-2 ) * (sample[len(sample) - 1] - current_function_value)

    return derivate

def get_sum_of_squared_residuals(data,current_slopes,current_intercept):
    sum=float(0)
    for sample in data:
        sum=sum+(sample[len(sample)-1]-get_value_of_function(sample,current_slopes,current_intercept))*(sample[len(sample)-1]-get_value_of_function(sample,current_slopes,current_intercept))

    return sum

def get_total_squares(data):
    sum=float(0)
    average=float(0)
    for sample in data:
        average=average+sample[len(sample)-1]
    average=average/len(data)
    for sample in data:
        sum=sum+(sample[len(sample)-1]-average)*(sample[len(sample)-1]-average)

    return sum

def print_results(data,slopes,intercept,current_attempts):
    print("best parameters found: slopes:",end="")
    print(slopes)
    print("intercept: ",end="")
    print(intercept)
    print("result obtained after "+str(current_attempts)+" trials")
    print("final least squares: ",end="")
    least_sq=get_sum_of_squared_residuals(data,slopes,intercept)

    print(least_sq)
    print("R^2 coefficient: ",end="")
    total_sq=get_total_squares(data)
    print(1-(least_sq/total_sq))

def allow_user_to_predict_prices(current_slope,current_intercept,minimum_value):
    ##this is the function which tries to estimate prices based on data consisting of time and price
    current_slope=current_slope[0]
    while True:
        print("Enter the day index for which you are interested, or -1 to go back")
        command=int(input())
        if(command==-1):
            return
        else:
            price=float()
            price=price+current_slope*command
            price=price+current_intercept
            price=price+minimum_value
            print(str(price)+"$")

def custom_allow_user_to_predict_prices(current_slopes,current_intercept):
    #this is the function which tries to estimate prices based on custom data
    #current slopes and current intercept are the estimated parameters
    #input_slope is the data the user is trying to get a prediction for
    while True:
        price=float(0)
        print("The training data contains " + str(len(current_slopes)) + " parameters")
        print("Enter the parameters for which to run the prediction one by one, and press enter after each one of them")
        for i in range(0,len(current_slopes),1):
            input_slope=int(input())
            price=price+input_slope*current_slopes[i]
        price=price+current_intercept
        print(str(price) + "$")
        print("Enter 1 if you want to continue, or 0 to exit")
        option=int(input())
        if(option==0):
            return





def estimate_price(training_data,run_mode):
    #the alforithm  is gonna compute parameters for the function which determines the price
    #if we prepare data taking only time into consideration (prepare_data_for_predicting_price_considering_only_time()) we obtain a slope and a intercept
    #prepare_data_for_predicting_price_considering_only_time()

    unproccesed_data= get_data(training_data)
    data_copy=copy.deepcopy(unproccesed_data)
    min_price=get_minimum_price(unproccesed_data)
    if(run_mode=="command2_mode"):
        data=normalise_data(unproccesed_data,min_price)
    else:
        data=unproccesed_data
    #now in data we have the prices minus the minimum overall price

    number_of_params=len(data[0])-1
    current_slopes=[]

    #-2 is the worst i assume for the parameters of the function, the value could be changes as needed
    worst_assumption=float(-2)

    current_intercept=worst_assumption
    #we ll start with all slopes being 0, the intercept also being 0 and keep increasing them depending on the value of the drivative
    for i in range(0,number_of_params,1):
        current_slopes.append(worst_assumption)

    #we execute the algorithm maximum 1000 times, for each 10 we compute the residual value and we compare it with the former residual
    #if the difference is less than a hardcoded threshhold , we stop the algorithm, and print the number of trials after which we obtained this result
    improvement_threshhold=0.001
    #this is the percent the improvement must exceed relative to the old residual in order for the algorithm to continue
    check_interval=10
    former_residual=get_sum_of_squared_residuals(data,current_slopes,current_intercept)
    max_trials=100000
    current_attempts=0
    learning_rates=[0.0000001,0.00000000001]
    # we need separate learning rates for custom parameters. These are set so that the experiment works reasonably

    while(current_attempts < max_trials):

        for i in range(0,len(current_slopes),1):
            #we update the slopes according to the derivatives and the learning rate
            slope_derivate=get_nth_slope_derivate(data,current_slopes,current_intercept,i)
            current_slopes[i]=current_slopes[i]-slope_derivate*learning_rates[i]



        #we update the intercept

        intercept_derivate=get_intercept_derivative(data,current_slopes,current_intercept)
        current_intercept=current_intercept-intercept_derivate*learning_rates[0]

        current_attempts=current_attempts+1

        # we check for the stopping condition, the improvement being insignificant
        actual_residual=get_sum_of_squared_residuals(data,current_slopes,current_intercept)
        if(current_attempts % check_interval ==0):
            improvement=former_residual-actual_residual
            percent_of_improvement=float(100)*improvement/former_residual
            if(percent_of_improvement < improvement_threshhold):
                break
            else:
                former_residual=actual_residual

    print_results(data,current_slopes,current_intercept,current_attempts)
    if(run_mode=="command2_mode"):
        #we plot the data to a graph
        real_time=[]
        real_price=[]
        estimated_price=[]
        plt.title("Blue line represents actual data, orange line represents the estimate")
        plt.ylabel('price in $')
        plt.xlabel('days past 12/02/2019')
        for sample in data_copy:
            real_time.append(sample[0])
            real_price.append(sample[1])
            estimated_price.append(get_value_of_function(sample,current_slopes,current_intercept)+min_price)
        plt.plot(real_time,real_price)
        plt.plot(real_time, estimated_price)
        plt.show()


        allow_user_to_predict_prices(current_slopes,current_intercept,min_price)
    else:
        custom_allow_user_to_predict_prices(current_slopes,current_intercept)

def print_main_menu():
    print("1. Get the price for a specific date (month/day/year)")
    print("2. Estimate price based on data containing time and price")
    print("3. Estimate price based on custom parameters")
    print("0. Exit")
    print("Please enter your command: ")

def print_prices_for_specific_day():
    while True:
        date = ""
        month = input("Enter the month (ex: 05) : ")
        validate_month(month)
        month = month + "/"

        day = input("Enter the day (ex: 09) : ")
        validate_day(day)
        day = day + "/"

        year = input("Enter the year: ")
        validate_year(year)

        date = date + month
        date = date + day
        date = date + year
        date = date + ","
        price = get_real_price_based_on_date(date)
        print(price[:-1])
        print("Enter 1 to continue getting prices or 0 to go back ")
        option=int(input())
        if(option==0):
            return

def estimate_price_based_on_custom_parameters():
    print("The file must contain rows of data separated by space, the last column is supposed to be the result(price)")
    print("Enter the filename from which to use the data. The experiment file can be used in this regard")
    filename=input()
    estimate_price(filename,"command3_mode")

def main():

    #in order to estimate prices for options 2 and 3, the algorithm uses gradient descent
    while(True):
        print_main_menu()
        command=int(input())
        if command==1:
            print_prices_for_specific_day()
        elif command ==2:
            estimate_price("amazon.txt","command2_mode")
        elif command==3:
            estimate_price_based_on_custom_parameters()
        elif command==0:
            return
        else:
            raise RuntimeError("Invalid command!")

main()


