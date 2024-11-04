from flask import Flask, render_template, request, jsonify
from curp_utils import generate_curp, validate_date

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_curp', methods=['POST'])
def get_curp():
    try:
        data = request.get_json()
        
        # Validate date
        if not validate_date(data['dia'], data['mes'], data['año']):
            return jsonify({'error': 'Fecha inválida'}), 400
            
        # Format date
        fecha = f"{data['año']}-{data['mes']:02d}-{data['dia']:02d}"
        
        curp = generate_curp(
            data['nombres'],
            data['apellido1'],
            data['apellido2'],
            fecha,
            data['sexo'],
            data['estado']
        )
        
        return jsonify({'curp': curp})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)