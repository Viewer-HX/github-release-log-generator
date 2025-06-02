from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
import os
import asyncio
from crew import create_release_log_crew
from config import GitHubRequest, Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    """Home page with the form"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_release_log():
    """Handle release log generation request"""
    try:
        # Get form data
        repository = request.form.get('repository', '').strip()
        from_commit = request.form.get('from_commit', '').strip()
        to_commit = request.form.get('to_commit', '').strip()
        recipient_email = request.form.get('recipient_email', '').strip()
        
        # Validate input
        if not all([repository, from_commit, to_commit, recipient_email]):
            flash('All fields are required!', 'error')
            return redirect(url_for('index'))
        
        # Create request object
        github_request = GitHubRequest(
            repository=repository,
            from_commit=from_commit,
            to_commit=to_commit,
            recipient_email=recipient_email
        )
        
        # Process request
        crew = create_release_log_crew()
        result = crew.process_request(github_request)
        
        if result['status'] == 'success':
            flash('Release log generated and email sent successfully!', 'success')
        else:
            flash(f'Error: {result["message"]}', 'error')
            
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        flash(f'An error occurred: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/api/generate', methods=['POST'])
def api_generate_release_log():
    """API endpoint for release log generation"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not all(k in data for k in ['repository', 'from_commit', 'to_commit', 'recipient_email']):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields: repository, from_commit, to_commit, recipient_email'
            }), 400
        
        # Create request object
        github_request = GitHubRequest(**data)
        
        # Process request
        crew = create_release_log_crew()
        result = crew.process_request(github_request)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    config = Config()
    
    return jsonify({
        'status': 'healthy',
        'config_valid': config.validate_config()
    })

if __name__ == '__main__':
    # Validate configuration
    config = Config()
    if not config.validate_config():
        print("❌ Configuration Error! Please check your .env file.")
        exit(1)
    
    print("🚀 Starting GitHub Release Log Generator Web Interface...")
    print("Visit http://localhost:5000 to use the web interface")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
