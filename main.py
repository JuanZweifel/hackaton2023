from flask import Flask, render_template, url_for, request
import boto3
import json

app = Flask(__name__)

boto3_bedrock = boto3.client("bedrock-runtime")
def call_bedrock(input: str) -> dict:
    contentType = 'application/json'
    accept = "*/*"
    
    request_body = {
        "prompt": input,
        "max_tokens_to_sample": 900,
        "temperature": 0.5,
        "top_k": 250,
        "top_p": 1,
        "stop_sequences": ["\n\nHuman:"],
        "anthropic_version": "bedrock-2023-05-31"
    }
    
    response = boto3_bedrock.invoke_model(
        modelId="anthropic.claude-v2",
        contentType=contentType,
        accept=accept,
        body=json.dumps(request_body)
    )

    response_content = response["body"].read().decode("utf-8")
    return json.loads(response_content)

@app.get("/bedrock")
def hello_bedrock():
    args=request.args.to_dict()
    if "q" not in args:
        return {"Mensaje":"Error!!!"}
    return call_bedrock(f"\n\nHuman: Ponte en el caso de que eres un asistente virtual financiero, tu nombre es Finny, por ende asume ese nombre como tal, ahora, te pasare esta pregunta: {args['q']} \n\nAssistant:")

@app.route('/')
def index():
    return render_template("frontpage.html")

@app.route("/chat")
def frontpage():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=8080)