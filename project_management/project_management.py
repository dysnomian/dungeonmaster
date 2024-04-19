import os
import autogen

from github_projects_graphql import get_board_status_options, get_project_board_status, update_project_item_field, update_project_item_single_select_field, update_project_item_iteration_field, get_project_fields

# Set environment variables
GITHUB_API_TOKEN = os.environ.get("GITHUB_API_TOKEN")
GITHUB_PROJECT_ID = os.environ.get("GITHUB_PROJECT_ID")

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")

general_llm_config = {
    "seed": 45, 
    "temperature": 1.0,
    "config_list": config_list,
    "timeout": 120,
}

def termination_msg(x):
    """
    Check if the message is a termination message.
    """
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

# humans
user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="""
    A human admin named Liss. Will request help with project planning and provide status updates.
    """,
    code_execution_config=False,
)

executor = autogen.UserProxyAgent(
    name="Executor",
    human_input_mode="ALWAYS",
    code_execution_config={"last_n_messages": 3, "work_dir": "paper"},
    system_message="Executor. Execute code and provide the output to the user."
)

# bots

## Software team

software_planner = autogen.AssistantAgent(
    name="SoftwarePlanner",
    is_termination_msg=termination_msg,
    llm_config=general_llm_config,
    system_message="""
    You are the software planner. When code is requested to solve a problem, plan the code for the software engineer and code reviewer. Describe the task and the expected outcome. Specify requirements. When the code meets the requirements, approve it. 
    """
)

software_engineer = autogen.AssistantAgent(
    name="SoftwareEngineer",
    is_termination_msg=termination_msg,
    llm_config=general_llm_config,
    system_message="""
    You are a skilled software engineer who is skilled with Python. You write reusable code and flexible scripts. Draft code according to the plan given by the planner. Integrate revisions from the code reviewer. When the code reviewer and planner have approved, send the code to the executor. When the code is executed, if the results are not as expected, return the code to the software engineer for revisions.
    """
)

code_reviewer = autogen.AssistantAgent(
    name="CodeReviewer",
    is_termination_msg=termination_msg,
    llm_config=general_llm_config,
    system_message="""
    You are an experienced code reviewer who is skilled with Python. Review the code written by the software engineer. You consider safety, reusability, readability, and purpose. Consider the software planner's requirements. Make suggestions for improvement. When the code is ready, approve it.
    """
)

## project team

project_manager = autogen.AssistantAgent(
    name="ProjectManager",
    is_termination_msg=termination_msg,
    llm_config=general_llm_config,
    code_execution_config={"last_n_messages": 5, "work_dir": 'paper'},
    human_input_mode="ALWAYS",
    system_message="""
    You are an agile project manager. You help the user with project planning and provide status updates. You read the board status from the Github Projects board. You help the user update item titles to be specific and scoped. You write user stories for the tickets. You update the tickets with status updates and adjust the requirements as needed. You help the user with project planning and provide status updates. You come up with priorities and timelines. You are informed about ADHD and how to work with people who have ADHD. You are patient and understanding. You are a good listener.
    """
)

get_project_board_status = project_manager.register_for_execution()(get_project_board_status)
get_project_board_status = project_manager.register_for_llm(
    name="get_project_board_status",
    description="Get the status of the Dungeonmaster project board from the Github API."
)(get_project_board_status)

update_project_item_field = project_manager.register_for_execution()(update_project_item_field)
update_project_item_field = project_manager.register_for_llm(
    name="update_project_item_field",
    description="Update a field for an item on the Dungeonmaster project board."
)(update_project_item_field)

update_project_item_single_select_field = project_manager.register_for_execution()(update_project_item_single_select_field)
update_project_item_single_select_field = project_manager.register_for_llm(
    name="update_project_item_single_select_field",
    description="Update a single select field for an item on the Dungeonmaster project board."
)(update_project_item_single_select_field)

update_project_item_iteration_field = project_manager.register_for_execution()(update_project_item_iteration_field)
update_project_item_iteration_field = project_manager.register_for_llm(
    name="update_project_item_iteration_field",
    description="Update the iteration field for an item on the Dungeonmaster project board."
)(update_project_item_iteration_field)

get_project_fields = project_manager.register_for_execution()(get_project_fields)
get_project_fields = project_manager.register_for_llm(
    name="get_project_fields",
    description="Get the fields for the Dungeonmaster project board."
)(get_project_fields)

# adhd_coach = autogen.AssistantAgent(
#     name="AdhdCoach",
#     is_termination_msg=termination_msg,
#     llm_config=general_llm_config,
#     code_execution_config={"last_n_messages": 5, "work_dir": workdir_path},
#     human_input_mode="NEVER",
#     system_message="""
#     You are an ADHD coach who is informed about software and project planning. You help the user break down projects into achievable chunks. You provide guidance with planning pomodoros and breaks. You help record accomplishments, advise on maintaining healthy habits, and provide encouragement. You are patient and understanding. You are a good listener.
#     """
# )

# start the "group chat" between agents and humans

groupchat = autogen.GroupChat(
    agents=[
        user_proxy,
        executor,
        # software_planner,
        # software_engineer,
        # code_reviewer,
        project_manager
    ],
    messages=[],
    max_round=50,
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=general_llm_config
)

# Start the Chat!
user_proxy.initiate_chat(
    manager,
    message="""
    Please help me with project planning and doing status updates for the Dungeonmaster project.
    """,
)
