SEND_USER_QUERY_AS_EMAIL = {
    "type": "function",
    "function": {
        "name": "send_user_query_as_email",
        "description": "Sends email to matt with user request and user information.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_name": {
                    "type": "string",
                    "description": "The name of the user",
                },
                "user_email": {
                    "type": "string",
                    "description": "The email of the user",
                },
                "user_query": {
                    "type": "string",
                    "description": "The user's query",
                },
                "user_interest": {
                    "type": "string",
                    "description": "Our product in which the user is interested",
                },
            },
            "required": ["user_email", "user_query", "user_interest"],
        },
    },
}
