import google.generativeai as genai

genai.configure(api_key="AIzaSyCXJYCzx-FLzcRVj89QuwkOXUMo4CYah6c")

models = genai.list_models()

for model in models:
    print(model.name)