import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
             'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self,suit,rank):
        
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    def __str__(self):
        
        return self.rank + ' of ' + self.suit
class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        
        for suit in suits:
            for rank in ranks:
                
                self.deck.append(Card(suit,rank))

#                 new_card = Card(suit,rank)
#                 self.deck.append(new_card)

    
    def __str__(self):
        num = len(self.deck)
        return f'The deck currently has {num} cards and the top card is {self.deck[0]}'

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += card.value
    
    def adjust_for_ace(self,card):
        # if card.suit == "Ace":
        if self.value <= 21:
            card.value = 11
        else:
            self.value -= 10
class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self,bet):
        self.total += self.bet
        return self.total
    
    def lose_bet(self,bet):
        self.total -= self.bet
        return self.total

### Additional functions ###

def take_bet():
    bet_on = True
    while bet_on:
        try:
            bet = int(input('Place your bet! '))
        except:
            print('Invalid bet!')
            continue
        else:
            if bet <= player_chips.total:
                print(f'Your bet is {bet}! Best of luck!')
                bet_on = False
                return bet
            else:
                print('Invalid bet! Not enough chips!')
                continue

def hit(deck,hand):
    new_card = deck.deal()
    hand.add_card(new_card)
    if new_card.rank == 'Ace':
        hand.adjust_for_ace(new_card)
    print(new_card)
    # print(new_card.value)

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop

    choice = input('Hit or Stand? ')
    if choice.capitalize() == 'Hit':
        hit(deck,hand)
        # print(hand.value)
    elif choice.capitalize() == 'Stand':
        # print(hand.value)
        playing = False
    else:
        print('Invalid response!')

def show_some(player,dealer):
    print("THE PLAYER'S HAND: ")
    for x in range(len(player)):
        print(f'{player[x]}')
    print("THE DEALER'S HAND: a hidden card and ")
    for x in range(1,len(dealer),1):
        print(f'{dealer[x]}')
    
def show_all(player,dealer):
    print("THE PLAYER'S HAND: ")
    for x in range(len(player)):
        print(f'{player[x]}')
    print("THE DEALER'S HAND: ")
    for x in range(len(dealer)):
        print(f'{dealer[x]}')

def player_busts(chips):
    lose = chips.lose_bet(chips)
    print(f'Sorry, that is a bust! You lose! Your current total is {lose} chips.')
    return lose

def player_wins(bet,chips):
    win = chips.win_bet(chips)
    print(f'You Win! Your winnings are {bet*2} chips!')
    return win

def dealer_busts(bet,chips):
    win = chips.win_bet(chips)
    print(f'Dealer Bust! You Win! Your winnings are {bet*2}!')
    return win

def dealer_wins(chips):
    lose = chips.lose_bet(chips)
    print(f'Sorry, Dealer wins! You lose. Your current total is {lose} chips.')
    return lose
    
def push(chips):
    lose = chips.lose_bet(chips)
    print(f'Sorry, tie, Dealer Pushes! Dealer wins! You lose. Your current total is {lose} chips.')
    return lose

### Game execution ###
game_count = 0
game_on = True
while game_on:
    # Opening statement
    print('Welcome to BlackJack! Best of luck!')

    # Create & shuffle the deck, deal two cards to each player
    new_deck = Deck()
    new_deck.shuffle()
    dealer_hand = Hand()
    player_hand = Hand()
    for x in range(2):
        dealer_hand.add_card(new_deck.deal())
        player_hand.add_card(new_deck.deal())
        
    # Player's chips
    # print(game_count)
    if game_count == 0:
        game_count += 1
        # print(game_count)
        player_chips = Chips()
        
    print(f'You have {player_chips.total} chips.')
    
    # Player bet
    player_bet = take_bet()
    player_chips.bet = player_bet
    
    # Show cards with one dealer card hidden
    show_some(player_hand.cards,dealer_hand.cards)
#     print(player_hand.value)

    
    while playing:  #from hit_or_stand function
        
        #Player to Hit or Stand
        hit_or_stand(new_deck,player_hand)
        
        # Show cards
        show_some(player_hand.cards,dealer_hand.cards)
 
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            balance = player_busts(player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    # Dealer's turn
    while dealer_hand.value <= 21 and dealer_hand.value < player_hand.value and player_hand.value <= 21:
        # Show all cards
        show_all(player_hand.cards,dealer_hand.cards)
        hit(new_deck,dealer_hand)
        if dealer_hand.value == player_hand.value:
            break
        # print(dealer_hand.value)
    
    # All other end game scenarios
    if player_hand.value > dealer_hand.value and player_hand.value <= 21:
        balance = player_wins(player_bet,player_chips)   
    elif dealer_hand.value > 21:
        balance = dealer_busts(player_bet,player_chips)
    elif dealer_hand.value > player_hand.value and dealer_hand.value <= 21:
        balance = dealer_wins(player_chips)
    elif dealer_hand.value == player_hand.value:
        balance = push(player_chips)
    
    # Chips total 
#     player_chips.total = balance
    print(f'Your current chip total is {balance}.')
    
    # Play again?
    new_game = True
    while new_game == True:
        ans = input('Would you like to play again? (Y or N): ')
        if ans.capitalize() == 'Y':
            new_game = False
            playing = True
            game_on = True
        elif ans.capitalize() == 'N':
            new_game = False
            playing = True
            game_on = False
        else:
            print('Incorrect Input!')
