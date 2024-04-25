import autogen

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="""
    A human admin.
    """
)