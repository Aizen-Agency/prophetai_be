from flask import Blueprint, request, jsonify
from app.models.scriptsModel import Script
from datetime import datetime

save_scripts_bp = Blueprint('save_scripts', __name__)

@save_scripts_bp.route('/save-script', methods=['POST'])
def save_script():
    try:
        data = request.get_json()
        
        # Check if script exists
        existing_script = Script.get_by_user_and_idea_id(data['user_id'], data['idea_id'])
        
        if existing_script:
            # Update existing script
            existing_script.script_content = data['script_content']
            existing_script.is_locked = data['is_locked']
            existing_script.update()
            
            return jsonify({
                'message': 'Script updated successfully',
                'script': {
                    'id': existing_script.id,
                    'idea_id': existing_script.idea_id,
                    'idea_title': existing_script.idea_title,
                    'script_title': existing_script.script_title,
                    'script_content': existing_script.script_content,
                    'is_locked': existing_script.is_locked
                }
            }), 200
        else:
            # Create new script
            script = Script(
                user_id=data['user_id'],
                idea_id=data['idea_id'],
                idea_title=data['idea_title'],
                script_title=data['script_title'],
                script_content=data['script_content'],
                is_locked=data['is_locked']
            )
            script.save()
            
            return jsonify({
                'message': 'Script saved successfully',
                'script': {
                    'id': script.id,
                    'idea_id': script.idea_id,
                    'idea_title': script.idea_title,
                    'script_title': script.script_title,
                    'script_content': script.script_content,
                    'is_locked': script.is_locked
                }
            }), 201
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@save_scripts_bp.route('/get-script', methods=['POST'])
def get_script():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        idea_id = data.get('idea_id')
        
        if not user_id or not idea_id:
            return jsonify({'error': 'User ID and Idea ID are required'}), 400
            
        # Get saved script
        saved_script = Script.get_by_user_and_idea_id(user_id, idea_id)
        
        if saved_script:
            return jsonify({
                'saved_script': {
                    'id': saved_script.id,
                    'idea_id': saved_script.idea_id,
                    'idea_title': saved_script.idea_title,
                    'script_title': saved_script.script_title,
                    'script_content': saved_script.script_content,
                    'is_locked': saved_script.is_locked,
                    'date': saved_script.created_at.isoformat()
                }
            }), 200
        else:
            return jsonify({'message': 'No saved script found'}), 404
            
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
