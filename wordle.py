class WordleSolver:
    dictionaryFilename = 'actualwordledictionary.txt'
    roundMax = 6

    def __init__(self):
        self.printToConsole = True

        self._initCandidates()
        self.roundNum = 1
        self.won = False

    def _initCandidates(self):
        self.candidateWords = []
        file = open(self.dictionaryFilename, 'r')
        while nextLine := file.readline().strip().lower():
            self.candidateWords.append(nextLine)
        if self.printToConsole:
            self.log(f"Reinitialized {len(self.candidateWords)} candidate words")

    def reinitialize(self):
        self._initCandidates()
        self.roundNum = 1
        self.won = False

    def getNextGuess(self):
        # Calculate frequencies of letters in each position
        frequencies = [{}, {}, {}, {}, {}]
        for word in self.candidateWords:
            for pos in range(5):
                letter = word[pos]
                if letter not in frequencies[pos]:
                    frequencies[pos][letter] = 1
                else:
                    frequencies[pos][letter] += 1

        # Build up word using most frequent letters
        optimal = ''
        for pos in range(5):
            optimal += max(frequencies[pos], key=lambda x: frequencies[pos][x], default='#')
        self.log(f'Optimal guess: {optimal}')

        # Guess most similar word
        guess = max(self.candidateWords, key=lambda candidate: sum([3 if candidate[i] == optimal[i] else 1 if candidate[i] in optimal else 0 for i in range(5)]))
        self.log(f'Most similar guess: {guess}')

        return guess

    def guessResults(self, guess, feedback):
        # Check for correct guess
        if feedback == 'GGGGG':
            self.won = True
            self.log(f"Word was: {guess}")
            return

        # Find new green letters
        green = [(guess[pos], pos) for pos in range(5) if feedback[pos] == 'G']

        # Find new yellow letters
        yellow = [(guess[pos], pos) for pos in range(5) if feedback[pos] == 'y']

        # For each grey letter, find the maximum number of occurrences possible in the hidden word for that letter
        grey = [(guess[pos], pos) for pos in range(5) if feedback[pos] == '.']
        maxoccurences = {letter: 5 if letter not in [x[0] for x in grey] else [x[0] for x in green + yellow].count(letter) for letter in 'abcdefghijklmnopqrstuvwxyz'}

        # Filter out candidate words
        wordsbefore = len(self.candidateWords)
        self.log(f'Reevaluating {wordsbefore} words', end='')
        i = 0
        while i < len(self.candidateWords):
            self.log('.', end='')
            remove = False
            candidate = self.candidateWords[i]

            # If we didn't win, the guess was wrong
            remove |= (candidate == guess)

            # If the word doesn't have green letters in the right position, remove it
            for letter, pos in green:
                remove |= (candidate[pos] != letter)

            # If the word has yellow letters in the guessed (and incorrect) position, remove it
            for letter, pos in yellow:
                remove |= (candidate[pos] == letter)

            # If the word does not contain enough yellow letters, remove it
            for letter, _ in yellow:
                remove |= (candidate.count(letter) < [x[0] for x in yellow].count(letter))

            # If the word contains too many occurences of a letter, remove it
            for letter, freq in maxoccurences.items():
                remove |= (candidate.count(letter) > freq)

            if remove:
                self.candidateWords.remove(candidate)
            else:
                i += 1
        wordsafter = len(self.candidateWords)

        self.log(f'\nRemoved {wordsbefore - wordsafter} words from candidate list, now down to {wordsafter}\n')

    def advanceRound(self):
        """
        Returns True if game continues, and False otherwise (game won or game lost)
        """
        if self.won:
            return False

        self.roundNum += 1

        if self.roundNum > self.roundMax:
            self.log("Game over")
            self.log(f"Narrowed it down to: {self.candidateWords}")
            return False

        if not self.candidateWords:
            self.log("Game over")
            self.log("Word not present in dictionary")
            return False

        return True

    def autoPlay(self):
        for i in range(self.roundMax):
            self.log(f'Round {self.roundNum}')

            guess = self.getNextGuess()
            self.log(f'Guess: {guess}')

            feedback = input('Score: ')
            self.guessResults(guess, feedback)

            self.advanceRound()

            if self.won:
                break

    def log(self, message, end='\n'):
        if self.printToConsole:
            print(message, end=end)


if __name__ == '__main__':
    wordleSolver = WordleSolver()
    wordleSolver.autoPlay()
