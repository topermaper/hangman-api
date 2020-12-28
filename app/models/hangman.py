from random import choice
from app.models.game import Game
from app import app,db
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property


class Hangman(Game):

    def __init__(self, user_id):
        super().__init__(user_id)

    '''
    @orm.reconstructor
    def init_on_load(self):
        print("reconstructor")
        print(self.__dict__)
        self.__user_guess = ""
    
    @hybrid_property
    def user_guess(self):
        print("Hangman getter")
        return self.__user_guess

    @user_guess.setter
    def user_guess(self, user_guess):
        print("Hangman setter")
        self.__user_guess = user_guess
    '''

    def set_user_guess(self, user_guess):

        if len(user_guess) != len(self.user_guess) + 1:
            raise Exception("Invalid user guess")

        for i in range(len(self.user_guess)):
            if user_guess[i] != self.user_guess[i]:
                raise Exception("Invalid user guess")

        if user_guess[-1] in user_guess[:-1]:
            raise Exception("The user guess character has already been used")

        # At this point user_guess is valid
        self.user_guess = user_guess
        
        if user_guess[-1] not in self.secret_word:
            self.misses += 1
            self.update_user_score(False)
        else:
            self.update_user_score(True)
 
        # Update the game status
        self.update_game_status()


    def update_user_score(self,user_guessed):
        # User guessed
        if user_guessed:
            # Add 1 to the score
            self.score += 1
            # Multiply score per multiplier
            self.score = self.score * self.multiplier
            # Increase multiplier
            self.multiplier += 1
        # User did not guess
        else:
            # Reset multiplier
            self.multiplier = 1


    def update_game_status(self):
        # User LOST the game
        if self.misses > app.config['ALLOWED_MISSES']:
            self.status = 'LOST'
        # All the characters in the user guess list, user WON
        elif all(c in self.user_guess for c in self.secret_word):
            self.status = 'WON'
        # Game is still ACTIVE
        else:
            self.status = 'ACTIVE'
