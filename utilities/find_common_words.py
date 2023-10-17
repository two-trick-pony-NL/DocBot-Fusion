from annotated_text import annotated_text


def find_common_words(string1, string2):
    string1 = string1.lower()
    string2 = string2.lower()
    words1 = string1.split()
    words2 = string2.split()

    result = []

    for word1 in words1:
        found = any(word1 in word2 or word2 in word1 for word2 in words2)
        if found and len(word1) > 3:
            result.append((word1, ""))
        else:
            result.append(word1 + " ")

    return annotated_text(result)