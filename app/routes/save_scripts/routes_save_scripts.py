from flask import Blueprint, request, jsonify
from app.models.scriptsModel import Script
from datetime import datetime

save_scripts_bp = Blueprint('save_scripts', __name__)

@save_scripts_bp.route('/save-script', methods=['POST'])
def save_script():
    try:
        data = request.get_json()
        
        # Check if script exists
        existing_script = Script.get_by_user_and_title(data['user_id'], data['title'])
        
        if existing_script:
            # Update existing script
            existing_script.content = data['content']
            existing_script.updated_at = datetime.now()
            existing_script.update()
            
            return jsonify({
                'message': 'Script updated successfully',
                'script': {
                    'id': existing_script.id,
                    'title': existing_script.title,
                    'content': existing_script.content,
                    'updated_at': existing_script.updated_at
                }
            }), 200
        else:
            # Create new script
            script = Script(
                user_id=data['user_id'],
                title=data['title'],
                content=data['content'],
                created_at=datetime.now()
            )
            script.save()
            
            return jsonify({
                'message': 'Script saved successfully',
                'script': {
                    'id': script.id,
                    'title': script.title,
                    'content': script.content,
                    'created_at': script.created_at
                }
            }), 201
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@save_scripts_bp.route('/delete-script', methods=['POST'])
def delete_script():
    try:
        data = request.get_json()
        script_id = data.get('script_id')
        
        if not script_id:
            return jsonify({'error': 'Script ID is required'}), 400
            
        # Delete script
        Script.delete(script_id)
        
        return jsonify({
            'message': 'Script deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
