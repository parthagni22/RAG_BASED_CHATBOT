from flask import Flask, request, render_template
from AggieCourses import *
from pinecone import Pinecone

application = Flask(__name__)

app = application

llm = AggieeRag()

## route for home

##import asyncio

@app.route('/')
def index():
    return render_template("AggieCourses.html")

@app.route('/llmtrigger', methods=['POST', 'GET'])
def reports():
    if request.method == 'POST':
        if 'message' in request.form:
            query = request.form['message']
            prompt =llm.augment_prompt(query=query)
            prompt = HumanMessage(
            content=prompt
            )

            llm.messages.append(prompt)

            res = llm.chatbot(llm.messages)
            response= {"message":res.content}
            print("#############----Output----##########################")
            return(response)




if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=8000, debug=True)
    app.run()
