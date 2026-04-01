
"""
Dummy file. Used to test different functions outside of the test suite.
"""

from blackjack.card import Card
from blackjack.helper import get_hand_value, get_soft_value, is_soft, is_win

def main():
    seed = [Card('Spades', 5), Card('Hearts', 'King'), Card('Spades', 8), Card('Clubs', 'Ace')]
    a, b, c = [], [], []
    
    for i in range(len(seed)): # Ensures the deal order is P->D->P->D
        if i % 2 == 0:
            a.append(seed[i])
        elif i % 2 == 1:
            b.append(seed[i])	 
    c.append(a)
    c.append(b)

    """Player Hand Output"""
    for i in range(len(c)):
        if is_soft(c[i]) and not is_win(c[i]):
            print('\nPlayer Hand: ' + str(get_soft_value(c[i])) 
                + ' / ' + str(get_hand_value(c[i])) + '\n')
        else:
            print('\nPlayer Hand: ' + str(get_hand_value(c[i])) + '\n')
        for card in c[i]:
            print(card.to_string())
        print('\n--------------------')

    # for item in temp:
    #     print(item)
    # for item in my_list:
    #     print(item)

if __name__ == '__main__':
    main()
