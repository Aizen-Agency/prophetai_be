from flask import Blueprint, request, jsonify
from app.models.scriptsModel import Script
from app.extensions import db
from datetime import datetime

save_scripts_bp = Blueprint('save_scripts', __name__)

@save_scripts_bp.route('/save-script', methods=['POST'])
def save_script():
    try:
        data = request.get_json()
        
        # Check if script exists
        existing_script = Script.query.filter_by(
            user_id=data['user_id'],
            title=data['title']
        ).first()
        
        if existing_script:
            # Update existing script
            existing_script.content = data['content']
            existing_script.product_name = data.get('product_name')
            existing_script.is_locked = data.get('is_locked', False)
            db.session.commit()
            return jsonify({
                'message': 'Script updated successfully',
                'script_id': existing_script.id
            }), 200
        else:
            # Create new script
            new_script = Script(
                user_id=data['user_id'],
                title=data['title'],
                content=data['content'],
                product_name=data.get('product_name'),
                is_locked=data.get('is_locked', False)
            )
            db.session.add(new_script)
            db.session.commit()
            return jsonify({
                'message': 'Script saved successfully',
                'script_id': new_script.id
            }), 201
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@save_scripts_bp.route('/delete-script', methods=['POST'])
def delete_script():
    try:
        data = request.get_json()
        script = Script.query.filter_by(
            id=data['script_id'],
            user_id=data['user_id']
        ).first()
        
        if script:
            db.session.delete(script)
            db.session.commit()
            return jsonify({'message': 'Script deleted successfully'}), 200
        else:
            return jsonify({'error': 'Script not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
