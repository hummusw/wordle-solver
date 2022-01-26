from wordle import WordleSolver


def score(guess, hidden):
    hidden = list(hidden)
    out = ['.','.','.','.','.']

    # First find perfect matches
    for pos in range(5):
        if guess[pos] == hidden[pos]:
            out[pos] = 'G'
            hidden[pos] = '#'

    # Then find near matches
    for pos in range(5):
        if out[pos] == '.' and guess[pos] in hidden:
            out[pos] = 'y'
            hidden = list(''.join(hidden).replace(guess[pos], '#', 1))

    return ''.join(out)


class WordleTester:
    testFilename = 'actualwordlewords.txt'

    def __init__(self):
        # Set up solver to try as many words as possible
        self.solver = WordleSolver()
        self.solver.roundMax = len(self.solver.candidateWords)  # increase round limit to maximum
        self.solver.printToConsole = False  # do not print to console

        # Set up set of words to test
        self.testWords = []
        file = open(self.testFilename, 'r')
        while nextLine := file.readline().strip().lower():
            self.testWords.append(nextLine)

        self.turnsUsed = []

    def testAll(self):
        self.turnsUsed = []
        self.gamesLost = 0

        for hidden in self.testWords:
            print(f"Testing word: {hidden}  ", end='')

            # Restart solver
            self.solver.reinitialize()

            # Emulate game
            gamecontinues = True
            while gamecontinues:
                guess = self.solver.getNextGuess()
                self.solver.guessResults(guess, score(guess, hidden))
                gamecontinues = self.solver.advanceRound()

            # Record results
            self.turnsUsed.append(self.solver.roundNum)

            print(f'Finished in {self.solver.roundNum} turns')

        # Print results
        print(f'Completed {len(self.testWords)} games')
        print(f'Average turns/game: {sum(self.turnsUsed)/len(self.turnsUsed)}')

    def showStats(self):
        histogram = {}
        for turns in self.turnsUsed:
            histogram[turns] = histogram.get(turns, 0) + 1

        histmin = min(histogram)
        histmax = max(histogram)
        histheight = max(histogram.items(), key=lambda x: x[1])[1]
        histscale = 60

        for turnlength in range(histmin, histmax + 1):
            print(f'{turnlength:>2} - {histogram[turnlength]:>4}: {"|" * int(histscale * histogram[turnlength] / histheight)}{"." if (histscale * histogram[turnlength] / histheight < 1) and (histogram[turnlength] > 0) else ""}')
