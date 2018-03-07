'''
This code pulls data from the 51 most recent lottery results from www.lottonumbers.com. Then, we choose random numbers for 
tickets and see how much we would have won. This code will run 30 hypothetical scenarios, wherein we buy 1, 2, 3, ..., up 
to 30 tickets for each draw (each with unique random numbers), and then see how many of those ticket would have won money.

The results are plotted on a bar plot and indicate that, within a certain margin, buying a greater number of tickets for a 
draw will result in losing more money. Running the code again will yield a different number set (due to random numbers being
selected for each draw). It is noteworthy that, sometimes, a moderate number of small wins will offset the cost of the tickets. 
However, as the number of tickets bought (and thus the cost) increases, the likelihood of this happening decreases. 
Repeatedly running this model shows that, with a few lucky exceptions, only scenarios that even came close to having a nett 
positive profit were those with a relatively small amount of money spent on tickets

Thus, if one does play the lottery, one should see this money as part of one's entertainment budget - and thus not a loss 
so much as a price paid for an entertainment experience. If one wanted to maximize any chance of winning anything, then it is 
best to keep the number of purchased tickets small. Say, less than 5.
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    MaxTicketsBought = 30

    # Data pulled from website:
    df = pd.read_html('http://www.lottonumbers.com/past-south-africa-lotto-results')
    df = df[0].dropna().drop('Result Date', axis = 1) #remove date column, and any NaN data

    # df = pd.read_csv('example').dropna().drop('Result Date', axis = 1)
    #convert jackpot string to integer (remove commas and "R" indicator):
    for i in range(len(df)):
        df['Jackpot'].iloc[i] = int(df['Jackpot'].iloc[i].replace("R","").replace(",",""))

     #Make dataframe to save the distribution of number of matches per ticket:
     # i.e. 20x tickets with no matching number, 23x with one match, etc...
    Summary = pd.DataFrame(data = np.zeros((MaxTicketsBought, 7)),
                            columns = range(7),
                            index = range(1, MaxTicketsBought+1))

    #We repeat the following code for each scenario - i.e. one ticket bought, two, three, etc:
    for TicketsBought in range(1, MaxTicketsBought+1):
        # Create array of zeros, to be populated with number of wins for each ticket
        # Array has dimensions: (number of tickets bought) X (number of draws played)
        Results = np.zeros(TicketsBought*len(df)).reshape(len(df), TicketsBought)

        # Choose tickets and get results of each draw:
        for draw in range(len(df)): #for each draw

            #parse winning numbers from dataframe:
            DrawNums = df['Numbers'].iloc[draw].split()[:6]

            #choose new numbers:
            MyTickets = np.array([]) #empty numpy array
            while(len(MyTickets) < TicketsBought*6):
                #choose random numbers without repeating:
                nums = np.random.choice(np.arange(1,53),
                                        size = 6,
                                        replace = False)
                MyTickets = np.append(MyTickets, nums) #currently just a list of enough random numbers
            MyTickets = MyTickets.reshape(TicketsBought, 6) #split into tickets (6 numbers each)

            #check if numbers in tickets are winning numbers in any draws:
            for ticket in range(len(MyTickets)): #for each ticket
                for number in MyTickets[ticket]:
                    numstr = str(number).replace('.0', '') #convert float to string an remove decimals
                    if numstr in DrawNums:
                        Results[draw,ticket] += 1
                        if Results[draw,ticket] == 6: #Any jackpot winners?
                            print("")
                            print("We have a winner!")
                            print("Draw numbers:" + str(DrawNums))
                            print("My numbers:" + str(MyTickets[ticket]))
                            print("")

        # We now have a dataframe containing the status of each bought ticket
        # i.e. how many tickets contain numbers that were chosen in a draw, and how many
        # Now, we sum those to get the number of times each number of matches comes up
        # i.e. how many times did a player get a ticket with n matching balls
        for i in range(7):
            count = 0
            for draw in range(len(Results)):
                for j in Results[draw]:
                    if j == i:
                        count += 1;
            Summary[i].loc[TicketsBought] = count

    # #uncomment to run sanity check:
    # #Add a column to Summary that sums all draws entered: (must always be 51):
    # Summary['Check'] = np.zeros(MaxTicketsBought)
    # for i in range(1, MaxTicketsBought+1):
    #     Summary['Check'].iloc[i-1] = Summary.iloc[i-1].sum()/i

    #calculate costs to enter each draw, based on the number of tickets drawn
    costs = np.arange(1, MaxTicketsBought+1, 1)*5*len(df)
    Summary['Costs'] = costs

    #calculate winnings from each draw, for all tickets bought
    # Winnings for each number of matches based on https://www.lotteryresults.co.za/lotto/
    winnings = np.zeros(MaxTicketsBought)
    for i in range(MaxTicketsBought):
        winnings[i] = (Summary[2].iloc[i]*20 +
                       Summary[3].iloc[i]*50 +
                       Summary[4].iloc[i]*242 +
                       Summary[5].iloc[i]*7276 +
                       Summary[6].iloc[i]*5994241)
    Summary['Winnings'] = winnings #add column to summary data frame

    profits = np.zeros(MaxTicketsBought)
    for i in range(MaxTicketsBought):
        profits[i] = Summary['Winnings'].iloc[i] - Summary['Costs'].iloc[i]
    Summary['Profits'] = profits

    plt.style.use('ggplot')
    g = Summary[['Costs', 'Profits']].plot.bar(x = 'Costs',
                                               y = 'Profits',
                                               color = 'purple',
                                               legend = False,
                                               alpha = 0.5)
    g.set_xlabel("Money spent on tickets [R]")
    g.set_ylabel("Profits after costs [R]")
    plt.tight_layout()

    print("Total money paid out: " + str(Summary['Profits'].sum()))
    print("Total tickets in scenario: " + str(MaxTicketsBought*(MaxTicketsBought + 1)/2))

    plt.show()
