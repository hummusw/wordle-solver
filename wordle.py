# allwordsfile = open("linuxwords.txt", "r", newline='\n')
# wordlefile = open("wordlewords.txt", "w")
#
# while word := allwordsfile.readline().strip():
#     print(f'{word} {len(word)}')
#     if len(word) == 5:
#         wordlefile.write(f'{word}\n')

import random

wordlefile = open("wordlewords.txt", "r")
wordstotal = 3264



# Set up variables
green = ['','','','','']
yellow = []

candidatewords = []
for i in range(wordstotal):
    candidatewords.append(wordlefile.readline().strip().lower())

# Generate random hidden word
hiddenwordindex = random.randint(0,wordstotal - 1)
hiddenword = candidatewords[hiddenwordindex]

# Game loop
for round in range(6):
    print(f'Round {round}')

    # Calculate probabilities
    positionfrequencies = [{},{},{},{},{}]
    for word in candidatewords:
        for index in range(5):
            # print(word, index)
            if word[index] not in positionfrequencies[index]:
                positionfrequencies[index][word[index]] = 1
            else:
                positionfrequencies[index][word[index]] += 1
    mostlikely = ''
    for index in range(5):
        maxfrequencycount = 0
        maxfrequencyletter = '#'
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            if positionfrequencies[index].get(letter, 0) > maxfrequencycount:
                maxfrequencycount = positionfrequencies[index][letter]
                maxfrequencyletter = letter
        mostlikely += maxfrequencyletter
    print(f'Optimal guess: {mostlikely}')

    # Guess most similar word
    maxsimilarity = 0
    maxsimilarityword = ''
    for word in candidatewords:
        similarity = 0
        for i in range(5):
            if word[i] == mostlikely[i]:
                similarity += 2
            elif word[i] in mostlikely:
                similarity += 1
        if similarity > maxsimilarity:
            maxsimilarity = similarity
            maxsimilarityword = word

    guess = maxsimilarityword
    print(f'Most similar guess: {guess}')

    # Score guess
    scoreinput = input("Score?")

    score = []
    for index in range(5):
        if scoreinput[index] == '.':
            score.append('grey')
        elif scoreinput[index] == 'G':
            score.append('green')
        elif scoreinput[index] == 'y':
            score.append('yellow')
        else:
            print("UNEXPECTED")
            exit(1)
    print(f'Score: {"".join({"grey":".","green":"G","yellow":"y"}[result] for result in score)}')

    # Check for win
    won = (score == ['green','green','green','green','green'])
    if won:
        print("won\n")
        break

    # Analyze feedback
    newgreen = [(guess[i], i) for i in range(5) if score[i] == 'green']
    newyellow = [(guess[i], i) for i in range(5) if score[i] == 'yellow']

    # Wordle's scoring is different - still need to understand rules better
    for letter, pos in newgreen:
        green[pos] = letter
    newgrey = [(guess[i], i) for i in range(5) if score[i] == 'grey' and guess[i] not in green and guess[i] not in [yellowletter for yellowletter, _ in newyellow]]

    wordsleft = len(candidatewords)
    wordsleftcopy = wordsleft
    i = 0

    # Reevaluate words
    print(f'Reevaluating {wordsleft} words',end='')
    while i < wordsleft:
        print('.', end='')
        candidateword = candidatewords[i]

        if candidateword == guess:
            candidatewords.pop(i)
            wordsleft -= 1
            continue

        # remove words that contain new grey letters
        for letter, pos in newgrey:
            if letter in candidateword:
                candidatewords.pop(i)
                wordsleft -= 1
                break
        else:

            # remove words that don't have new green letters in the right position
            for letter, pos in newgreen:
                if candidateword[pos] != letter:
                    candidatewords.pop(i)
                    wordsleft -= 1
                    break
            else:
                # remove words that have new yellow letters in the incorrect position
                for letter, pos in newyellow:
                    if candidateword[pos] == letter:
                        candidatewords.pop(i)
                        wordsleft -= 1
                        break
                else:
                    # remove words that don't contain any new yellow letters in any position
                    for letter, _ in newyellow:
                        if letter not in candidateword:
                            candidatewords.pop(i)
                            wordsleft -= 1
                            break
                    else:
                        i += 1

    print(f'\nRemoved {wordsleftcopy - wordsleft} words from candidate list, now down to {wordsleft}\n')

if (won):
    print(f"Word was: {guess}")
else:
    print(f"Narrowed it down to: {candidatewords}")
