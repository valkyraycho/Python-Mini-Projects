with open(r'C:\Users\razor\Desktop\Python\Project Practice\Mini Projects\Madlibs Generator Story\Madlibs Generator Story.txt', 'r') as f:
    story = f.read()
    
words = set()
start_of_words = -1
end_of_words = -1

target_start = '<'
target_end = '>'
  
for i, char in enumerate(story):
    if char == target_start:
        start_of_words = i
    
    if char == target_end and start_of_words != -1:
        end_of_words = i
        word = story[start_of_words: end_of_words + 1]
        words.add(word)

answers = {}

for word in words:
    answer = input(f"Enter a word for {word}: ")
    answers[word] = answer
    
for word in words:
    story = story.replace(word, answers[word])
    
print(story)