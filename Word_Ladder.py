from Graph import Graph

def can_link_words(word1, word2):
    difference = 0
    for char1, char2 in zip(word1, word2):
        if char1 != char2:
            difference += 1
        if difference > 1:
            return False
    return difference != 0

#words is a list of valid words
#return a list containing the word ladder
#if not possible return None
def word_ladder(start, end, words):
    word_graph = Graph()
    word_graph += words
    for word1 in words:
        for word2 in words:
            if can_link_words(word1, word2):
                word_graph += (word1, word2)
    return word_graph.get_shortest_path(start, end)

start = "cat"
end = "dog"
words = ["cat", "dog", "bat", "bog", "bag", "bot", "car", "far", "art"]

print(word_ladder(start, end, words))