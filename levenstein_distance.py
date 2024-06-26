import streamlit as st
import os


def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = sorted(set([line.strip().lower() for line in lines]))
    return words


VOCAB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'vocab.txt')
vocabs = load_vocab(VOCAB_PATH)


def levenshtein_distance(first_word, second_word):
    rows = len(first_word) + 1
    cols = len(second_word) + 1
    distance_matrix = [[0] * cols for _ in range(rows)]

    for i in range(1, rows):
        distance_matrix[i][0] = i

    for j in range(1, cols):
        distance_matrix[0][j] = j

    for i in range(1, rows):
        for j in range(1, cols):
            if first_word[i - 1] == second_word[j - 1]:
                distance_matrix[i][j] = distance_matrix[i - 1][j - 1]
            else:
                deletion = distance_matrix[i - 1][j] + 1
                insertion = distance_matrix[i][j - 1] + 1
                substitution = distance_matrix[i - 1][j - 1] + 1
                distance_matrix[i][j] = min(deletion, insertion, substitution)

    return distance_matrix[rows - 1][cols - 1]


def main():
    st.title("Word Correction using Levenshtein Distance")
    word = st.text_input('Word:')

    if st.button("Compute"):
        # compute levenshtein distance
        leven_distances = dict()
        for vocab in vocabs:
            leven_distances[vocab] = levenshtein_distance(word, vocab)

        # sorted by distance
        sorted_distences = dict(
            sorted(leven_distances.items(), key=lambda item: item[1]))
        correct_word = list(sorted_distences.keys())[0]
        st.write('Correct word: ', correct_word)

        col1, col2 = st.columns(2)
        col1.write('Vocabulary:')
        col1.write(vocabs)

        col2.write('Distances:')
        col2.write(sorted_distences)


if __name__ == "__main__":
    main()
