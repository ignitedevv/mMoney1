from django.http import JsonResponse
from django.shortcuts import render
from .forms import MyForm
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from .chat_actions import action_check
from .questions_answers import qa_pairs as qa_pairs
# Define the questions and answers as a dictionary


# Initialize the NLTK components
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")
stop_words = set('')
stop_words.update(["?"])
lemmatizer = WordNetLemmatizer()

# Define a function to preprocess text
def preprocess(text):
    tokens = word_tokenize(text.lower())
    lemmas = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return lemmas

# Define a function to calculate the similarity between two questions
def similarity(question1, question2):
    q1 = set(preprocess(question1))
    q2 = set(preprocess(question2))
    if len(q1.union(q2)) == 0:
        return 0
    return len(q1.intersection(q2)) / len(q1.union(q2))

# Define a function to find the most similar question in the dictionary
def find_most_similar(question, qa_pairs):
    similarities = [(q, similarity(question, q)) for q in qa_pairs.keys()]
    return max(similarities, key=lambda x: x[1])[0]




def handle_input(request):
    user = request.user
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # process the input data
            input_data = form.cleaned_data['input_field']

            if input_data.lower() == 'quit':
                print('its quit')
            else:
                most_similar_question = find_most_similar(input_data, qa_pairs)
                if action_check(qa_pairs[most_similar_question], user, request)[0] == True:
                    output_data = action_check(qa_pairs[most_similar_question], user, request)
                    response_data = {'output_data': output_data}
                    return JsonResponse(response_data)
                else:
                    output_data = qa_pairs[most_similar_question]
                    response_data = {'output_data': output_data}
                    return JsonResponse(response_data)


            # return the output c
        else:
            # return the form errors as a JSON response
            errors = {'errors': form.errors.as_json()}
            return JsonResponse(errors, status=400)
    else:
        form = MyForm()
    return render(request, 'Budget/howy.html', {'form': form})