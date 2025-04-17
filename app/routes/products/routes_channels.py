from flask import Blueprint, request, jsonify
from app.models.channels import Channel

channels_bp = Blueprint('channels', __name__)

@channels_bp.route('/channels', methods=['POST'])
def add_channel():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'product_id', 'product_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create new channel
        channel = Channel(
            user_id=data['user_id'],
            product_id=data['product_id'],
            product_name=data['product_name'],
            link=data.get('link'),
            description=data.get('description')
        )
        
        channel.save()
        
        return jsonify({'message': 'Channel added successfully', 'channel': channel.to_dict()}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@channels_bp.route('/channels/<int:user_id>', methods=['GET'])
def get_channels(user_id):
    try:
        channels = Channel.get_by_user(user_id)
        return jsonify({'channels': [channel.to_dict() for channel in channels]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@channels_bp.route('/channels/<int:channel_id>', methods=['DELETE'])
def delete_channel(channel_id):
    try:
        channel = Channel.get_by_id(channel_id)
        if not channel:
            return jsonify({'error': 'Channel not found'}), 404
        
        Channel.delete(channel_id)
        
        return jsonify({'message': 'Channel deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
