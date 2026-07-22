from flask import Blueprint, request, jsonify
from langchain_core.messages import HumanMessage
from app.graph.workflow import compiled_graph

# Create a Flask Blueprint
chat_bp = Blueprint('chat_controller', __name__)

@chat_bp.route('/chat', methods=['POST'])
def handle_chat():
    """
    Endpoint: POST /api/v1/chat
    Payload: { "message": "hello", "thread_id": "user_123" }
    """
    data = request.json
    
    # Validation
    if not data or 'message' not in data:
        return jsonify({"error": "Missing 'message' in request body."}), 400
        
    user_message = data['message']
    thread_id = data.get('thread_id', 'default_session')
    
    # DB / Memory config for this specific thread
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        # Invoke the LangGraph service
        result = compiled_graph.invoke(
            {"messages": [HumanMessage(content=user_message)]}, 
            config=config
        )
        
        return jsonify({
            "response": result["response"],
            "thread_id": thread_id
        }), 200
        
    except Exception as e:
        # In a real app, you would log this error to Sentry/Datadog
        return jsonify({"error": "Internal server error", "details": str(e)}), 500