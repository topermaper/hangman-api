from random import choice
from app.models.game import Game
from app import app

class Hangman(Game):

    def __init__(self, user_id):
        super().__init__(user_id)

    # Main method, new_user_guess.
    def set_user_guess(self, user_guess):
        if user_guess == None:
            raise Exception("The user guess character is empty.")

        if user_guess in self.user_guess:
            raise Exception("The user guess character has already been used.")
    
        # Guess is valid, add guess character
       
        self.user_guess += user_guess

        if user_guess not in self.secret_word:
            self.misses += 1
            self.update_user_score(False)
        else:
            self.update_user_score(True)
 
        # Update the game status
        self.update_game_status()

        return True

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
