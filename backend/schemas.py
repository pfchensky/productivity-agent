CHECK_IN_RESPONSE_SCHEMA = {
    "type" : "object",
    "properties" : {
            "progress" : {
                # The user's current completion percentage in plain int
                # Use null when the user doesn't mention progress
                "type" : "INTEGER",
                "nullable" : True,
                "minimum" : 0,
                "maximum" : 100
            },

            "time_remaining" : {
                # Amount of work time the user describes is remaining
                # Keep the original string in text like "2 hours 11 minutes, 33 minutes, 10 seconds"
                # Use null when no time is provided
                "type" : "STRING",
                "nullable" : True
            },

            # Whether the task now requires more importance 
            # Could be due to increased importance, risk, blocking work,
            # serious consequences, or unusually high difficulty as described by user.
            "importance_signal" : {
                "type" : "STRING",
                "nullable" : True,
                "enum" : ["Increased", "Unchanged", "Decreased"]
            },

            # Short explanation of the user's check in stored for records
            "summary" : {
                "type" : "STRING"
            }
    },

    # Every field must be returned, even with null values so required includes all fields
    "required" : [
        "progress",
        "time_remaining",
        "importance_signal",
        "summary"
    ]
}