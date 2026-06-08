from flask import Flask, request, jsonify, render_template
from main import calculate_gaokao_score

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    try:
        data = request.get_json()
        main_scores = {
            '语文': data['yuwen'],
            '数学': data['shuxue'],
            '外语': data['waiyu'],
        }
        elective_inputs = [data['elective1'], data['elective2'], data['elective3']]
        result = calculate_gaokao_score(main_scores, elective_inputs)
        return jsonify({'ok': True, 'result': result})
    except ValueError as e:
        return jsonify({'ok': False, 'error': str(e)})
    except KeyError as e:
        return jsonify({'ok': False, 'error': f'缺少必填字段: {e}'})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
