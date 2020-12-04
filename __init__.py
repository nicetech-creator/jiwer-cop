from flask import Flask, render_template, jsonify, request
import jiwer
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        req_data = request.get_json()

        compose_rule_set = []
        if req_data.get('to_lower_case', False) == True:
            compose_rule_set.append(jiwer.ToLowerCase())
        if req_data.get('strip_punctuation', False) == True:
            compose_rule_set.append(jiwer.RemovePunctuation())
        if req_data.get('strip_words', False) == True:
            compose_rule_set.append(jiwer.Strip())
        if req_data.get('strip_multi_space', False) == True:
            compose_rule_set.append(jiwer.RemoveMultipleSpaces())
        word_excepts = req_data.get('t_words', '')
        if word_excepts != '':
            words = [a.strip() for a in word_excepts.split(",")]
            compose_rule_set.append(jiwer.RemoveSpecificWords(words))

        compose_rule_set.append(jiwer.RemoveWhiteSpace(replace_by_space=req_data.get('replace_whitespace', False)))
        
        transformation  = jiwer.Compose(compose_rule_set)

        measures = jiwer.compute_measures(
            req_data.get('s_truth', ""), 
            req_data.get('s_hypo', ""), 
            truth_transform=transformation, 
            hypothesis_transform=transformation
        )
        
        return jsonify({
            "wer": measures['wer'],
            "mer": measures['mer'],
            "wil": measures['wil']
            })
    except:
        return jsonify("API endpoint Error")


if __name__ == '__main__':
    app.run()