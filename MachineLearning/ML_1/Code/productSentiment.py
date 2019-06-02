word_counts = {'and': 3,  'bags': 1,  'came': 1,  'disappointed.': 1,
            'does': 1,  'early': 1,  'highly': 1,  'holder.': 1,
            'i': 1,  'it': 2,  'it.': 1,  'keps': 1,
            'leak.': 1, 'love': 1, 'moist': 1, 'my': 2,
            'not': 2, 'now': 1, 'osocozy': 1, 'planet': 1,
            'recommend': 1, 'was': 1, 'wipe': 1, 'wipes': 1,
            'wise': 1, 'awesome': 93}

def count_word(word, word_count_dict):
    if word in word_count_dict:
        return word_count_dict[word]
    else:
        return 0

selected_words = ['awesome', 'great', 'fantastic', 'amazing', 'love', 'horrible',
                  'bad', 'terrible', 'awful', 'wow', 'hate']


for word in selected_words:
    print word, 'count:', count_word(word, word_counts)
