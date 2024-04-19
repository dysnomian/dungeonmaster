import os
import requests
from typing import Annotated, Optional, Union, Dict, List

from typing import Annotated, Optional, Union
from pydantic import BaseModel

# Define Pydantic models
class ProjectV2ItemFieldTextValue(BaseModel):
    text: str
    field: dict

class ProjectV2ItemFieldDateValue(BaseModel):
    date: str
    field: dict

class ProjectV2ItemFieldSingleSelectValue(BaseModel):
    name: str
    field: dict

class ProjectV2Item(BaseModel):
    id: str
    fieldValues: list[
        ProjectV2ItemFieldTextValue
        | ProjectV2ItemFieldDateValue
        | ProjectV2ItemFieldSingleSelectValue
    ]
    content: dict

class ProjectV2Response(BaseModel):
    node: dict

# Set environment variables
GITHUB_API_TOKEN = os.environ.get("GITHUB_API_TOKEN")
GITHUB_PROJECT_ID = os.environ.get("GITHUB_PROJECT_ID")

def execute_graphql_query(
    query: Annotated[str, "The GraphQL query to execute."],
    variables: Annotated[dict, "The variables to use in the query."] = None,
    return_json: Annotated[bool, "Whether to return the response as JSON or a Python dict."] = True,
) -> Union[dict, ProjectV2Response]:
    """
    Execute a GraphQL query against the GitHub API.

    Args:
        query (str): The GraphQL query to execute.
        variables (dict, optional): The variables to use in the query. Defaults to None.
        return_json (bool, optional): Whether to return the response as JSON or a Python dict. Defaults to True.

    Returns:
        Union[dict, ProjectV2Response]: The response from the GraphQL query, either as a JSON string or a Python dict.
    """
    headers = {
        "Authorization": f"Bearer {GITHUB_API_TOKEN}",
        "Content-Type": "application/json",
    }
    request_data = {"query": query}
    if variables:
        request_data["variables"] = variables

    response = requests.post(
      "https://api.github.com/graphql",
      json=request_data,
      timeout=10,
      headers=headers
    )

    response.raise_for_status()

    if return_json:
        return response.json()
    else:
        return ProjectV2Response(**response.json()["data"])

def get_project_board_status(
    project_id: Annotated[str, "The ID of the GitHub project to fetch."] = GITHUB_PROJECT_ID,
    return_json: Annotated[bool, "Whether to return the response as JSON or a Python dict."] = True,
) -> Union[dict, ProjectV2Response]:
    """
    Fetch the current status of a GitHub project board.

    Args:
        project_id (str, optional): The ID of the GitHub project to fetch.
        return_json (bool, optional): Whether to return the response as JSON or a Python dict. Defaults to True.

    Returns:
        Union[dict, ProjectV2Response]: The response from the GraphQL query, either as a JSON string or a Python dict.
    """
    query = """
    query {
      node(id: "%s") {
        ... on ProjectV2 {
          items(first: 20) {
            nodes {
              id
              fieldValues(first: 8) {
                nodes {
                  ... on ProjectV2ItemFieldTextValue {
                    text
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                  }
                  ... on ProjectV2ItemFieldDateValue {
                    date
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                  }
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    name
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                  }
                }
              }
              content {
                ... on DraftIssue {
                  title
                  body
                }
                ... on Issue {
                  title
                  assignees(first: 10) {
                    nodes {
                      login
                    }
                  }
                }
                ... on PullRequest {
                  title
                  assignees(first: 10) {
                    nodes {
                      login
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """ % project_id

    return execute_graphql_query(query, return_json=return_json)

def get_project_items(
    project_id: Annotated[Optional[str], "The ID of the GitHub project to fetch items from. Defaults to GITHUB_PROJECT_ID if not provided."] = GITHUB_PROJECT_ID,


    return_json: Annotated[bool, "Whether to return the response as JSON or a Python dict."] = True,
) -> Union[dict, ProjectV2Response]:
    """
    Fetch information about items in a GitHub project.

    Args:
        project_id (Optional[str]): The ID of the GitHub project to fetch items from. Defaults to GITHUB_PROJECT_ID if not provided.
        return_json (bool, optional): Whether to return the response as JSON or a Python dict. Defaults to True.

    Returns:
        Union[dict, ProjectV2Response]: The response from the GraphQL query, either as a JSON string or a Python dict.
    """
    query = """
    query {
      node(id: "%s") {
        ... on ProjectV2 {
          items(first: 20) {
            nodes {
              id
              fieldValues(first: 8) {
                nodes {
                  ... on ProjectV2ItemFieldTextValue {
                    text
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                  }
                  ... on ProjectV2ItemFieldDateValue {
                    date
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                  }
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    name
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                  }
                }
              }
              content {
                ... on DraftIssue {
                  title
                  body
                }
                ... on Issue {
                  title
                  assignees(first: 10) {
                    nodes {
                      login
                    }
                  }
                }
                ... on PullRequest {
                  title
                  assignees(first: 10) {
                    nodes {
                      login
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """ % project_id

    return execute_graphql_query(query, return_json=return_json)

def update_project_item_field(
    item_id: Annotated[str, "The ID of the project item to update."],
    field_id: Annotated[str, "The ID of the field to update."],
    value: Annotated[dict, "The new value for the field."],
    project_id: Annotated[Optional[str], "The ID of the GitHub project. Defaults to GITHUB_PROJECT_ID if not provided."] = GITHUB_PROJECT_ID,
    return_json: Annotated[bool, "Whether to return the response as JSON or a Python dict."] = True,
) -> Union[dict, ProjectV2Response]:
    """
    Update a custom text, number, or date field for a project item.

    Args:
        project_id (Optional[str]): The ID of the GitHub project. Defaults to GITHUB_PROJECT_ID if not provided.
        item_id (str): The ID of the project item to update.
        field_id (str): The ID of the field to update.
        value (dict): The new value for the field.
        return_json (bool, optional): Whether to return the response as JSON or a Python dict. Defaults to True.

    Returns:
        Union[dict, ProjectV2Response]: The response from the GraphQL mutation, either as a JSON string or a Python dict.
    """
    query = """
    mutation {
      updateProjectV2ItemFieldValue(input: {
        projectId: "%s"
        itemId: "%s"
        fieldId: "%s"
        value: %s
      }) {
        projectV2Item {
          id
        }
      }
    }
    """ % (project_id, item_id, field_id, str(value).replace("'", '"'))

    return execute_graphql_query(query, return_json=return_json)

def update_project_item_single_select_field(
    item_id: Annotated[str, "The ID of the project item to update."],
    field_id: Annotated[str, "The ID of the single select field to update."],
    option_id: Annotated[str, "The ID of the new single select option."],
    project_id: Annotated[Optional[str], "The ID of the GitHub project. Defaults to GITHUB_PROJECT_ID if not provided."] = GITHUB_PROJECT_ID,    return_json: Annotated[bool, "Whether to return the response as JSON or a Python dict."] = True,
) -> Union[dict, ProjectV2Response]:
    """
    Update the value of a single select field for a project item.

    Args:
        item_id (str): The ID of the project item to update.
        field_id (str): The ID of the single select field to update.
        option_id (str): The ID of the new single select option.
        project_id (str, optional): The ID of the GitHub project.
        return_json (bool, optional): Whether to return the response as JSON or a Python dict. Defaults to True.

    Returns:
        Union[dict, ProjectV2Response]: The response from the GraphQL mutation, either as a JSON string or a Python dict.
    """
    query = """
    mutation {
      updateProjectV2ItemFieldValue(input: {
        projectId: "%s"
        itemId: "%s"
        fieldId: "%s"
        value: {
          singleSelectOptionId: "%s"
        }
      }) {
        projectV2Item {
          id
        }
      }
    }
    """ % (project_id, item_id, field_id, option_id)

    return execute_graphql_query(query, return_json=return_json)

def update_project_item_iteration_field(
  item_id: Annotated[str, "The ID of the project item to update."],
  field_id: Annotated[str, "The ID of the iteration field to update."],
  iteration_id: Annotated[str, "The ID of the new iteration."],
  project_id: Annotated[Optional[str], "The ID of the GitHub project. Defaults to GITHUB_PROJECT_ID if not provided."] = GITHUB_PROJECT_ID,
  return_json: Annotated[bool, "Whether to return the response as JSON or a Python dict."] = True,
) -> Union[dict, ProjectV2Response]:
    """
    Update the value of an iteration field for a project item.

    Args:
        item_id (str): The ID of the project item to update.
        field_id (str): The ID of the iteration field to update.
        iteration_id (str): The ID of the new iteration.
        project_id (str, optional): The ID of the GitHub project.
        return_json (bool, optional): Whether to return the response as JSON or a Python dict. Defaults to True.

    Returns:
        Union[dict, ProjectV2Response]: The response from the GraphQL mutation, either as a JSON string or a Python dict.
    """
    query = """
    mutation {
      updateProjectV2ItemFieldValue(input: {
        projectId: "%s"
        itemId: "%s"
        fieldId: "%s"
        value: {
          iterationId: "%s"
        }
      }) {
        projectV2Item {
          id
        }
      }
    }
    """ % (project_id, item_id, field_id, iteration_id)

    return execute_graphql_query(query, return_json=return_json)

def get_project_fields(
    project_id: Annotated[Optional[str], "The ID of the GitHub project to fetch fields from. Defaults to GITHUB_PROJECT_ID if not provided."] = GITHUB_PROJECT_ID,
    return_json: Annotated[bool, "Whether to return the response as JSON or a Python dict."] = True,
) -> Union[dict, Dict[str, List[Dict[str, Union[str, Dict[str, List[Dict[str, str]]]]]]]]:
    """
    Fetch the fields of a GitHub project.

    Args:
        project_id (Optional[str]): The ID of the GitHub project to fetch fields from. Defaults to GITHUB_PROJECT_ID if not provided.
        return_json (bool, optional): Whether to return the response as JSON or a Python dict. Defaults to True.

    Returns:
        Union[dict, Dict[str, List[Dict[str, Union[str, Dict[str, List[Dict[str, str]]]]]]]]: The response from the GraphQL query, either as a JSON string or a Python dict.
    """
    query = """
    query {
      node(id: "%s") {
        ... on ProjectV2 {
          fields(first: 20) {
            nodes {
              ... on ProjectV2Field {
                id
                name
              }
              ... on ProjectV2IterationField {
                id
                name
                configuration {
                  iterations {
                    startDate
                    id
                  }
                }
              }
              ... on ProjectV2SingleSelectField {
                id
                name
                options {
                  id
                  name
                }
              }
            }
          }
        }
      }
    }
    """ % project_id

    return execute_graphql_query(query, return_json=return_json)

def get_board_status_options(
    project_id: Annotated[Optional[str], "The ID of the GitHub project to fetch fields from. Defaults to GITHUB_PROJECT_ID if not provided."] = GITHUB_PROJECT_ID,
) -> Dict[str, str]:
    """
    Fetch the status options for a project board.

    Args:
        project_id (Optional[str]): The ID of the GitHub project to fetch fields from. Defaults to GITHUB_PROJECT_ID if not provided.

    Returns:
        Dict[str, str]: A dictionary of name to ID mappings for the status options.
    """
    fields = get_project_fields(project_id)
    status_field_id = None
    for field in fields["node"]["fields"]["nodes"]:
        if field["name"] == "Status":
            status_field_id = field["id"]
            break

    if status_field_id is None:
        raise ValueError("Status field not found in project fields.")

    options = field["options"]
    return {option["name"]: option["id"] for option in options}

def update_item_status(
        item_id: Annotated[str, "The ID of the project item to update."],
        status: Annotated[str, "The new status of the project item."]
) -> Union[dict, ProjectV2Response]:
    """
    Update the status of a project item.

    Args:
        item_id (str): The ID of the project item to update.
        status (str): The new status of the project item.

    Returns:
        Union[dict, ProjectV2Response]: The response from the GraphQL mutation, either as a JSON string or a Python dict.
    """
    fields = get_project_fields()
    status_options = get_board_status_options()
    status_field_id = None
    