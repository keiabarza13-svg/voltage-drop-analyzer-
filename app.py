from flask import Flask, render_template, request
from calculations import perform_vd_analysis

app = Flask(__name__)
def get_data(prefix):
    return {
        "location": request.form.get(f'{prefix}_name', 'GENERAL'), # This is the input from index.html
        # ... rest of your keys
    }
@app.route('/calculate', methods=['POST'])
def calculate():
    # 1. Collect inputs from your index.html form
    # Make sure the 'name' attributes in your form match these strings
    user_data = {
        'voltage': request.form.get('voltage'),
        'load_current': request.form.get('load_current'),
        'distance': request.form.get('distance'),
        'wire_size': request.form.get('wire_size', '125'),
        'installation': request.form.get('installation', 'PVC Conduit'),
        'material': request.form.get('material', 'Copper'),
        'system_type': request.form.get('system_type', 'Three Phase'),
        'n_parallel': request.form.get('n_parallel', 1),
        'temp_conductor': request.form.get('temp_conductor', 75),
        'from_point': request.form.get('from_point', 'POINT A'),
        'to_point': request.form.get('to_point', 'POINT B')
    }

    
    analysis_result = perform_vd_analysis(user_data)
    
    return render_template('solution.html', res1=analysis_result, res2=analysis_result)




@app.route('/')
def landing():
    return render_template('landing.html')

# 2. MAIN CALCULATOR (The 2-Location Dashboard)
@app.route('/calculator')
def index():
    return render_template('index.html')

# ... (rest of your imports and routes)

@app.route('/analyze', methods=['POST'])
def analyze():
    # Helper function to extract all 11 parameters per location
    def get_data(prefix):
        return {
            "location": request.form.get(f'{prefix}_name'),
            "system_type": request.form.get(f'{prefix}_system_type'),
            "voltage": request.form.get(f'{prefix}_voltage'),
            "material": request.form.get(f'{prefix}_material'),
            "wire_size": request.form.get(f'{prefix}_wire_size'),
            "installation": request.form.get(f'{prefix}_install'),
            "n_parallel": request.form.get(f'{prefix}_n', 1),
            "distance": request.form.get(f'{prefix}_dist', 0),
            "load_current": request.form.get(f'{prefix}_load', 0),
            "temp_conductor": request.form.get(f'{prefix}_temp', 75),
            "desired_vd": request.form.get(f'{prefix}_limit', 3.0)
        }

    # 1. Get the data for both locations
    data_l1 = get_data('l1')
    data_l2 = get_data('l2')

    # 2. Extract the limit to use for the Pass/Fail check in HTML
    # We convert it to a float so the HTML can do math with it
    try:
        limit_to_send = float(data_l1['desired_vd'])
    except:
        limit_to_send = 3.0 # Fallback

    # 3. Process Location 1 and Location 2
    res1 = perform_vd_analysis(data_l1)
    res2 = perform_vd_analysis(data_l2)

    # 4. SEND EVERYTHING TO HTML
    # Added vd_limit=limit_to_send here
    return render_template(
        'solution.html', 
        res1=res1, 
        res2=res2,
        vd_limit=limit_to_send
    )

if __name__ == '__main__':
    app.run(debug=True)
    