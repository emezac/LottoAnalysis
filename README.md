# LottoAnalysis
I have always had a sneaking suspicion that there is an optimum number of lottery tickets to buy such that minor wins consistently cover the ticket prices. I analyzed historical data for the South African Lottery to find out. 

This code pulls data from the 51 most recent lottery results from www.lottonumbers.com. Then, we choose random numbers for tickets and see how much we would have won. This code will run 30 hypothetical scenarios, wherein we buy 1, 2, 3, ..., up to 30 tickets for each draw (each with unique random numbers), and then see how many of those ticket would have won money.

The results are plotted on a bar plot (see below) and indicate that, within a certain margin, buying a greater number of tickets for a  draw will result in losing more money. Running the code again will yield a different number set (due to random numbers being selected for each draw). It is noteworthy that, sometimes, a moderate number of small wins will offset the cost of the tickets. However, as the number of tickets bought (and thus the cost) increases, the likelihood of this happening decreases. Repeatedly running this model shows that, with a few lucky exceptions, only scenarios that even came close to having an overall positive profit were those with a relatively small amount of money spent on tickets

Thus, if one does play the lottery, one should see this money as part of one's entertainment budget - and thus not a loss so much as a price paid for an entertainment experience. If one wanted to maximize any chance of winning anything, then it is best to keep the number of purchased tickets small. Say, less than 5.

![Lotto results plot](https://raw.githubusercontent.com/MProx/LottoAnalysis/master/Figure_1.png)

Some notes and caveats:
1. Note that, because of the summing up of ticket sales, running the code once simulates 1 + 2 + 3 + ... + 29 + 30 =  465 ticket sales. 

2. Hypothetically, a winning ticket could be "drawn" in this model. In all the times I have run it (many dozens now), I have never seen a jackpot win - which is encouraging, cnsidering the statatics. 

3. The numbers are calculated based on the following assumptions: games were kept simple - only six balls drawn and six chosen by the player. No bonus balls or any of the fancy "+1" or "+2" games were considered. I may eventually build this into the model.

4. All tickets cost the same (R5). Real-life winnings depend on how many other people also won that draw, but an estimate based on past history is available [here](https://www.lotteryresults.co.za/lotto/):
* Two winning numbers: R20 (guaranteed payout)
* Three winning numbers: R50 (guaranteed payout)
* Four winning numbers: R242
* Five winning numbers: R7,276
* Six winning numbers: R5,994,241
